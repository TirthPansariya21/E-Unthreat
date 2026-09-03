import { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import type { NavTab } from './components/Sidebar';
import { TopHeader } from './components/TopHeader';
import { ThreatVerdictCard } from './components/ThreatVerdictCard';
import { ThreatScoreGauge } from './components/ThreatScoreGauge';
import { EmailInfoGrid } from './components/EmailInfoGrid';
import { EmailAuthenticationCard } from './components/EmailAuthenticationCard';
import { ContentAnalysisCard } from './components/ContentAnalysisCard';
import { OriginGeolocationCard } from './components/OriginGeolocationCard';
import { ThreatIndicatorsCard } from './components/ThreatIndicatorsCard';
import { ForensicTimelineCard } from './components/ForensicTimelineCard';
import { InvestigationConsoleBar } from './components/InvestigationConsoleBar';
import { CaseHistoryView } from './components/CaseHistoryView';
import { ThreatIntelView } from './components/ThreatIntelView';
import { ReportsView } from './components/ReportsView';
import { SettingsView } from './components/SettingsView';
import { EmptyState } from './components/EmptyState';
import { LoadingState } from './components/LoadingState';
import type { SampleItem, ThreatAnalysisResult, SOCStats } from './types/threat';
import {
  fetchSamples,
  fetchSampleContent,
  analyzeEmailRaw,
  analyzeEmailUpload,
  fetchCaseById,
  fetchStats,
  getPdfDownloadUrl,
} from './services/api';
import { AlertTriangle } from 'lucide-react';

export function App() {
  const [activeTab, setActiveTab] = useState<NavTab>('dashboard');
  const [samples, setSamples] = useState<SampleItem[]>([]);
  const [activeCase, setActiveCase] = useState<ThreatAnalysisResult | null>(null);
  const [stats, setStats] = useState<SOCStats | undefined>(undefined);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Initial load: Fetch samples & load default demo case (PayPal phish)
  useEffect(() => {
    fetchStats().then(setStats).catch(() => {});
    fetchSamples()
      .then((data) => {
        setSamples(data);
        if (data && data.length > 0) {
          handleSelectSample(data[0].id);
        }
      })
      .catch((err) => {
        console.error('Failed to connect to backend API:', err);
      });
  }, []);

  const handleSelectSample = async (sampleId: string) => {
    setLoading(true);
    setError(null);
    try {
      const rawText = await fetchSampleContent(sampleId);
      const result = await analyzeEmailRaw(rawText, sampleId);
      setActiveCase(result);
      setActiveTab('dashboard');
      fetchStats().then(setStats).catch(() => {});
    } catch (err: any) {
      setError(err.message || 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const handleUploadFile = async (file: File) => {
    setLoading(true);
    setError(null);
    try {
      const result = await analyzeEmailUpload(file);
      setActiveCase(result);
      setActiveTab('dashboard');
      fetchStats().then(setStats).catch(() => {});
    } catch (err: any) {
      setError(err.message || 'File analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const handlePasteAnalyze = async (rawText: string) => {
    setLoading(true);
    setError(null);
    try {
      const result = await analyzeEmailRaw(rawText, 'pasted_email.eml');
      setActiveCase(result);
      setActiveTab('dashboard');
      fetchStats().then(setStats).catch(() => {});
    } catch (err: any) {
      setError(err.message || 'Paste analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectArchivedCase = async (caseId: number) => {
    setLoading(true);
    setError(null);
    try {
      const result = await fetchCaseById(caseId);
      setActiveCase(result);
      setActiveTab('dashboard');
    } catch (err: any) {
      setError(err.message || 'Failed to load case');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadReport = () => {
    if (activeCase && activeCase.id) {
      window.open(getPdfDownloadUrl(activeCase.id), '_blank');
    }
  };

  return (
    <div className="flex min-h-screen bg-[#070B14] text-cyber-text font-sans selection:bg-cyber-cyan selection:text-black">
      {/* Left Sidebar */}
      <Sidebar activeTab={activeTab} onSelectTab={setActiveTab} stats={stats} />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-h-screen overflow-y-auto px-4 lg:px-8 py-6 max-w-[1500px] mx-auto w-full">
        {/* Top Header */}
        <TopHeader
          onDownloadReport={handleDownloadReport}
          isReportAvailable={!!activeCase}
        />

        {/* Error Notification Bar */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/40 rounded-xl p-3 mb-6 flex items-center justify-between text-xs text-red-400">
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-4 h-4" />
              <span>{error}</span>
            </div>
            <button
              onClick={() => setError(null)}
              className="text-cyber-muted hover:text-white font-bold px-2 py-0.5"
            >
              ✕
            </button>
          </div>
        )}

        {/* Tab Views */}
        {activeTab === 'history' && (
          <CaseHistoryView onSelectCase={handleSelectArchivedCase} />
        )}

        {activeTab === 'threat-intel' && <ThreatIntelView />}

        {activeTab === 'reports' && (
          <ReportsView onSelectCase={handleSelectArchivedCase} />
        )}

        {activeTab === 'settings' && <SettingsView />}

        {activeTab === 'help' && (
          <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl p-6 space-y-4">
            <h2 className="text-lg font-bold text-white">E-Unthreat User Guide & Documentation</h2>
            <p className="text-xs text-cyber-text-secondary leading-relaxed">
              E-Unthreat is an AI-powered email threat intelligence and forensic analysis platform built for SOC analysts, incident response teams, and security engineers.
            </p>
            <div className="space-y-2 text-xs">
              <div className="p-3 bg-[#090D16] rounded-xl border border-[#1E2D4A]">
                <span className="font-bold text-cyber-cyan block mb-1">1. Phishing & BEC Detection</span>
                TF-IDF lexical vectorizer combined with calibrated Logistic Regression to identify credential harvesting and financial lures.
              </div>
              <div className="p-3 bg-[#090D16] rounded-xl border border-[#1E2D4A]">
                <span className="font-bold text-emerald-400 block mb-1">2. Cryptographic Protocol Validation</span>
                Inspects SPF, DKIM, and DMARC alignment against authoritative DNS records and Received chains.
              </div>
              <div className="p-3 bg-[#090D16] rounded-xl border border-[#1E2D4A]">
                <span className="font-bold text-blue-400 block mb-1">3. GeoIP & MTA Relay Forensics</span>
                Traces the originating client IP, geolocates coordinate ranges, flags hosting/VPN providers, and reconstructs hop-by-hop traversal.
              </div>
            </div>
          </div>
        )}

        {(activeTab === 'dashboard' || activeTab === 'analyze') && (
          <>
            {loading ? (
              <LoadingState />
            ) : activeCase ? (
              <main className="space-y-4 flex-1 pb-24">
                {/* Row 1: Threat Result Card (Left) & Threat Score Gauge (Right) */}
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
                  <div className="lg:col-span-7">
                    <ThreatVerdictCard
                      verdict={activeCase.verdict}
                      copy={activeCase.verdict_copy}
                      badge={activeCase.threat_badge}
                      levelLabel={activeCase.threat_level_label}
                    />
                  </div>
                  <div className="lg:col-span-5">
                    <ThreatScoreGauge
                      score={activeCase.fraud_score}
                      verdict={activeCase.verdict}
                    />
                  </div>
                </div>

                {/* Row 2: 4 Email Overview Cards */}
                <EmailInfoGrid
                  sender={activeCase.sender}
                  subject={activeCase.subject}
                  originIp={activeCase.origin_ip}
                  isp={activeCase.origin_isp}
                  receivedDate={activeCase.analyzed_at}
                  isSuspiciousDomain={activeCase.indicators.some((i) =>
                    i.name.toLowerCase().includes('domain')
                  )}
                />

                {/* Row 3: Email Authentication & Content Analysis (ML) */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                  <EmailAuthenticationCard
                    spf={activeCase.spf_result}
                    dkim={activeCase.dkim_result}
                    dmarc={activeCase.dmarc_result}
                    summary={activeCase.auth_summary}
                  />
                  <ContentAnalysisCard
                    label={activeCase.ml_label}
                    confidencePct={activeCase.confidence_pct}
                    verdict={activeCase.verdict}
                  />
                </div>

                {/* Row 4: Origin & Geolocation (Col 1), Threat Indicators (Col 2), Forensic Timeline (Col 3) */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <OriginGeolocationCard
                    ip={activeCase.origin_ip}
                    city={activeCase.origin_city}
                    country={activeCase.origin_country}
                    isp={activeCase.origin_isp}
                    asn={activeCase.asn}
                    lat={activeCase.origin_lat}
                    lon={activeCase.origin_lon}
                    isVpn={activeCase.is_vpn_or_hosting}
                  />
                  <ThreatIndicatorsCard indicators={activeCase.indicators} />
                  <ForensicTimelineCard timeline={activeCase.timeline} />
                </div>
              </main>
            ) : (
              <EmptyState
                samples={samples}
                onSelectSample={handleSelectSample}
              />
            )}

            {/* Bottom Investigation Console Bar */}
            <div className="fixed bottom-4 left-4 right-4 lg:left-72 max-w-[1450px] mx-auto z-40">
              <InvestigationConsoleBar
                samples={samples}
                onSelectSample={handleSelectSample}
                onUploadFile={handleUploadFile}
                onPasteAnalyze={handlePasteAnalyze}
                loading={loading}
              />
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
