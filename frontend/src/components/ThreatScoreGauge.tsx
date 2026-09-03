import React from 'react';

interface ThreatScoreGaugeProps {
  score: number;
  verdict: 'Phishing' | 'Suspicious' | 'Legitimate';
}

export const ThreatScoreGauge: React.FC<ThreatScoreGaugeProps> = ({ score, verdict }) => {
  // Score clamped 0-100
  const clampedScore = Math.max(0, Math.min(100, score));

  // Determine color and status
  const isHigh = clampedScore >= 61 || verdict === 'Phishing';
  const isMedium = (clampedScore >= 31 && clampedScore <= 60) || verdict === 'Suspicious';

  const strokeColor = isHigh ? '#EF4444' : isMedium ? '#F59E0B' : '#10B981';

  const riskLabel = isHigh ? 'CRITICAL RISK' : isMedium ? 'ELEVATED RISK' : 'LOW RISK';
  const labelColor = isHigh ? 'text-red-400' : isMedium ? 'text-amber-400' : 'text-emerald-400';

  // SVG Gauge calculations
  // Semicircle radius = 80, circumference = PI * 80 ~= 251.32
  const radius = 80;
  const circumference = Math.PI * radius;
  const strokeDashoffset = circumference - (clampedScore / 100) * circumference;

  return (
    <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl p-5 flex flex-col justify-between h-full relative overflow-hidden">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-xs font-bold uppercase tracking-wider text-cyber-muted">
          THREAT SCORE
        </h3>
      </div>

      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 my-auto">
        {/* Semicircle Gauge Visual */}
        <div className="relative flex flex-col items-center justify-center">
          <svg className="w-48 h-28 overflow-visible" viewBox="0 0 200 115">
            <defs>
              <filter id="gauge-glow" x="-20%" y="-20%" width="140%" height="140%">
                <feDropShadow dx="0" dy="0" stdDeviation="4" floodColor={strokeColor} floodOpacity="0.6" />
              </filter>
            </defs>

            {/* Background Arc */}
            <path
              d="M 20 100 A 80 80 0 0 1 180 100"
              fill="none"
              stroke="#1E2D4A"
              strokeWidth="14"
              strokeLinecap="round"
            />

            {/* Animated Value Arc */}
            <path
              d="M 20 100 A 80 80 0 0 1 180 100"
              fill="none"
              stroke={strokeColor}
              strokeWidth="14"
              strokeLinecap="round"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              filter="url(#gauge-glow)"
              className="transition-all duration-1000 ease-out"
            />
          </svg>

          {/* Centered Score Text */}
          <div className="absolute top-12 flex flex-col items-center">
            <div className="flex items-baseline gap-1">
              <span className="text-3xl font-black text-white font-mono">{clampedScore}</span>
              <span className="text-xs font-semibold text-cyber-muted">/100</span>
            </div>
            <span className={`text-[11px] font-extrabold tracking-wider uppercase mt-0.5 ${labelColor}`}>
              {riskLabel}
            </span>
          </div>

          {/* Min & Max Labels */}
          <div className="w-48 flex justify-between px-2 text-[10px] font-mono text-cyber-muted mt-1">
            <span>0</span>
            <span>100</span>
          </div>
        </div>

        {/* Legend */}
        <div className="flex flex-col gap-2.5 text-xs text-cyber-text-secondary pr-2">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400" />
            <span className="font-mono text-cyber-muted">0 - 30</span>
            <span className="text-cyber-text-secondary ml-1">Low Risk</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-amber-400" />
            <span className="font-mono text-cyber-muted">31 - 60</span>
            <span className="text-cyber-text-secondary ml-1">Medium Risk</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-red-400" />
            <span className="font-mono text-cyber-muted">61 - 100</span>
            <span className="text-cyber-text-secondary ml-1 font-semibold text-white">High Risk</span>
          </div>
        </div>
      </div>
    </div>
  );
};
