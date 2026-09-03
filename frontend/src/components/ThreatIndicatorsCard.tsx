import React from 'react';
import { ShieldAlert, AlertTriangle, Key, AlertCircle, AlertOctagon, CheckCircle2 } from 'lucide-react';
import type { ThreatIndicator } from '../types/threat';

interface ThreatIndicatorsCardProps {
  indicators: ThreatIndicator[];
}

export const ThreatIndicatorsCard: React.FC<ThreatIndicatorsCardProps> = ({ indicators }) => {
  const getIconForIndicator = (name: string) => {
    const n = name.toLowerCase();
    if (n.includes('credential') || n.includes('password') || n.includes('login')) {
      return Key;
    }
    if (n.includes('urgency') || n.includes('pressure') || n.includes('activity')) {
      return AlertCircle;
    }
    if (n.includes('auth') || n.includes('spf') || n.includes('dkim') || n.includes('dmarc')) {
      return AlertTriangle;
    }
    if (n.includes('domain') || n.includes('lookalike') || n.includes('spoof')) {
      return ShieldAlert;
    }
    return AlertOctagon;
  };

  const getSeverityBadge = (severity: string) => {
    const s = severity.toUpperCase();
    if (s === 'HIGH' || s === 'CRITICAL') {
      return {
        bg: 'bg-red-500/10 text-red-400 border border-red-500/30',
        label: 'HIGH',
      };
    }
    if (s === 'MEDIUM' || s === 'WARNING') {
      return {
        bg: 'bg-amber-500/10 text-amber-400 border border-amber-500/30',
        label: 'MEDIUM',
      };
    }
    return {
      bg: 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30',
      label: 'LOW',
    };
  };

  return (
    <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl p-5 flex flex-col justify-between h-full">
      <div>
        <h3 className="text-xs font-bold uppercase tracking-wider text-cyber-muted mb-3.5 flex items-center gap-2">
          <ShieldAlert className="w-3.5 h-3.5 text-cyber-danger" />
          THREAT INDICATORS
        </h3>

        <div className="space-y-2.5">
          {indicators.length === 0 ? (
            <div className="flex items-center gap-2 text-xs text-emerald-400 py-3">
              <CheckCircle2 className="w-4 h-4" />
              <span>No critical threat indicators detected in message.</span>
            </div>
          ) : (
            indicators.slice(0, 6).map((item, idx) => {
              const Icon = getIconForIndicator(item.name);
              const badge = getSeverityBadge(item.severity);
              return (
                <div
                  key={idx}
                  className="flex items-center justify-between gap-3 p-2 rounded-xl bg-[#090D16]/70 border border-[#1E2D4A]/50 hover:border-cyber-border-hover transition-colors"
                >
                  <div className="flex items-center gap-2.5 min-w-0">
                    <Icon className="w-4 h-4 text-cyber-muted shrink-0" />
                    <span className="text-xs font-semibold text-cyber-text truncate" title={item.name}>
                      {item.name}
                    </span>
                  </div>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded shrink-0 ${badge.bg}`}>
                    {badge.label}
                  </span>
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
};
