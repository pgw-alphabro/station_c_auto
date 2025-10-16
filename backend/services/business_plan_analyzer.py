import os
from utils.file_processor import extract_text_from_file
from services.gpt_service import call_gpt

async def analyze_business_plan(file_paths: list, upload_dir: str) -> str:
    """사업계획서 분석 (OCR + GPT)"""
    if not file_paths:
        return "업로드된 사업계획서가 없습니다."
    
    # 파일 내용을 텍스트로 추출 (OCR 및 다양한 파일 형식 지원)
    extracted_text = ""
    for file_path in file_paths:
        try:
            # 실제 파일 경로로 읽기
            full_path = os.path.join(upload_dir, file_path)
            if os.path.exists(full_path):
                # OCR 및 파일 처리 함수 사용
                content = extract_text_from_file(full_path)
                extracted_text += f"\n\n=== 파일: {file_path} ===\n{content}"
            else:
                extracted_text += f"\n\n=== 파일: {file_path} ===\n파일을 찾을 수 없습니다."
        except Exception as e:
            print(f"파일 처리 오류 {file_path}: {e}")
            extracted_text += f"\n\n=== 파일: {file_path} ===\n파일 처리 중 오류 발생: {str(e)}"
    
    # GPT-5로 직접 전체 텍스트 분석 (청크 처리 제거)
    print(f"📄 사업계획서 텍스트 길이: {len(extracted_text)}자")
    
    final_prompt = f"""
    다음은 사업계획서에서 추출된 전체 텍스트입니다.
    이 텍스트를 분석하여 Station C 진단보고서에 필요한 핵심 정보를 추출해주세요. 마크다운은 제외해주세요.
    
    사업계획서 텍스트:
    {extracted_text}
    
    다음 형식으로 핵심 내용을 정리해주세요. 마크다운 문법을 사용하지 말고 일반 텍스트로 작성해주세요:
    
    ■ 기업 개요
    • 기업명: [텍스트에서 찾은 기업명, 브랜드명, 사업체명]
    • 업종: [텍스트에서 찾은 사업 분야, 제품/서비스 분야]
    • 설립년도: [텍스트에서 찾은 설립, 창립, 시작년도]
    • 대표자: [텍스트에서 찾은 대표자명, CEO, 창립자명]
    
    ■ 제품/서비스
    • [텍스트에서 찾은 주요 제품/서비스들]
    
    ■ 시장 분석
    • 타겟 시장: [텍스트에서 찾은 타겟 시장 정보]
    • 시장 규모: [텍스트에서 찾은 시장 규모 정보]
    • 경쟁사 분석: [텍스트에서 찾은 경쟁사 정보]
    
    ■ 비즈니스 모델
    • [텍스트에서 찾은 수익 모델들]
    
    ■ 재무 계획
    • [텍스트에서 찾은 재무 목표들 - 구체적 숫자 포함]
    
    ■ 사업비 및 투자 정보
    • 총 사업비: [텍스트에서 찾은 총 사업비 금액]
    • 지원금: [텍스트에서 찾은 지원금 금액]
    • 자기부담금: [텍스트에서 찾은 자기부담금 금액]
    • 투자 유치: [텍스트에서 찾은 투자 유치 금액]
    • 매출 목표: [텍스트에서 찾은 매출 목표 금액]
    
    ■ 기타 중요 정보
    • [텍스트에서 찾은 기타 중요한 정보들]
    
    지시사항:
    1. 모든 청크 요약을 종합하여 일관성 있는 분석을 제공하세요.
    2. 중복되는 내용은 통합하여 정리하세요.
    3. 숫자, 금액, 연도 등은 정확히 추출하세요.
    4. 정보가 없는 경우에만 "정보 없음"으로 표시하세요.
    """
    
    return await call_gpt(final_prompt)
