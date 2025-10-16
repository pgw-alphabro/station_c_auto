import os
import ssl
import whisper
from services.gpt_service import call_gpt

async def analyze_meeting_audio(file_paths: list, upload_dir: str) -> str:
    """미팅 오디오 분석 (Whisper STT + GPT)"""
    if not file_paths:
        return "업로드된 미팅 오디오가 없습니다."
    
    # SSL 인증서 검증 비활성화
    ssl._create_default_https_context = ssl._create_unverified_context
    
    # Whisper 모델 로드 (한번만 로드)
    try:
        model = whisper.load_model("tiny")  # 또는 "small" 추천
        print("✅ Whisper 모델 로드 완료")
    except Exception as e:
        print(f"❌ Whisper 모델 로드 실패: {e}")
        return f"STT 처리 중 오류가 발생했습니다: {str(e)}"
    
    # 모든 오디오 파일에서 텍스트 추출
    all_transcripts = []
    for file_path in file_paths:
        full_path = os.path.join(upload_dir, file_path)
        if os.path.exists(full_path):
            try:
                print(f"🎵 Whisper STT 처리 중: {file_path}")
                
                # Whisper는 M4A, MP3 등을 직접 지원 - 변환 불필요!
                whisper_result = model.transcribe(
                    full_path, 
                    language="ko",
                    fp16=False,  # CPU 사용 시 False
                    verbose=False  # 상세 로그 끄기
                )
                transcript = whisper_result["text"].strip()
                
                if transcript:
                    all_transcripts.append(f"파일: {file_path}\n내용: {transcript}")
                    print(f"✅ Whisper STT 완료: {len(transcript)}자 추출")
                else:
                    all_transcripts.append(f"파일: {file_path}\n내용: 음성을 인식할 수 없습니다.")
                    
            except Exception as e:
                print(f"❌ Whisper STT 처리 실패: {e}")
                all_transcripts.append(f"파일: {file_path}\n내용: STT 처리 중 오류 발생 - {str(e)}")
        else:
            all_transcripts.append(f"파일을 찾을 수 없습니다: {file_path}")
    
    # 모든 파일이 실패한 경우
    if not any("내용:" in t and "오류" not in t and "찾을 수 없습니다" not in t for t in all_transcripts):
        return "모든 오디오 파일 처리에 실패했습니다."
    
    # GPT-5로 직접 전체 텍스트 분석 (청크 처리 제거)
    all_transcripts_text = "\n\n".join(all_transcripts)
    print(f"📝 STT 텍스트 길이: {len(all_transcripts_text)}자")
    
    final_prompt = f"""
    다음은 미팅 오디오에서 추출된 전체 텍스트입니다.
    이 텍스트를 분석하여 Station C 진단보고서에 필요한 핵심 정보를 추출해주세요. 마크다운은 제외해주세요.
    
    미팅 오디오 텍스트:
    {all_transcripts_text}
    
    다음 형식으로 핵심 내용을 정리해주세요. 마크다운 문법을 사용하지 말고 일반 텍스트로 작성해주세요:
    
    ■ 미팅 개요
    - 미팅 주제: [전체 미팅의 주요 주제나 목적]
    - 참석자: [참석자 정보]
    - 미팅 시간: [미팅 시간 정보]
    
    ■ 주요 논의사항
    - [전체 미팅에서 논의된 주요 사항들]
    
    ■ 결정사항
    - [미팅에서 결정된 중요 사항들]
    
    ■ 액션 아이템
    - [실행해야 할 구체적인 액션 아이템들]
    
    ■ 사업 관련 핵심 내용
    - [사업, 전략, 목표 등과 관련된 핵심 내용들]
    - [구체적인 수치, 목표, 계획 등]
    
    지시사항:
    1. 전체 텍스트를 종합하여 일관성 있는 분석을 제공하세요.
    2. 중복되는 내용은 통합하여 정리하세요.
    3. 구체적인 수치, 목표, 계획 등을 정확히 추출하세요.
    4. 정보가 없는 경우에만 "정보 없음"으로 표시하세요.
    """
    
    return await call_gpt(final_prompt)