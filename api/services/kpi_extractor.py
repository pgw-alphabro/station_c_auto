from services.gpt_service import call_gpt

async def extract_kpis(business_plan: str, meeting: str) -> str:
    """KPI 추출"""
    prompt = f"""
    다음은 사업계획서와 미팅 분석 결과입니다. 
    Station C 진단보고서에 필요한 핵심성과지표(KPI)를 추출하여 정리해주세요. 마크다운은 제외해주세요.
    
    사업계획서 분석:
    {business_plan}
    
    미팅 분석:
    {meeting}
    
    다음 형식으로 KPI를 정리해주세요. 마크다운 문법을 사용하지 말고 일반 텍스트로 작성해주세요:
    
    ■ 추출된 핵심성과지표 (KPI)
    
    🔹 공통 KPI
    • 매출: [현재] → [목표] (목표년도)
    • 고용: [현재] → [목표] (목표년도)
    • 투자: [현재] → [목표] (목표년도)
    
    🔹 자율 시장검증 KPI
    1. PSF 설문조사: [목표 수치]명
    2. 가격검증: [목표 수치]명
    3. MAU: [목표 수치]명
    4. 리텐션율: [목표 수치]%
    5. LTV:CAC 비율: [목표 수치]배
    6. PMF Survey: [목표 수치]%
    7. 파트너십: [목표 수치]개 기관
    8. 기타 KPI: [추가 KPI들]
    
    정보가 명확하지 않은 경우는 표시하지 말아주세요,마크다운은 제외해주세요.
    """
    
    return await call_gpt(prompt)
