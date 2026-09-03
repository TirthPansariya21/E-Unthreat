import React from 'react';
import { ShieldAlert, ShieldCheck, AlertTriangle } from 'lucide-react';
import type { ThreatVerdict } from '../types/threat';

interface ThreatVerdictCardProps {
  verdict: ThreatVerdict;
  copy: string;
  badge?: string;
  levelLabel?: string;
}

export const ThreatVerdictCard: React.FC<ThreatVerdictCardProps> = ({
  verdict,
  copy,
  badge,
  levelLabel,
}) => {
  const isPhish = verdict === 'Phishing';
  const isSus = verdict === 'Suspicious';

  const colorConfig = isPhish
    ? {
        border: 'border-red-500/40',
        bg: 'bg-gradient-to-r from-red-950/40 via-[#0F1626] to-[#0F1626]',
        glow: 'shadow-danger-glow',
        badgeBorder: 'border-red-500/50',
        badgeBg: 'bg-red-500/10',
        badgeText: 'text-red-400',
        iconBg: 'bg-red-500/15 border-red-500/30 text-red-400',
        titleColor: 'text-red-400',
        labelColor: 'text-red-400',
        icon: ShieldAlert,
        defaultBadge: 'CRITICAL',
        defaultLabel: 'High Risk',
        headline: 'PHISHING',
      }
    : isSus
    ? {
        border: 'border-amber-500/40',
        bg: 'bg-gradient-to-r from-amber-950/40 via-[#0F1626] to-[#0F1626]',
        glow: 'shadow-warning-glow',
        badgeBorder: 'border-amber-500/50',
        badgeBg: 'bg-amber-500/10',
        badgeText: 'text-amber-400',
        iconBg: 'bg-amber-500/15 border-amber-500/30 text-amber-400',
        titleColor: 'text-amber-400',
        labelColor: 'text-amber-400',
        icon: AlertTriangle,
        defaultBadge: 'SUSPICIOUS',
        defaultLabel: 'Medium Risk',
        headline: 'SUSPICIOUS EMAIL',
      }
    : {
        border: 'border-emerald-500/40',
        bg: 'bg-gradient-to-r from-emerald-950/40 via-[#0F1626] to-[#0F1626]',
        glow: 'shadow-success-glow',
        badgeBorder: 'border-emerald-500/50',
        badgeBg: 'bg-emerald-500/10',
        badgeText: 'text-emerald-400',
        iconBg: 'bg-emerald-500/15 border-emerald-500/30 text-emerald-400',
        titleColor: 'text-emerald-400',
        labelColor: 'text-emerald-400',
        icon: ShieldCheck,
        defaultBadge: 'VERIFIED',
        defaultLabel: 'Low Risk',
        headline: 'LEGITIMATE EMAIL',
      };

  const Icon = colorConfig.icon;

  return (
    <div
      className={`rounded-2xl p-5 border ${colorConfig.border} ${colorConfig.bg} ${colorConfig.glow} flex flex-col sm:flex-row sm:items-center justify-between gap-4 transition-all duration-300 relative overflow-hidden`}
    >
      {/* Glow highlight line */}
      <div className={`absolute top-0 left-0 right-0 h-[2px] ${isPhish ? 'bg-gradient-to-r from-red-500 to-transparent' : isSus ? 'bg-gradient-to-r from-amber-500 to-transparent' : 'bg-gradient-to-r from-emerald-500 to-transparent'}`} />

      <div className="flex items-start gap-4">
        <div
          className={`w-14 h-14 rounded-2xl border ${colorConfig.iconBg} flex items-center justify-center shrink-0 shadow-lg`}
        >
          <Icon className="w-7 h-7" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <span className={`text-[11px] font-bold tracking-wider uppercase ${colorConfig.labelColor}`}>
              THREAT DETECTED
            </span>
          </div>
          <h2 className={`text-2xl lg:text-3xl font-black tracking-tight mt-0.5 ${colorConfig.titleColor}`}>
            {colorConfig.headline}
          </h2>
          <p className="text-xs lg:text-sm text-cyber-text-secondary mt-1 max-w-xl leading-relaxed">
            {copy}
          </p>
        </div>
      </div>

      {/* Risk Badge */}
      <div className="sm:text-right shrink-0">
        <div
          className={`inline-block px-3 py-1 rounded-lg border ${colorConfig.badgeBorder} ${colorConfig.badgeBg} ${colorConfig.badgeText} text-xs font-bold tracking-wider`}
        >
          {badge || colorConfig.defaultBadge}
        </div>
        <p className={`text-xs font-semibold mt-1 ${colorConfig.labelColor}`}>
          {levelLabel || colorConfig.defaultLabel}
        </p>
      </div>
    </div>
  );
};
