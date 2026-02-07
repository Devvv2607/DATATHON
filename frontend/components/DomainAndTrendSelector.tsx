'use client';

import DomainSelector from './DomainSelector';
import { useDomain } from '@/contexts/DomainContext';

export default function DomainAndTrendSelector() {
  const { selectedDomain, setSelectedDomain, selectedTrend, setSelectedTrend } = useDomain();

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <DomainSelector value={selectedDomain} onChange={setSelectedDomain} />
      
      {/* Trend Selector */}
      <div className="glass-card p-4 rounded-xl">
        <label className="text-sm text-gray-400 mb-2 block">Select Trend</label>
        <select
          value={selectedTrend}
          onChange={(e) => setSelectedTrend(e.target.value)}
          className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
        >
          <option value="trend_1">#AIRevolution2026</option>
          <option value="trend_2">#SustainableFashion</option>
          <option value="trend_3">#MetaverseLife</option>
          <option value="trend_4">#CryptoRecovery</option>
          <option value="trend_5">#RemoteWork</option>
          <option value="trend_6">#HealthTech</option>
          <option value="trend_7">#GenZMarketing</option>
          <option value="trend_8">#ClimateAction</option>
          <option value="trend_9">#WebThreeDev</option>
          <option value="trend_10">#MindfulLiving</option>
        </select>
      </div>
    </div>
  );
}
