import React, { useState, useRef } from 'react';
import { UploadCloud, FileText, Search, ChevronDown, X } from 'lucide-react';
import type { SampleItem } from '../types/threat';

interface InvestigationConsoleBarProps {
  samples: SampleItem[];
  onSelectSample: (sampleId: string) => void;
  onUploadFile: (file: File) => void;
  onPasteAnalyze: (rawText: string) => void;
  loading: boolean;
}

export const InvestigationConsoleBar: React.FC<InvestigationConsoleBarProps> = ({
  samples,
  onSelectSample,
  onUploadFile,
  onPasteAnalyze,
  loading,
}) => {
  const [activeMode, setActiveMode] = useState<'demo' | 'upload' | 'paste'>('demo');
  const [selectedSampleId, setSelectedSampleId] = useState<string>(samples[0]?.id || 'paypal_phish.eml');
  const [pasteModalOpen, setPasteModalOpen] = useState(false);
  const [rawText, setRawText] = useState('');
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onUploadFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      onUploadFile(e.target.files[0]);
    }
  };

  const handlePrimaryAnalyze = () => {
    if (activeMode === 'demo') {
      onSelectSample(selectedSampleId);
    } else if (activeMode === 'upload') {
      fileInputRef.current?.click();
    } else {
      setPasteModalOpen(true);
    }
  };

  return (
    <>
      <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl p-3 flex flex-col md:flex-row items-center justify-between gap-3 shadow-2xl">
        {/* Left: Drag & Drop Dropzone info */}
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setDragActive(true);
          }}
          onDragLeave={() => setDragActive(false)}
          onDrop={handleFileDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`flex items-center gap-3 px-4 py-2 rounded-xl border border-dashed transition-colors cursor-pointer w-full md:w-auto ${
            dragActive
              ? 'border-cyber-cyan bg-cyber-cyan/10'
              : 'border-[#1E2D4A] hover:border-cyber-cyan/50 bg-[#090D16]/60'
          }`}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".eml,.txt,.msg,.mbox"
            className="hidden"
            onChange={handleFileChange}
          />
          <div className="w-8 h-8 rounded-lg bg-blue-500/10 border border-blue-500/30 flex items-center justify-center text-cyber-cyan shrink-0">
            <UploadCloud className="w-4 h-4" />
          </div>
          <div>
            <p className="text-xs font-semibold text-white">Drag & drop email file here</p>
            <p className="text-[10px] text-cyber-muted">.eml, .msg, .mbox files supported</p>
          </div>
        </div>

        {/* Center: Mode Tabs + Selector */}
        <div className="flex items-center gap-2 w-full md:w-auto justify-center">
          <div className="bg-[#090D16] border border-[#1E2D4A] rounded-xl p-1 flex items-center gap-1">
            <button
              onClick={() => setActiveMode('demo')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeMode === 'demo'
                  ? 'bg-blue-600/30 text-cyber-cyan border border-blue-500/40 shadow-sm'
                  : 'text-cyber-text-secondary hover:text-white'
              }`}
            >
              Demo Cases
            </button>
            <button
              onClick={() => {
                setActiveMode('upload');
                fileInputRef.current?.click();
              }}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeMode === 'upload'
                  ? 'bg-blue-600/30 text-cyber-cyan border border-blue-500/40 shadow-sm'
                  : 'text-cyber-text-secondary hover:text-white'
              }`}
            >
              Upload Email
            </button>
            <button
              onClick={() => {
                setActiveMode('paste');
                setPasteModalOpen(true);
              }}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeMode === 'paste'
                  ? 'bg-blue-600/30 text-cyber-cyan border border-blue-500/40 shadow-sm'
                  : 'text-cyber-text-secondary hover:text-white'
              }`}
            >
              Paste Raw Email
            </button>
          </div>

          {/* If demo mode, inline select */}
          {activeMode === 'demo' && (
            <div className="relative hidden lg:block">
              <select
                value={selectedSampleId}
                onChange={(e) => setSelectedSampleId(e.target.value)}
                className="appearance-none bg-[#090D16] border border-[#1E2D4A] rounded-xl px-3 py-2 pr-8 text-xs font-semibold text-white focus:outline-none focus:border-cyber-cyan"
              >
                {samples.map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.name} ({s.expected_verdict})
                  </option>
                ))}
              </select>
              <ChevronDown className="w-3.5 h-3.5 text-cyber-muted absolute right-2.5 top-2.5 pointer-events-none" />
            </div>
          )}
        </div>

        {/* Right: Primary Action Button */}
        <button
          onClick={handlePrimaryAnalyze}
          disabled={loading}
          className="w-full md:w-auto flex items-center justify-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white text-xs font-bold shadow-blue-glow transition-all duration-200 hover:scale-[1.02] cursor-pointer disabled:opacity-50"
        >
          {loading ? (
            <span className="flex items-center gap-2">
              <span className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              <span>Analyzing...</span>
            </span>
          ) : (
            <>
              <Search className="w-4 h-4" />
              <span>Analyze Email</span>
            </>
          )}
        </button>
      </div>

      {/* Paste Raw Email Modal */}
      {pasteModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl w-full max-w-2xl p-6 shadow-2xl animate-fade-in relative">
            <button
              onClick={() => setPasteModalOpen(false)}
              className="absolute right-4 top-4 text-cyber-muted hover:text-white"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-2.5 mb-2">
              <FileText className="w-5 h-5 text-cyber-cyan" />
              <h3 className="text-lg font-bold text-white">Paste Raw Email Source / MIME Headers</h3>
            </div>
            <p className="text-xs text-cyber-text-secondary mb-4">
              Paste the raw RFC 822 email headers and message body to trigger full multi-layer forensic inspection.
            </p>

            <textarea
              rows={10}
              value={rawText}
              onChange={(e) => setRawText(e.target.value)}
              placeholder="From: security@paypal-verify.com&#10;To: user@target.com&#10;Subject: Account Suspension Notice&#10;Received: from unknown (45.9.148.22)...&#10;&#10;Dear Customer, please verify your details..."
              className="w-full bg-[#090D16] border border-[#1E2D4A] rounded-xl p-3.5 text-xs font-mono text-cyber-cyan focus:outline-none focus:border-cyber-cyan mb-4"
            />

            <div className="flex items-center justify-end gap-3">
              <button
                onClick={() => setPasteModalOpen(false)}
                className="px-4 py-2 rounded-xl text-xs font-semibold text-cyber-muted hover:text-white bg-white/[0.03] border border-[#1E2D4A]"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  if (rawText.trim()) {
                    setPasteModalOpen(false);
                    onPasteAnalyze(rawText);
                  }
                }}
                disabled={!rawText.trim()}
                className="px-5 py-2 rounded-xl text-xs font-bold text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 shadow-blue-glow disabled:opacity-50"
              >
                Run Forensic Analysis
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
