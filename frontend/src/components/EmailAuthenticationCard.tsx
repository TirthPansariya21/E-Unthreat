import React from 'react';
import { Shield, XCircle, CheckCircle2, AlertCircle } from 'lucide-react';

interface EmailAuthenticationCardProps {
  spf: string;
  dkim: string;
  dmarc: string;
  summary?: string;
}

export const EmailAuthenticationCard: React.FC<EmailAuthenticationCardProps> = ({
  spf,
  dkim,
  dmarc,
  summary,
}) => {
  const getProtocolConfig = (result: string, name: string) => {
    const norm = (result || 'NONE').toUpperCase();
    if (norm === 'PASS') {
      return {
        status: 'PASS',
        subtext: 'Authentication passed',
        isPass: true,
        boxBg: 'bg-emerald-500/5 border-emerald-500/30',
        textColor: 'text-emerald-400',
        icon: CheckCircle2,
      };
    }
    if (norm === 'FAIL') {
      return {
        status: 'FAIL',
        subtext: name === 'DMARC' ? 'Policy not aligned' : 'Authentication failed',
        isPass: false,
        boxBg: 'bg-red-500/5 border-red-500/30',
        textColor: 'text-red-400',
        icon: XCircle,
      };
    }
    return {
      status: 'NONE',
      subtext: 'No record / unaligned',
      isPass: false,
      boxBg: 'bg-amber-500/5 border-amber-500/30',
      textColor: 'text-amber-400',
      icon: AlertCircle,
    };
  };

  const protocols = [
    { name: 'SPF', ...getProtocolConfig(spf, 'SPF') },
    { name: 'DKIM', ...getProtocolConfig(dkim, 'DKIM') },
    { name: 'DMARC', ...getProtocolConfig(dmarc, 'DMARC') },
  ];

  const defaultSummary =
    protocols.every((p) => !p.isPass)
      ? 'All authentication checks failed. This increases the likelihood of spoofing and phishing. Treat this email with extreme caution.'
      : protocols.every((p) => p.isPass)
      ? 'All cryptographic authentication mechanisms (SPF, DKIM, DMARC) passed and verify genuine sender origin.'
      : 'Partial authentication alignment failure detected. Sender domain verification could not be validated across all protocols.';

  return (
    <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl p-5 flex flex-col justify-between h-full">
      <div>
        <h3 className="text-xs font-bold uppercase tracking-wider text-cyber-muted mb-3.5">
          EMAIL AUTHENTICATION
        </h3>

        {/* 3 Protocol Boxes */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-4">
          {protocols.map((proto) => {
            const StatusIcon = proto.icon;
            return (
              <div
                key={proto.name}
                className={`rounded-xl border p-3.5 flex items-center justify-between ${proto.boxBg}`}
              >
                <div>
                  <div className="flex items-center gap-1.5 mb-1">
                    <Shield className="w-3.5 h-3.5 text-cyber-cyan" />
                    <span className="text-xs font-bold text-cyber-text-secondary">{proto.name}</span>
                  </div>
                  <div className={`text-base font-extrabold ${proto.textColor}`}>
                    {proto.status}
                  </div>
                  <p className="text-[10px] text-cyber-muted mt-0.5">{proto.subtext}</p>
                </div>
                <StatusIcon className={`w-5 h-5 ${proto.textColor} shrink-0`} />
              </div>
            );
          })}
        </div>
      </div>

      {/* Summary Note */}
      <p className="text-xs text-cyber-text-secondary leading-relaxed bg-[#0B101D] border border-[#1E2D4A]/60 rounded-xl p-3">
        {summary || defaultSummary}
      </p>
    </div>
  );
};
