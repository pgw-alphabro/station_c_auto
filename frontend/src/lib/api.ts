import axios from 'axios';
import { AnalysisRequest, AnalysisResponse, UploadedFile } from '@/types';

const API_BASE_URL = 'http://localhost:8002';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadBusinessPlan = async (file: File): Promise<UploadedFile> => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/upload/business-plan', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const uploadMeetingAudio = async (file: File): Promise<UploadedFile> => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/upload/meeting-audio', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const analyzeDocuments = async (request: AnalysisRequest): Promise<AnalysisResponse> => {
  const response = await api.post('/analyze', request);
  return response.data;
};
