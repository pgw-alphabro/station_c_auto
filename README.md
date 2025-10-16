# Station C 2025 AI 진단보고서 시스템

AI 기반 자동 진단보고서 생성 시스템입니다. Next.js 프론트엔드와 FastAPI 백엔드를 사용하여 구현되었습니다.

## 프로젝트 구조

```
station_c_auto/
├── frontend/          # Next.js 프론트엔드
│   ├── src/
│   │   ├── app/       # App Router
│   │   ├── components/ # React 컴포넌트
│   │   ├── lib/       # 유틸리티 함수
│   │   └── types/     # TypeScript 타입 정의
│   └── package.json
├── backend/           # FastAPI 백엔드
│   ├── main.py        # 메인 API 서버
│   ├── config.py      # 설정 파일
│   └── requirements.txt
└── README.md
```

## 주요 기능

1. **파일 업로드**
   - 사업계획서 (PDF, Word, PowerPoint)
   - 미팅 오디오 (MP3, WAV, M4A)

2. **멘토 입력**
   - 성장단계, KPI, 전략, 경영진단 영역별 의견 입력
   - 멘토 입력에 가중치 적용

3. **AI 분석**
   - OCR을 통한 사업계획서 텍스트 추출
   - STT를 통한 오디오 텍스트 변환
   - GPT를 통한 내용 분석 및 보고서 생성

4. **보고서 생성**
   - 성장단계 진단
   - KPI 분석
   - 전략 수립
   - 경영진단

## 설치 및 실행

### 백엔드 실행

```bash
cd backend
pip install -r requirements.txt
python main.py
```

백엔드는 `http://localhost:8000`에서 실행됩니다.

### 프론트엔드 실행

```bash
cd frontend
npm install
npm run dev
```

프론트엔드는 `http://localhost:3000`에서 실행됩니다.

## API 엔드포인트

- `POST /upload/business-plan` - 사업계획서 업로드
- `POST /upload/meeting-audio` - 미팅 오디오 업로드
- `POST /analyze` - 문서 분석 및 보고서 생성

## 환경 변수

백엔드에서 사용하는 환경 변수:
- `OPENAI_API_KEY`: OpenAI API 키

## 기술 스택

### 프론트엔드
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- React Dropzone
- Axios

### 백엔드
- FastAPI
- OpenAI GPT-4
- Python-multipart
- Pydantic
- aiofiles

## 개발 상태

- [x] 프로젝트 구조 설정
- [x] 기본 UI 컴포넌트 구현
- [x] 파일 업로드 기능
- [x] 멘토 입력 폼
- [x] 분석 상태 표시
- [x] 결과 표시 UI
- [ ] OCR 기능 통합
- [ ] STT 기능 통합
- [ ] GPT API 연동
- [ ] 실제 파일 처리 로직
