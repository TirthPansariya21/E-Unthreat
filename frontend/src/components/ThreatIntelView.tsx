import React, { useState } from 'react';
import { Globe, Search, ShieldAlert, Database } from 'lucide-react';

export const ThreatIntelView: React.FC = () => {
  const [domainQuery, setDomainQuery] = useState('');
  const [checkedDomain, setCheckedDomain] = useState<string | null>(null);

  const lookalikeList = [
    { target: 'paypal.com', detected: 'paypa1-secure.com', risk: 'CRITICAL', type: 'Homoglyph substitution' },
    { target: 'microsoft.com', detected: 'microsoft-verify.com', risk: 'HIGH', type: 'Keyword spoofing' },
    { target: 'dhl.com', detected: 'dhl-customs-clear.com', risk: 'HIGH', type: 'Brand lure domain' },
    { target: 'apple.com', detected: 'apple-id-update.net', risk: 'CRITICAL', type: 'Credential harvesting' },
    { target: 'chase.com', detected: 'chase-security-auth.cc', risk: 'CRITICAL', type: 'Banking impersonation' },
  ];

  return (
    <div className="space-y-6">
      {/* Search Header */}
      <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl p-6">
        <div className="flex items-center gap-2.5 mb-2">
          <Globe className="w-5 h-5 text-cyber-cyan" />
          <h2 className="text-lg font-bold text-white">Threat Intelligence Knowledge Base</h2>
        </div>
        <p className="text-xs text-cyber-text-secondary max-w-2xl mb-4">
          Query target domain names, IP address ranges, and brand keywords against the local lure dictionary and heuristic threat models.
        </p>

        <div className="flex gap-2 max-w-xl">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-cyber-muted absolute left-3 top-2.5 pointer-events-none" />
            <input
              type="text"
              placeholder="e.g. microsoft-verify.com, 20.42.65.80"
              value={domainQuery}
              onChange={(e) => setDomainQuery(e.target.value)}
              className="w-full bg-[#090D16] border border-[#1E2D4A] rounded-xl pl-9 pr-3 py-2 text-xs font-semibold text-white focus:outline-none focus:border-cyber-cyan font-mono"
            />
          </div>
          <button
            onClick={() => setCheckedDomain(domainQuery || 'microsoft-verify.com')}
            className="px-4 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white rounded-xl text-xs font-bold shadow-blue-glow"
          >
            Inspect Entity
          </button>
        </div>

        {checkedDomain && (
          <div className="mt-4 p-4 rounded-xl bg-[#090D16] border border-red-500/30 flex items-start gap-3">
            <ShieldAlert className="w-5 h-5 text-red-400 shrink-0 mt-0.5" />
            <div className="text-xs">
              <div className="flex items-center gap-2">
                <span className="font-mono font-bold text-white">{checkedDomain}</span>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-red-500/10 text-red-400 border border-red-500/30">
                  FLAGGED LURE
                </span>
              </div>
              <p className="text-cyber-text-secondary mt-1">
                Domain registered via privacy proxy. Keyword matches Microsoft 365 brand impersonation rule dictionary.
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Brand Lookalike Database Table */}
      <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl p-6">
        <h3 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
          <Database className="w-4 h-4 text-cyber-cyan" />
          Active Brand Impersonation Signatures
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-[#1E2D4A] text-cyber-muted uppercase text-[10px] font-bold">
                <th className="py-2.5 px-3">Targeted Brand</th>
                <th className="py-2.5 px-3">Spoofed Domain Signature</th>
                <th className="py-2.5 px-3">Risk Level</th>
                <th className="py-2.5 px-3">Attack Pattern</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1E2D4A]/40">
              {lookalikeList.map((item, idx) => (
                <tr key={idx} className="hover:bg-white/[0.02]">
                  <td className="py-3 px-3 font-semibold text-white">{item.target}</td>
                  <td className="py-3 px-3 font-mono text-red-400 font-medium">{item.detected}</td>
                  <td className="py-3 px-3">
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-red-500/10 text-red-400 border border-red-500/30">
                      {item.risk}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-cyber-text-secondary">{item.type}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
