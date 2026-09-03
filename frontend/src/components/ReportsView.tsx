import React, { useState, useEffect } from 'react';
import { FileText, Download, Calendar, Eye } from 'lucide-react';
import type { CaseRecord } from '../types/threat';
import { fetchCases, getPdfDownloadUrl } from '../services/api';

interface ReportsViewProps {
  onSelectCase: (caseId: number) => void;
}

export const ReportsView: React.FC<ReportsViewProps> = ({ onSelectCase }) => {
  const [cases, setCases] = useState<CaseRecord[]>([]);

  useEffect(() => {
    fetchCases().then(setCases).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl p-6">
        <div className="flex items-center gap-2.5 mb-2">
          <FileText className="w-5 h-5 text-cyber-cyan" />
          <h2 className="text-lg font-bold text-white">Forensic PDF Report Center</h2>
        </div>
        <p className="text-xs text-cyber-text-secondary max-w-2xl mb-4">
          Export standardized forensic analysis dossiers detailing cryptographic email authentication, machine learning NLP scores, WHOIS entity lookups, and relay graph diagnostics.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {cases.map((c) => (
          <div
            key={c.id}
            className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl p-4 flex flex-col justify-between hover:border-cyber-cyan/40 transition-all shadow-md"
          >
            <div>
              <div className="flex items-center justify-between gap-2 mb-2">
                <span className="text-[10px] font-mono font-bold text-cyber-muted">CASE #{c.id}</span>
                <span
                  className={`text-[10px] font-bold px-2 py-0.5 rounded border ${
                    c.verdict === 'Phishing'
                      ? 'bg-red-500/10 text-red-400 border-red-500/30'
                      : c.verdict === 'Suspicious'
                      ? 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                      : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                  }`}
                >
                  {c.verdict} ({c.fraud_score}/100)
                </span>
              </div>

              <h4 className="text-xs font-bold text-white truncate" title={c.subject}>
                {c.subject || '(No Subject)'}
              </h4>
              <p className="text-[11px] font-mono text-cyber-text-secondary truncate mt-1">
                {c.sender}
              </p>

              <div className="flex items-center gap-1.5 text-[10px] text-cyber-muted mt-3">
                <Calendar className="w-3 h-3" />
                <span>{c.analyzed_at || 'Recent Analysis'}</span>
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-[#1E2D4A]/60 flex items-center justify-between gap-2">
              <button
                onClick={() => onSelectCase(c.id)}
                className="text-xs text-cyber-cyan font-semibold hover:underline flex items-center gap-1"
              >
                <Eye className="w-3.5 h-3.5" />
                <span>Inspect</span>
              </button>

              <a
                href={getPdfDownloadUrl(c.id)}
                download
                className="px-3 py-1.5 rounded-lg bg-blue-600/20 hover:bg-blue-600/30 text-cyber-cyan border border-blue-500/40 text-xs font-semibold flex items-center gap-1.5 transition-colors"
              >
                <Download className="w-3 h-3" />
                <span>Download PDF</span>
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
