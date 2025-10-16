from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import aiofiles
import asyncio
from typing import List
import tempfile
import shutil

# 모델 임포트
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from models.schemas import MentorInput, AnalysisRequest, AnalysisResponse, UploadedFile

# 서비스 임포트
from services.business_plan_analyzer import analyze_business_plan
from services.meeting_analyzer import analyze_meeting_audio
from services.kpi_extractor import extract_kpis
from services.report_generator import generate_reports

app = FastAPI(title="Station C AI 진단보고서 API", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vercel에서는 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Vercel에서 임시 디렉토리 사용
UPLOAD_DIR = tempfile.mkdtemp()

@app.get("/")
async def root():
    return {"message": "Station C AI 진단보고서 API"}

@app.post("/upload/business-plan", response_model=UploadedFile)
async def upload_business_plan(file: UploadFile = File(...)):
    """사업계획서 파일 업로드"""
    try:
        # 파일 ID 생성
        file_id = str(uuid.uuid4())
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else ''
        filename = f"business_plan_{file_id}.{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # 파일 저장
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        return UploadedFile(
            file_id=file_id,
            filename=filename,
            file_path=filename  # Vercel에서는 상대 경로 사용
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 업로드 실패: {str(e)}")

@app.post("/upload/meeting-audio", response_model=UploadedFile)
async def upload_meeting_audio(file: UploadFile = File(...)):
    """미팅 오디오 파일 업로드"""
    try:
        # 파일 ID 생성
        file_id = str(uuid.uuid4())
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else ''
        filename = f"meeting_audio_{file_id}.{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # 파일 저장
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        return UploadedFile(
            file_id=file_id,
            filename=filename,
            file_path=filename  # Vercel에서는 상대 경로 사용
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 업로드 실패: {str(e)}")

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_documents(request: AnalysisRequest):
    """문서 분석 및 보고서 생성"""
    try:
        # 1. 사업계획서 분석과 미팅 오디오 분석을 비동기로 동시 처리
        business_plan_task = None
        meeting_task = None
        
        if request.business_plan_files:
            business_plan_task = analyze_business_plan(request.business_plan_files, UPLOAD_DIR)
        
        if request.meeting_audio_files:
            meeting_task = analyze_meeting_audio(request.meeting_audio_files, UPLOAD_DIR)
        
        # 비동기로 동시 실행
        tasks = []
        if business_plan_task:
            tasks.append(business_plan_task)
        if meeting_task:
            tasks.append(meeting_task)
        
        if tasks:
            results = await asyncio.gather(*tasks)
            business_plan_summary = results[0] if business_plan_task else ""
            meeting_summary = results[1] if meeting_task else (results[0] if not business_plan_task else "")
        else:
            business_plan_summary = ""
            meeting_summary = ""
        
        # 2. KPI 추출
        extracted_kpis = await extract_kpis(business_plan_summary, meeting_summary)
        
        # 3. 보고서 생성 (멘토 입력 가중치 적용)
        reports = await generate_reports(
            business_plan_summary, 
            meeting_summary, 
            extracted_kpis, 
            request.mentor_input
        )
        
        return AnalysisResponse(
            business_plan_summary=business_plan_summary,
            meeting_summary=meeting_summary,
            extracted_kpis=extracted_kpis,
            reports=reports
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 실패: {str(e)}")

# Vercel Functions 핸들러
def handler(request):
    return app(request.scope, request.receive, request.send)
