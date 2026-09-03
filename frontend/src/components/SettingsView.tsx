import React from 'react';
import { Settings, Shield, Server, Database, Lock, CheckCircle2 } from 'lucide-react';

export const SettingsView: React.FC = () => {
  return (
    <div className="space-y-6 max-w-4xl">
      <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl p-6">
        <div className="flex items-center gap-2.5 mb-2">
          <Settings className="w-5 h-5 text-cyber-cyan" />
          <h2 className="text-lg font-bold text-white">Engine Configuration & Telemetry</h2>
        </div>
        <p className="text-xs text-cyber-text-secondary max-w-2xl">
          Manage local threat intelligence heuristics, sandboxed ML model weights, and cryptographic verification parameters.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* ML Configuration */}
        <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl p-5 space-y-3">
          <div className="flex items-center gap-2 text-white text-sm font-bold">
            <Server className="w-4 h-4 text-cyber-cyan" />
            <span>NLP Classifier Engine</span>
          </div>
          <p className="text-xs text-cyber-text-secondary">
            TF-IDF Vectorizer + Calibrated Logistic Regression (Scikit-Learn 1.5.0)
          </p>
          <div className="flex items-center gap-2 text-xs text-emerald-400">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Local Model Loaded (data/models/phishing_tfidf.joblib)</span>
          </div>
        </div>

        {/* Database */}
        <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl p-5 space-y-3">
          <div className="flex items-center gap-2 text-white text-sm font-bold">
            <Database className="w-4 h-4 text-cyber-cyan" />
            <span>SQLite Persistence Layer</span>
          </div>
          <p className="text-xs text-cyber-text-secondary">
            Local encrypted incident cases and forensic flags archive.
          </p>
          <div className="flex items-center gap-2 text-xs text-emerald-400">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Connected: data/cases.db</span>
          </div>
        </div>

        {/* Cryptographic Alignment */}
        <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl p-5 space-y-3">
          <div className="flex items-center gap-2 text-white text-sm font-bold">
            <Lock className="w-4 h-4 text-cyber-cyan" />
            <span>Cryptographic DNS Validators</span>
          </div>
          <p className="text-xs text-cyber-text-secondary">
            Direct DNS TXT / SPF / DMARC resolution via dnspython & DKIM verification.
          </p>
          <div className="flex items-center gap-2 text-xs text-emerald-400">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Active with offline fallback</span>
          </div>
        </div>

        {/* System Telemetry */}
        <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl p-5 space-y-3">
          <div className="flex items-center gap-2 text-white text-sm font-bold">
            <Shield className="w-4 h-4 text-cyber-cyan" />
            <span>System Telemetry</span>
          </div>
          <p className="text-xs text-cyber-text-secondary">
            FastAPI Backend: http://localhost:8000
          </p>
          <div className="flex items-center gap-2 text-xs text-cyber-cyan">
            <span className="w-2 h-2 rounded-full bg-cyber-cyan animate-pulse" />
            <span>Real-time REST API Active</span>
          </div>
        </div>
      </div>
    </div>
  );
};
