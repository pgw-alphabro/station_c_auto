'use client';

import { MentorInput as MentorInputType } from '@/types';

interface MentorInputProps {
  mentorInput: MentorInputType;
  onMentorInputChange: (input: MentorInputType) => void;
}

const MentorInput = ({ mentorInput, onMentorInputChange }: MentorInputProps) => {
  const handleChange = (field: keyof MentorInputType, value: string) => {
    onMentorInputChange({
      ...mentorInput,
      [field]: value
    });
  };

  return (
    <div className="mentor-input-section">
      <h3 className="text-orange-700 text-xl font-semibold mb-4 flex items-center">
        📝 멘토 의견 입력
      </h3>
      <p className="text-orange-700 mb-4">
        미팅 중 작성한 멘토 의견을 각 영역별로 입력해주세요.
      </p>
      
      <div className="space-y-4">
        <div>
          <label className="block text-orange-700 font-semibold mb-2">
            1. 성장단계 관련 의견
          </label>
          <textarea
            value={mentorInput.growth}
            onChange={(e) => handleChange('growth', e.target.value)}
            className="mentor-textarea"
            placeholder="예: 현재 MVP 완료 단계이며, 베타 테스터 확보 상태를 고려할 때 PMF 단계가 적합합니다. 다만 의료기관 파트너십 확대가 필요합니다."
          />
        </div>
        
        <div>
          <label className="block text-orange-700 font-semibold mb-2">
            2. KPI 관련 의견
          </label>
          <textarea
            value={mentorInput.kpi}
            onChange={(e) => handleChange('kpi', e.target.value)}
            className="mentor-textarea"
            placeholder="예: PSF 설문조사 목표를 100명에서 200명으로 상향 조정이 필요합니다. MAU 목표도 15,000명으로 조정하는 것이 현실적입니다."
          />
        </div>
        
        <div>
          <label className="block text-orange-700 font-semibold mb-2">
            3. 전략 관련 의견
          </label>
          <textarea
            value={mentorInput.strategy}
            onChange={(e) => handleChange('strategy', e.target.value)}
            className="mentor-textarea"
            placeholder="예: 의료기관 파트너십 확대 전략이 효과적입니다. 다만 데이터 보안 강화에 더 많은 예산 배정이 필요합니다."
          />
        </div>
        
      </div>
    </div>
  );
};

export default MentorInput;
