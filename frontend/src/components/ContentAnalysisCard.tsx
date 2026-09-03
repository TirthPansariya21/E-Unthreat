import React from 'react';
import { Cpu, AlertTriangle, ShieldCheck } from 'lucide-react';

interface ContentAnalysisCardProps {
  label: string;
  confidencePct: number;
  modelName?: string;
  verdict: 'Phishing' | 'Suspicious' | 'Legitimate';
}

export const ContentAnalysisCard: React.FC<ContentAnalysisCardProps> = ({
  label,
  confidencePct,
  modelName = 'TF-IDF + Logistic Regression',
  verdict,
}) => {
  const isPhish = label.toLowerCase() === 'phishing' || verdict === 'Phishing';
  const isSus = label.toLowerCase() === 'suspicious' || verdict === 'Suspicious';

  const labelColor = isPhish ? 'text-red-400' : isSus ? 'text-amber-400' : 'text-emerald-400';
  const barGradient = isPhish
    ? 'bg-gradient-to-r from-red-600 to-red-400 shadow-danger-glow'
    : isSus
    ? 'bg-gradient-to-r from-amber-600 to-amber-400 shadow-warning-glow'
    : 'bg-gradient-to-r from-emerald-600 to-emerald-400 shadow-success-glow';

  return (
    <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl p-5 flex flex-col justify-between h-full relative overflow-hidden">
      <div>
        <div className="flex items-center gap-2 mb-4">
          <Cpu className="w-4 h-4 text-cyber-cyan" />
          <h3 className="text-xs font-bold uppercase tracking-wider text-cyber-muted">
            CONTENT ANALYSIS (ML)
          </h3>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 items-center">
          {/* Left Column: Metrics */}
          <div className="space-y-3.5">
            <div>
              <span className="text-[11px] font-bold uppercase tracking-wider text-cyber-muted block mb-0.5">
                ML CLASSIFIER
              </span>
              <p className={`text-xl font-extrabold tracking-tight ${labelColor}`}>
                {label || (isPhish ? 'Phishing' : 'Legitimate')}
              </p>
            </div>

            <div>
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-[11px] font-bold uppercase tracking-wider text-cyber-muted">
                  CONFIDENCE SCORE
                </span>
                <span className="text-xs font-mono font-bold text-white">{confidencePct}%</span>
              </div>
              {/* Animated Progress Bar */}
              <div className="w-full h-2 rounded-full bg-[#1E2D4A] overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-1000 ease-out ${barGradient}`}
                  style={{ width: `${Math.max(5, Math.min(100, confidencePct))}%` }}
                />
              </div>
            </div>

            <div>
              <span className="text-[11px] font-bold uppercase tracking-wider text-cyber-muted block mb-0.5">
                MODEL USED
              </span>
              <p className="text-xs font-semibold text-cyber-text-secondary">{modelName}</p>
            </div>
          </div>

          {/* Right Column: Holographic Cyber Envelope Illustration */}
          <div className="flex items-center justify-center p-2 relative">
            <div className="relative w-36 h-28 flex items-center justify-center">
              {/* Background glowing polygon mesh */}
              <svg className="absolute inset-0 w-full h-full opacity-30" viewBox="0 0 140 100">
                <polygon points="10,10 70,5 130,10 135,90 70,95 5,90" fill="none" stroke="#38BDF8" strokeWidth="0.8" strokeDasharray="3 3" />
                <line x1="10" y1="10" x2="70" y2="55" stroke="#38BDF8" strokeWidth="0.6" />
                <line x1="130" y1="10" x2="70" y2="55" stroke="#38BDF8" strokeWidth="0.6" />
                <line x1="5" y1="90" x2="70" y2="55" stroke="#38BDF8" strokeWidth="0.6" />
                <line x1="135" y1="90" x2="70" y2="55" stroke="#38BDF8" strokeWidth="0.6" />
              </svg>

              {/* Envelope Body */}
              <div
                className={`w-28 h-20 rounded-xl border flex items-center justify-center relative shadow-2xl transition-transform hover:scale-105 ${
                  isPhish
                    ? 'bg-gradient-to-b from-red-950/50 to-blue-950/40 border-red-500/50 shadow-danger-glow'
                    : 'bg-gradient-to-b from-emerald-950/50 to-blue-950/40 border-emerald-500/50 shadow-success-glow'
                }`}
              >
                {/* Envelope Flap Lines */}
                <svg className="absolute inset-0 w-full h-full" viewBox="0 0 112 80">
                  <path
                    d="M 4 4 L 56 42 L 108 4"
                    fill="none"
                    stroke={isPhish ? '#EF4444' : '#10B981'}
                    strokeWidth="1.5"
                    strokeOpacity="0.8"
                  />
                </svg>

                {/* Center Warning or Check Symbol */}
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center z-10 ${
                    isPhish
                      ? 'bg-red-500/20 text-red-400 border border-red-500/60 shadow-lg animate-pulse'
                      : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/60 shadow-lg'
                  }`}
                >
                  {isPhish ? (
                    <AlertTriangle className="w-5 h-5 fill-red-500/20" />
                  ) : (
                    <ShieldCheck className="w-5 h-5" />
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
