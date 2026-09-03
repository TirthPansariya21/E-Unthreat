import React from 'react';
import { Shield, Cpu, Lock, Globe, Server, FileCheck, ArrowRight } from 'lucide-react';
import type { SampleItem } from '../types/threat';

interface EmptyStateProps {
  samples: SampleItem[];
  onSelectSample: (sampleId: string) => void;
  onOpenUpload?: () => void;
  onOpenPaste?: () => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  samples,
  onSelectSample,
}) => {
  return (
    <div className="space-y-6">
      {/* Ready Banner */}
      <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl p-8 text-center relative overflow-hidden">
        <div className="w-16 h-16 rounded-2xl bg-blue-500/10 border border-blue-500/30 flex items-center justify-center text-cyber-cyan mx-auto mb-4 shadow-cyan-glow">
          <Shield className="w-8 h-8" />
        </div>

        <h2 className="text-xl lg:text-2xl font-black text-white tracking-tight">
          READY FOR THREAT INVESTIGATION
        </h2>
        <p className="text-xs lg:text-sm text-cyber-text-secondary max-w-xl mx-auto mt-2 leading-relaxed">
          Select a pre-loaded threat sample below, drag and drop an email file (.eml/.msg), or paste raw RFC 822 MIME headers to begin multi-layer forensic inspection.
        </p>

        {/* Feature Capability Tags */}
        <div className="flex flex-wrap items-center justify-center gap-2 mt-6">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-white/[0.03] border border-[#1E2D4A] text-cyber-text-secondary">
            <Cpu className="w-3.5 h-3.5 text-cyber-cyan" />
            TF-IDF & Logistic ML
          </span>
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-white/[0.03] border border-[#1E2D4A] text-cyber-text-secondary">
            <Lock className="w-3.5 h-3.5 text-emerald-400" />
            SPF / DKIM / DMARC Cryptography
          </span>
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-white/[0.03] border border-[#1E2D4A] text-cyber-text-secondary">
            <Globe className="w-3.5 h-3.5 text-blue-400" />
            GeoIP & ASN Mapping
          </span>
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-white/[0.03] border border-[#1E2D4A] text-cyber-text-secondary">
            <Server className="w-3.5 h-3.5 text-purple-400" />
            Hop-by-Hop MTA Traversal
          </span>
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-white/[0.03] border border-[#1E2D4A] text-cyber-text-secondary">
            <FileCheck className="w-3.5 h-3.5 text-amber-400" />
            Forensic PDF Generator
          </span>
        </div>
      </div>

      {/* Pre-loaded Sample Incident Library */}
      <div>
        <h3 className="text-xs font-bold uppercase tracking-wider text-cyber-muted mb-3 flex items-center gap-2">
          <span>📂</span>
          SELECT A DEMO INVESTIGATION SAMPLE
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5">
          {samples.map((sample) => {
            const isPhish = sample.expected_verdict === 'Phishing';
            const isSus = sample.expected_verdict === 'Suspicious';
            const badgeBg = isPhish
              ? 'bg-red-500/10 text-red-400 border-red-500/30'
              : isSus
              ? 'bg-amber-500/10 text-amber-400 border-amber-500/30'
              : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';

            return (
              <div
                key={sample.id}
                onClick={() => onSelectSample(sample.id)}
                className="bg-[#0F1626] border border-[#1E2D4A] hover:border-cyber-cyan/50 rounded-2xl p-4 flex flex-col justify-between cursor-pointer transition-all duration-200 hover:-translate-y-0.5 hover:shadow-cyan-glow group"
              >
                <div>
                  <div className="flex items-center justify-between gap-2 mb-2">
                    <span className="text-[10px] font-bold tracking-wider uppercase text-cyber-muted">
                      {sample.category}
                    </span>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${badgeBg}`}>
                      {sample.expected_verdict}
                    </span>
                  </div>
                  <h4 className="text-sm font-bold text-white group-hover:text-cyber-cyan transition-colors">
                    {sample.name}
                  </h4>
                  <p className="text-xs text-cyber-text-secondary mt-1 line-clamp-2 leading-relaxed">
                    {sample.description}
                  </p>
                </div>

                <div className="mt-4 pt-3 border-t border-[#1E2D4A]/60 flex items-center justify-between text-xs text-cyber-cyan font-semibold">
                  <span>Run Analysis</span>
                  <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
