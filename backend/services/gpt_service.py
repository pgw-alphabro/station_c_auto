import openai
from config import OPENAI_API_KEY

async def call_gpt(prompt: str) -> str:
    """GPT API 호출"""
    try:
        print(f"🔍 GPT API 호출 시작 - 프롬프트 길이: {len(prompt)}")
        client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "당신은 Station C 진단보고서 전문가입니다. 제공된 정보를 정확히 분석하고, 추측이나 가정 없이 실제 데이터만을 바탕으로 진단보고서를 작성해주세요. 정보가 명확하지 않은 경우 '정보 없음'으로 표시하세요."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=16000,
            temperature=0.3
        )
        print(f"✅ GPT API 호출 성공")
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ GPT API 오류: {str(e)}")
        return f"GPT 분석 중 오류가 발생했습니다: {str(e)}"