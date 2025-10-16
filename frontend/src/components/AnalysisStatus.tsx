'use client';

import { useState } from 'react';
import { Play, CheckCircle, Clock, Loader } from 'lucide-react';

interface AnalysisStatusProps {
  isAnalyzing: boolean;
  onStartAnalysis: () => void;
}

const AnalysisStatus = ({ isAnalyzing, onStartAnalysis }: AnalysisStatusProps) => {
  const [progress, setProgress] = useState(0);

  const statusSteps = [
    { id: 'upload', label: '파일 업로드 대기중', icon: Clock },
    { id: 'extract', label: '내용 추출 대기중', icon: Clock },
    { id: 'analyze', label: 'AI 분석 대기중', icon: Clock },
    { id: 'generate', label: '보고서 생성 대기중', icon: Clock },
  ];

  const getStatusIcon = (stepId: string) => {
    if (isAnalyzing) {
      if (stepId === 'upload') return <CheckCircle className="w-5 h-5 text-green-500" />;
      if (stepId === 'extract' || stepId === 'analyze' || stepId === 'generate') {
        return <Loader className="w-5 h-5 text-blue-500 animate-spin" />;
      }
    }
    return <Clock className="w-5 h-5 text-yellow-500" />;
  };

  const getStatusText = (stepId: string) => {
    if (isAnalyzing) {
      if (stepId === 'upload') return '완료';
      if (stepId === 'extract' || stepId === 'analyze' || stepId === 'generate') {
        return '처리중';
      }
    }
    return '대기중';
  };

  return (
    <div className="bg-gray-50 rounded-xl p-5 my-5">
      <h3 className="text-lg font-semibold text-gray-700 mb-4">분석 진행상황</h3>
      
      {/* Progress Bar */}
      <div className="w-full bg-gray-200 rounded-full h-2 mb-4">
        <div 
          className="bg-gradient-to-r from-blue-500 to-green-500 h-2 rounded-full transition-all duration-300"
          style={{ width: `${isAnalyzing ? 75 : 0}%` }}
        />
      </div>
      
      {/* Status Steps */}
      <div className="space-y-3">
        {statusSteps.map((step) => (
          <div key={step.id} className="flex items-center space-x-3">
            {getStatusIcon(step.id)}
            <span className="text-sm text-gray-700">{step.label}</span>
            <span className="text-xs text-gray-500 ml-auto">
              {getStatusText(step.id)}
            </span>
          </div>
        ))}
      </div>
      
      {/* Start Analysis Button */}
      <button
        onClick={onStartAnalysis}
        disabled={isAnalyzing}
        className={`w-full mt-6 btn ${isAnalyzing ? 'opacity-50 cursor-not-allowed' : ''}`}
      >
        {isAnalyzing ? (
          <div className="flex items-center justify-center space-x-2">
            <Loader className="w-4 h-4 animate-spin" />
            <span>AI 분석 진행중...</span>
          </div>
        ) : (
          <div className="flex items-center justify-center space-x-2">
            <Play className="w-4 h-4" />
            <span>AI 분석 시작 (데모)</span>
          </div>
        )}
      </button>
    </div>
  );
};

export default AnalysisStatus;
