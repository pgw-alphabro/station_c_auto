export interface MentorInput {
  growth: string;
  kpi: string;
  strategy: string;
}

export interface AnalysisRequest {
  mentor_input: MentorInput;
  business_plan_files: string[];
  meeting_audio_files: string[];
}

export interface AnalysisResponse {
  business_plan_summary: string;
  meeting_summary: string;
  extracted_kpis: string;
  reports: {
    growth: string;
    kpi: string;
    strategy: string;
  };
}

export interface UploadedFile {
  file_id: string;
  filename: string;
  file_path: string;
}

export interface FileUpload {
  file: File;
  type: 'business-plan' | 'meeting-audio';
}
