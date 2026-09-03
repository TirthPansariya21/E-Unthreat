import React, { useState, useEffect } from 'react';
import { Shield, CheckCircle2, Loader2 } from 'lucide-react';

export const LoadingState: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(0);

  const steps = [
    'Parsing multi-part MIME hierarchy and RFC 822 header graph...',
    'Evaluating NLP TF-IDF vectorizer and lexical lure models...',
    'Cryptographically validating SPF, DKIM, and DMARC alignment...',
    'Triangulating GeoIP origin and autonomous system provider...',
    'Reconstructing hop-by-hop MTA relay trajectory and assembling forensic report...',
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentStep((prev) => (prev < steps.length - 1 ? prev + 1 : prev));
    }, 400);
    return () => clearInterval(timer);
  }, [steps.length]);

  return (
    <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl p-8 max-w-xl mx-auto text-center shadow-2xl my-12">
      <div className="w-16 h-16 rounded-2xl bg-blue-500/10 border border-blue-500/30 flex items-center justify-center text-cyber-cyan mx-auto mb-5 shadow-cyan-glow relative">
        <Shield className="w-8 h-8" />
        <span className="absolute -top-1 -right-1 flex h-3 w-3">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyber-cyan opacity-75" />
          <span className="relative inline-flex rounded-full h-3 w-3 bg-cyber-cyan" />
        </span>
      </div>

      <h3 className="text-lg font-bold text-white mb-2">Executing Deep Threat Pipeline</h3>
      <p className="text-xs text-cyber-text-secondary mb-6">
        Running offline classifiers, cryptographic verifications, and origin forensics.
      </p>

      {/* Step List */}
      <div className="space-y-2.5 text-left bg-[#090D16] border border-[#1E2D4A] rounded-xl p-4">
        {steps.map((step, idx) => {
          const isDone = idx < currentStep;
          const isCurrent = idx === currentStep;

          return (
            <div key={idx} className="flex items-center gap-2.5 text-xs">
              {isDone ? (
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
              ) : isCurrent ? (
                <Loader2 className="w-4 h-4 text-cyber-cyan animate-spin shrink-0" />
              ) : (
                <span className="w-4 h-4 rounded-full border border-[#1E2D4A] shrink-0" />
              )}
              <span
                className={
                  isDone
                    ? 'text-cyber-muted line-through'
                    : isCurrent
                    ? 'text-white font-semibold'
                    : 'text-cyber-muted'
                }
              >
                {step}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
