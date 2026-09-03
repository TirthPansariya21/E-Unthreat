import React from 'react';
import { User, Mail, Globe, Clock, AlertTriangle } from 'lucide-react';

interface EmailInfoGridProps {
  sender: string;
  subject: string;
  originIp: string;
  isp?: string;
  receivedDate?: string;
  isSuspiciousDomain?: boolean;
}

export const EmailInfoGrid: React.FC<EmailInfoGridProps> = ({
  sender,
  subject,
  originIp,
  isp,
  receivedDate,
  isSuspiciousDomain = false,
}) => {
  const displayDate = receivedDate || new Date().toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
    timeZoneName: 'short',
  });

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">
      {/* 1. SENDER */}
      <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl p-4 flex items-start gap-3.5 hover:border-cyber-border-hover transition-colors">
        <div className="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-cyber-cyan shrink-0">
          <User className="w-4 h-4" />
        </div>
        <div className="min-w-0 flex-1">
          <span className="text-[11px] font-bold uppercase tracking-wider text-cyber-muted block mb-0.5">
            SENDER
          </span>
          <p className="text-xs font-semibold text-white font-mono truncate" title={sender}>
            {sender || 'Unknown'}
          </p>
          {isSuspiciousDomain && (
            <span className="inline-flex items-center gap-1 text-[10px] font-bold text-red-400 mt-1 bg-red-500/10 border border-red-500/20 px-1.5 py-0.5 rounded">
              <AlertTriangle className="w-2.5 h-2.5" />
              Suspicious Domain
            </span>
          )}
        </div>
      </div>

      {/* 2. SUBJECT */}
      <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl p-4 flex items-start gap-3.5 hover:border-cyber-border-hover transition-colors">
        <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 shrink-0">
          <Mail className="w-4 h-4" />
        </div>
        <div className="min-w-0 flex-1">
          <span className="text-[11px] font-bold uppercase tracking-wider text-cyber-muted block mb-0.5">
            SUBJECT
          </span>
          <p className="text-xs font-medium text-cyber-text leading-snug line-clamp-2" title={subject}>
            {subject || '(No Subject)'}
          </p>
        </div>
      </div>

      {/* 3. ORIGIN IP */}
      <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl p-4 flex items-start gap-3.5 hover:border-cyber-border-hover transition-colors">
        <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyber-cyan shrink-0">
          <Globe className="w-4 h-4" />
        </div>
        <div className="min-w-0 flex-1">
          <span className="text-[11px] font-bold uppercase tracking-wider text-cyber-muted block mb-0.5">
            ORIGIN IP
          </span>
          <p className="text-xs font-bold text-white font-mono">
            {originIp || 'Unknown'}
          </p>
          {isp && (
            <p className="text-[11px] text-cyber-cyan font-medium truncate mt-0.5" title={isp}>
              {isp}
            </p>
          )}
        </div>
      </div>

      {/* 4. RECEIVED */}
      <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl p-4 flex items-start gap-3.5 hover:border-cyber-border-hover transition-colors">
        <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400 shrink-0">
          <Clock className="w-4 h-4" />
        </div>
        <div className="min-w-0 flex-1">
          <span className="text-[11px] font-bold uppercase tracking-wider text-cyber-muted block mb-0.5">
            RECEIVED
          </span>
          <p className="text-xs font-semibold text-white leading-snug">
            {displayDate}
          </p>
          <span className="text-[10px] text-cyber-muted">UTC Timestamp</span>
        </div>
      </div>
    </div>
  );
};
