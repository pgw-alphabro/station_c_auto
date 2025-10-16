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
    
    # 청크 단위로 나누어 요약 후 병합
    # 텍스트를 청크로 나누기 (각 청크는 약 1000자)
    chunk_size = 1000
    chunks = []
    for i in range(0, len(extracted_text), chunk_size):
        chunk = extracted_text[i:i + chunk_size]
        chunks.append(chunk)
    
    print(f"📄 사업계획서 텍스트를 {len(chunks)}개 청크로 분할")
    
    # 각 청크를 개별적으로 요약
    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        print(f"🔄 사업계획서 청크 {i+1}/{len(chunks)} 요약 중...")
        
        chunk_prompt = f"""
        다음은 사업계획서에서 추출된 텍스트의 일부입니다.
        이 청크에서 Station C 진단보고서에 필요한 핵심 정보를 추출하여 간단히 요약해주세요. 마크다운은 제외해주세요.
        
        텍스트 청크:
        {chunk}
        
        다음 형식으로 핵심 내용만 요약해주세요:
        - 기업 정보: [기업명, 업종, 설립년도, 대표자 등]
        - 제품/서비스: [주요 제품/서비스 내용]
        - 시장 정보: [타겟 시장, 시장 규모, 경쟁사 등]
        - 비즈니스 모델: [수익 모델, 사업 방식]
        - 재무 정보: [매출, 투자, 사업비 등 구체적 숫자]
        - 기타 중요 정보: [기타 핵심 내용]
        """
        
        chunk_summary = await call_gpt(chunk_prompt)
        chunk_summaries.append(f"=== 청크 {i+1} 요약 ===\n{chunk_summary}\n")
    
    # 모든 청크 요약을 병합하여 최종 분석
    combined_summaries = "\n\n".join(chunk_summaries)
    
    final_prompt = f"""
    다음은 사업계획서 파일들을 청크 단위로 나누어 각각 요약한 결과입니다.
    이 요약들을 종합하여 Station C 진단보고서에 필요한 최종 사업계획서 분석을 작성해주세요. 마크다운은 제외해주세요.
    
    청크별 요약 결과:
    {combined_summaries}
    
    위 요약들을 종합하여 다음 형식으로 최종 정리해주세요. 마크다운 문법을 사용하지 말고 일반 텍스트로 작성해주세요:
    
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
