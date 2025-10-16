'use client';

import { useState } from 'react';
import { Copy, Download, FileText, BarChart3, Target, Users } from 'lucide-react';
import { AnalysisResponse } from '@/types';

interface AnalysisResultsProps {
  results: AnalysisResponse | null;
}

const AnalysisResults = ({ results }: AnalysisResultsProps) => {
  const [activeTab, setActiveTab] = useState<'extracted' | 'report'>('extracted');
  const [activeReportTab, setActiveReportTab] = useState<'growth' | 'kpi' | 'strategy'>('growth');

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      // TODO: 토스트 알림 추가
    } catch (err) {
      console.error('복사 실패:', err);
    }
  };

  const downloadReport = () => {
    if (!results) return;
    
    const currentDate = new Date().toLocaleDateString('ko-KR');
    let fullReport = `Station C 2025 AI 진단보고서\n`;
    fullReport += `생성일: ${currentDate}\n`;
    fullReport += `AI 분석 기반 자동생성 보고서\n`;
    fullReport += `${'='.repeat(60)}\n\n`;
    
    fullReport += `📄 사업계획서 분석 결과\n`;
    fullReport += `${'-'.repeat(40)}\n`;
    fullReport += `${results.business_plan_summary}\n\n`;
    
    fullReport += `🎤 미팅 분석 결과\n`;
    fullReport += `${'-'.repeat(40)}\n`;
    fullReport += `${results.meeting_summary}\n\n`;
    
    fullReport += `📊 추출된 KPI\n`;
    fullReport += `${'-'.repeat(40)}\n`;
    fullReport += `${results.extracted_kpis}\n\n`;
    
    fullReport += `${'='.repeat(60)}\n`;
    fullReport += `📋 자동생성 진단보고서\n`;
    fullReport += `${'='.repeat(60)}\n\n`;
    
    fullReport += `${results.reports.growth}\n\n`;
    fullReport += `${'-'.repeat(50)}\n\n`;
    fullReport += `${results.reports.kpi}\n\n`;
    fullReport += `${'-'.repeat(50)}\n\n`;
    fullReport += `${results.reports.strategy}\n`;
    
    const blob = new Blob([fullReport], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Station_C_AI진단보고서_${currentDate.replace(/\./g, '')}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  if (!results) {
    return (
      <div className="text-center py-12">
        <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <p className="text-gray-500 text-lg">AI 분석을 시작하면 결과가 여기에 표시됩니다.</p>
      </div>
    );
  }

  return (
    <div>
      {/* Tab Navigation */}
      <div className="flex mb-6">
        <button
          onClick={() => setActiveTab('extracted')}
          className={`tab ${activeTab === 'extracted' ? 'active' : ''}`}
        >
          추출된 정보
        </button>
        <button
          onClick={() => setActiveTab('report')}
          className={`tab ${activeTab === 'report' ? 'active' : ''}`}
        >
          생성된 보고서
        </button>
      </div>

      {/* Extracted Information Tab */}
      {activeTab === 'extracted' && (
        <div className="space-y-6">
          <div className="bg-primary-700 text-white rounded p-5">
            <h3 className="text-lg font-semibold mb-2 flex items-center">
              <FileText className="w-5 h-5 mr-2" />
              AI 추출 정보
            </h3>
            <p>업로드된 파일들에서 AI가 자동으로 추출한 핵심 정보입니다.</p>
          </div>

          <div className="space-y-4">
            <div className="bg-gray-50 rounded-lg p-4">
              <h4 className="font-semibold text-gray-700 mb-3 border-b border-gray-200 pb-2">
                사업계획서 요약
              </h4>
              <div className="text-gray-600 whitespace-pre-line">
                {results.business_plan_summary}
              </div>
            </div>

            <div className="bg-gray-50 rounded-lg p-4">
              <h4 className="font-semibold text-gray-700 mb-3 border-b border-gray-200 pb-2">
                미팅 핵심 내용
              </h4>
              <div className="text-gray-600 whitespace-pre-line">
                {results.meeting_summary}
              </div>
            </div>

            <div className="bg-gray-50 rounded-lg p-4">
              <h4 className="font-semibold text-gray-700 mb-3 border-b border-gray-200 pb-2">
                추출된 KPI
              </h4>
              <div className="text-gray-600 whitespace-pre-line">
                {results.extracted_kpis}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Report Tab */}
      {activeTab === 'report' && (
        <div className="space-y-6">
          <div className="bg-primary-700 text-white rounded p-5">
            <h3 className="text-lg font-semibold mb-2 flex items-center">
              <BarChart3 className="w-5 h-5 mr-2" />
              자동생성 보고서
            </h3>
            <p>Station C 양식에 맞게 자동으로 생성된 진단보고서입니다.</p>
          </div>

          {/* Report Tab Navigation */}
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setActiveReportTab('growth')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                activeReportTab === 'growth'
                  ? 'bg-primary-500 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              성장단계
            </button>
            <button
              onClick={() => setActiveReportTab('kpi')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                activeReportTab === 'kpi'
                  ? 'bg-primary-500 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              KPI
            </button>
            <button
              onClick={() => setActiveReportTab('strategy')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                activeReportTab === 'strategy'
                  ? 'bg-primary-500 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              종합 분석
            </button>
          </div>

          {/* Report Content */}
          <div className="bg-white border-2 border-gray-200 rounded-lg p-5">
            <div className="text-gray-700 whitespace-pre-line leading-relaxed">
              {results.reports[activeReportTab]}
            </div>
            <button
              onClick={() => copyToClipboard(results.reports[activeReportTab])}
              className="mt-4 bg-green-500 text-white px-4 py-2 rounded-lg text-sm hover:bg-green-600 transition-colors flex items-center space-x-2"
            >
              <Copy className="w-4 h-4" />
              <span>복사</span>
            </button>
          </div>

          {/* Download Full Report Button */}
          <button
            onClick={downloadReport}
            className="w-full btn bg-primary-500 hover:bg-primary-600 flex items-center justify-center space-x-2"
          >
            <Download className="w-4 h-4" />
            <span>전체 보고서 다운로드</span>
          </button>
        </div>
      )}
    </div>
  );
};

export default AnalysisResults;
