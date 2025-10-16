from pydantic import BaseModel
from typing import List

class MentorInput(BaseModel):
    growth: str
    kpi: str
    strategy: str

class AnalysisRequest(BaseModel):
    mentor_input: MentorInput
    business_plan_files: List[str] = []
    meeting_audio_files: List[str] = []

class AnalysisResponse(BaseModel):
    business_plan_summary: str
    meeting_summary: str
    extracted_kpis: str
    reports: dict

class UploadedFile(BaseModel):
    file_id: str
    filename: str
    file_path: str
