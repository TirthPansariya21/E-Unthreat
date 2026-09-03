import React, { useState, useEffect } from 'react';
import { History, Search, Download, Eye, ShieldAlert, AlertTriangle, ShieldCheck } from 'lucide-react';
import type { CaseRecord } from '../types/threat';
import { fetchCases, getPdfDownloadUrl } from '../services/api';

interface CaseHistoryViewProps {
  onSelectCase: (caseId: number) => void;
}

export const CaseHistoryView: React.FC<CaseHistoryViewProps> = ({ onSelectCase }) => {
  const [cases, setCases] = useState<CaseRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [verdictFilter, setVerdictFilter] = useState<string>('ALL');

  useEffect(() => {
    fetchCases()
      .then((data) => setCases(data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  const filteredCases = cases.filter((c) => {
    const matchesSearch =
      (c.sender || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
      (c.subject || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
      (c.filename || '').toLowerCase().includes(searchQuery.toLowerCase());
    const matchesVerdict = verdictFilter === 'ALL' || c.verdict.toUpperCase() === verdictFilter;
    return matchesSearch && matchesVerdict;
  });

  return (
    <div className="space-y-4">
      {/* Header & Filter Controls */}
      <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl p-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <History className="w-5 h-5 text-cyber-cyan" />
            SOC Forensic Case Archive
          </h2>
          <p className="text-xs text-cyber-text-secondary mt-0.5">
            Browse and review historical email incident investigations stored in local database.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2.5">
          {/* Search Bar */}
          <div className="relative">
            <Search className="w-4 h-4 text-cyber-muted absolute left-3 top-2.5 pointer-events-none" />
            <input
              type="text"
              placeholder="Search sender, subject..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="bg-[#090D16] border border-[#1E2D4A] rounded-xl pl-9 pr-3 py-2 text-xs font-semibold text-white focus:outline-none focus:border-cyber-cyan w-full sm:w-56"
            />
          </div>

          {/* Verdict Filter Buttons */}
          <div className="bg-[#090D16] border border-[#1E2D4A] rounded-xl p-1 flex items-center gap-1">
            {['ALL', 'PHISHING', 'SUSPICIOUS', 'LEGITIMATE'].map((filter) => (
              <button
                key={filter}
                onClick={() => setVerdictFilter(filter)}
                className={`px-2.5 py-1 rounded-lg text-[11px] font-bold transition-colors ${
                  verdictFilter === filter
                    ? 'bg-blue-600/30 text-cyber-cyan border border-blue-500/40 shadow-sm'
                    : 'text-cyber-muted hover:text-white'
                }`}
              >
                {filter}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Cases Table */}
      <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl overflow-hidden shadow-2xl">
        {loading ? (
          <div className="p-12 text-center text-cyber-muted text-xs">
            <span className="w-6 h-6 border-2 border-cyber-cyan/30 border-t-cyber-cyan rounded-full animate-spin inline-block mb-3" />
            <p>Loading historical incident cases...</p>
          </div>
        ) : filteredCases.length === 0 ? (
          <div className="p-12 text-center text-cyber-muted text-xs">
            No archived cases found matching search criteria.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="bg-[#090D16] border-b border-[#1E2D4A] text-cyber-muted uppercase text-[10px] font-bold tracking-wider">
                  <th className="py-3 px-4">ID</th>
                  <th className="py-3 px-4">Sender Address</th>
                  <th className="py-3 px-4">Subject</th>
                  <th className="py-3 px-4">Verdict</th>
                  <th className="py-3 px-4">Risk Index</th>
                  <th className="py-3 px-4">Origin</th>
                  <th className="py-3 px-4">Analyzed (UTC)</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1E2D4A]/50">
                {filteredCases.map((c) => {
                  const isPhish = c.verdict === 'Phishing';
                  const isSus = c.verdict === 'Suspicious';

                  const badgeClass = isPhish
                    ? 'bg-red-500/10 text-red-400 border-red-500/30'
                    : isSus
                    ? 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                    : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';

                  const barColor = isPhish ? 'bg-red-500' : isSus ? 'bg-amber-500' : 'bg-emerald-500';

                  return (
                    <tr
                      key={c.id}
                      className="hover:bg-white/[0.02] transition-colors group cursor-pointer"
                      onClick={() => onSelectCase(c.id)}
                    >
                      <td className="py-3.5 px-4 font-mono font-bold text-cyber-muted">#{c.id}</td>
                      <td className="py-3.5 px-4 font-mono font-semibold text-white max-w-[200px] truncate" title={c.sender}>
                        {c.sender}
                      </td>
                      <td className="py-3.5 px-4 text-cyber-text max-w-[240px] truncate" title={c.subject}>
                        {c.subject}
                      </td>
                      <td className="py-3.5 px-4">
                        <span className={`inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded border ${badgeClass}`}>
                          {isPhish && <ShieldAlert className="w-3 h-3" />}
                          {isSus && <AlertTriangle className="w-3 h-3" />}
                          {!isPhish && !isSus && <ShieldCheck className="w-3 h-3" />}
                          {c.verdict}
                        </span>
                      </td>
                      <td className="py-3.5 px-4">
                        <div className="flex items-center gap-2">
                          <span className="font-mono font-bold text-white w-6">{c.fraud_score}</span>
                          <div className="w-16 h-1.5 rounded-full bg-[#1E2D4A] overflow-hidden">
                            <div className={`h-full ${barColor}`} style={{ width: `${c.fraud_score}%` }} />
                          </div>
                        </div>
                      </td>
                      <td className="py-3.5 px-4 text-cyber-text-secondary">{c.origin_country || '—'}</td>
                      <td className="py-3.5 px-4 font-mono text-[11px] text-cyber-muted">{c.analyzed_at || '—'}</td>
                      <td className="py-3.5 px-4 text-right" onClick={(e) => e.stopPropagation()}>
                        <div className="flex items-center justify-end gap-2">
                          <button
                            onClick={() => onSelectCase(c.id)}
                            className="p-1.5 rounded-lg bg-blue-500/10 hover:bg-blue-500/20 text-cyber-cyan border border-blue-500/30"
                            title="Open Full Case"
                          >
                            <Eye className="w-3.5 h-3.5" />
                          </button>
                          <a
                            href={getPdfDownloadUrl(c.id)}
                            download
                            className="p-1.5 rounded-lg bg-white/[0.04] hover:bg-white/[0.08] text-cyber-muted hover:text-white border border-[#1E2D4A]"
                            title="Download PDF"
                          >
                            <Download className="w-3.5 h-3.5" />
                          </a>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
