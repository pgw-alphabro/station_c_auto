'use client';

import { useState } from 'react';
import FileUpload from '@/components/FileUpload';
import MentorInput from '@/components/MentorInput';
import AnalysisStatus from '@/components/AnalysisStatus';
import AnalysisResults from '@/components/AnalysisResults';
import { MentorInput as MentorInputType, AnalysisResponse } from '@/types';

export default function Home() {
  const [uploadedFiles, setUploadedFiles] = useState<{
    businessPlan: File[];
    meetingAudio: File[];
  }>({
    businessPlan: [],
    meetingAudio: []
  });

  const [mentorInput, setMentorInput] = useState<MentorInputType>({
    growth: '',
    kpi: '',
    strategy: ''
  });

  const [analysisResults, setAnalysisResults] = useState<AnalysisResponse | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleFileUpload = (files: File[], type: 'business-plan' | 'meeting-audio') => {
    if (type === 'business-plan') {
      setUploadedFiles(prev => ({
        ...prev,
        businessPlan: [...prev.businessPlan, ...files]
      }));
    } else {
      setUploadedFiles(prev => ({
        ...prev,
        meetingAudio: [...prev.meetingAudio, ...files]
      }));
    }
  };

  const handleRemoveFile = (index: number, type: 'business-plan' | 'meeting-audio') => {
    if (type === 'business-plan') {
      setUploadedFiles(prev => ({
        ...prev,
        businessPlan: prev.businessPlan.filter((_, i) => i !== index)
      }));
    } else {
      setUploadedFiles(prev => ({
        ...prev,
        meetingAudio: prev.meetingAudio.filter((_, i) => i !== index)
      }));
    }
  };

  const handleStartAnalysis = async () => {
    setIsAnalyzing(true);
    
    try {
      // 실제 API 호출
      const { analyzeDocuments } = await import('@/lib/api');
      
      const request = {
        mentor_input: mentorInput,
        business_plan_files: uploadedFiles.businessPlan.map(f => f.name),
        meeting_audio_files: uploadedFiles.meetingAudio.map(f => f.name)
      };
      
      const results = await analyzeDocuments(request);
      setAnalysisResults(results);
    } catch (error) {
      console.error('분석 중 오류 발생:', error);
      // 오류 발생 시 에러 메시지 표시
      setAnalysisResults({
        business_plan_summary: `API 연결 오류: ${error}`,
        meeting_summary: `API 연결 오류: ${error}`,
        extracted_kpis: `API 연결 오류: ${error}`,
        reports: {
          growth: `API 연결 오류: ${error}`,
          kpi: `API 연결 오류: ${error}`,
          strategy: `API 연결 오류: ${error}`,
          management: `API 연결 오류: ${error}`
        }
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-primary-50">
      <div className="max-w-7xl mx-auto bg-white rounded shadow-sm border border-gray-200">
        {/* Header */}
        <div className="bg-primary-700 text-white p-8 text-center">
          <h1 className="text-4xl font-bold mb-2">Station C 2025 AI 진단보고서</h1>
          <p className="text-xl opacity-90">AI 기반 자동 진단보고서 생성 시스템 (데모 버전)</p>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-2 min-h-screen">
          {/* Upload Section */}
          <div className="bg-primary-50 p-10 border-r border-gray-200">
            <h2 className="text-2xl font-semibold text-primary-700 mb-6 border-b border-gray-300 pb-3">
              파일 업로드
            </h2>
            
            <FileUpload
              type="business-plan"
              files={uploadedFiles.businessPlan}
              onFileUpload={handleFileUpload}
              onRemoveFile={handleRemoveFile}
            />
            
            <FileUpload
              type="meeting-audio"
              files={uploadedFiles.meetingAudio}
              onFileUpload={handleFileUpload}
              onRemoveFile={handleRemoveFile}
            />

            <MentorInput
              mentorInput={mentorInput}
              onMentorInputChange={setMentorInput}
            />

            <AnalysisStatus
              isAnalyzing={isAnalyzing}
              onStartAnalysis={handleStartAnalysis}
            />
          </div>

          {/* Analysis Section */}
          <div className="bg-white p-10">
            <h2 className="text-2xl font-semibold text-primary-700 mb-6 border-b border-gray-300 pb-3">
              분석 결과
            </h2>
            
            <AnalysisResults results={analysisResults} />
          </div>
        </div>
      </div>
    </div>
  );
}