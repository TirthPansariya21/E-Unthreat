import React from 'react';
import { Download, Moon, Sun } from 'lucide-react';

interface TopHeaderProps {
  onDownloadReport?: () => void;
  isReportAvailable?: boolean;
}

export const TopHeader: React.FC<TopHeaderProps> = ({
  onDownloadReport,
  isReportAvailable = true,
}) => {
  const [isDark, setIsDark] = React.useState(true);

  return (
    <header className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-6 mb-2">
      {/* Title & Subtitle */}
      <div>
        <h1 className="text-2xl lg:text-[26px] font-extrabold text-white tracking-tight">
          Email Threat Analysis
        </h1>
        <p className="text-xs lg:text-sm text-cyber-text-secondary mt-1 max-w-2xl">
          Analyze suspicious emails and get comprehensive threat intelligence, authentication results, and forensic insights.
        </p>
      </div>

      {/* Top Controls */}
      <div className="flex items-center gap-3 shrink-0">
        {/* System Operational Badge */}
        <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          <span>System Operational</span>
        </div>

        {/* Theme Toggle */}
        <button
          onClick={() => setIsDark(!isDark)}
          title="Toggle Theme"
          className="w-9 h-9 rounded-xl bg-[#0F1626] border border-[#1E2D4A] flex items-center justify-center text-cyber-text-secondary hover:text-white hover:border-cyber-cyan/40 transition-colors"
        >
          {isDark ? <Moon className="w-4 h-4" /> : <Sun className="w-4 h-4" />}
        </button>

        {/* User Profile Avatar */}
        <div className="w-9 h-9 rounded-xl bg-blue-600/30 border border-blue-500/50 flex items-center justify-center text-xs font-bold text-cyber-cyan shadow-cyan-glow">
          AD
        </div>

        {/* Download Report Button */}
        <button
          onClick={onDownloadReport}
          disabled={!isReportAvailable}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all duration-200 border ${
            isReportAvailable
              ? 'bg-[#121B30] hover:bg-blue-600/20 text-white border-blue-500/40 hover:border-cyber-cyan shadow-sm hover:shadow-cyan-glow cursor-pointer'
              : 'bg-[#0F1626] text-cyber-muted border-[#1E2D4A] cursor-not-allowed opacity-60'
          }`}
        >
          <Download className="w-3.5 h-3.5 text-cyber-cyan" />
          <span>Download Report</span>
        </button>
      </div>
    </header>
  );
};
