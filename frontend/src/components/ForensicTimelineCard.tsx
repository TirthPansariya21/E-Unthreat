import React from 'react';
import { Radio } from 'lucide-react';
import type { TimelineStep } from '../types/threat';

interface ForensicTimelineCardProps {
  timeline: TimelineStep[];
}

export const ForensicTimelineCard: React.FC<ForensicTimelineCardProps> = ({ timeline }) => {
  // Default mock timeline if empty
  const displayTimeline: TimelineStep[] =
    timeline && timeline.length > 0
      ? timeline
      : [
          {
            step: 'Email Sent',
            host: 'Originating Mail Server',
            role: 'Origin Server',
            timestamp: '10:23:58 AM',
          },
          {
            step: 'Relay',
            host: 'Intermediate Gateway',
            role: 'MTA Relay',
            timestamp: '10:24:01 AM',
          },
          {
            step: 'Delivered',
            host: 'Recipient Mail Server',
            role: 'Destination MX',
            timestamp: '10:24:04 AM',
          },
        ];

  return (
    <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl p-5 flex flex-col justify-between h-full">
      <div>
        <h3 className="text-xs font-bold uppercase tracking-wider text-cyber-muted mb-4 flex items-center gap-2">
          <Radio className="w-3.5 h-3.5 text-cyber-cyan" />
          FORENSIC TIMELINE
        </h3>

        {/* Vertical Timeline */}
        <div className="relative pl-6 space-y-4">
          {/* Vertical continuous line */}
          <div className="absolute top-2 bottom-2 left-[9px] w-[2px] bg-gradient-to-b from-red-500 via-amber-500 to-emerald-500 opacity-40" />

          {displayTimeline.map((item, idx) => {
            const isFirst = idx === 0;
            const isLast = idx === displayTimeline.length - 1;

            const dotColor = isFirst
              ? 'bg-red-500 border-red-400 shadow-danger-glow'
              : isLast
              ? 'bg-emerald-500 border-emerald-400 shadow-success-glow'
              : 'bg-amber-500 border-amber-400';

            return (
              <div key={idx} className="relative flex items-start justify-between gap-2">
                {/* Timeline Dot */}
                <div
                  className={`absolute -left-6 top-1 w-2.5 h-2.5 rounded-full border ${dotColor} z-10`}
                />

                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-1.5">
                    <span className="text-xs font-bold text-white">{item.step}</span>
                  </div>
                  <p
                    className="text-[11px] font-mono text-cyber-text-secondary truncate mt-0.5"
                    title={item.host}
                  >
                    {item.host}
                  </p>
                </div>

                <span className="text-[10px] font-mono text-cyber-muted shrink-0">
                  {item.timestamp || '—'}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
