export type ThreatVerdict = 'Phishing' | 'Suspicious' | 'Legitimate';

export interface ThreatIndicator {
  name: string;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  description: string;
}

export interface TimelineStep {
  step: 'Email Sent' | 'Relay' | 'Delivered' | string;
  host: string;
  ip?: string;
  role: string;
  timestamp: string;
}

export interface SampleItem {
  id: string;
  name: string;
  category: string;
  description: string;
  expected_verdict: ThreatVerdict;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
}

export interface CaseRecord {
  id: number;
  filename: string;
  sender: string;
  subject: string;
  verdict: ThreatVerdict;
  fraud_score: number;
  origin_country: string;
  analyzed_at: string;
}

export interface ThreatAnalysisResult {
  id?: number;
  filename?: string;
  verdict: ThreatVerdict;
  fraud_score: number;
  sender: string;
  from_name?: string;
  to?: string;
  subject: string;
  origin_ip: string;
  origin_isp?: string;
  origin_country: string;
  origin_city: string;
  origin_lat: number;
  origin_lon: number;
  is_vpn_or_hosting: boolean;
  spf_result: string;
  dkim_result: string;
  dmarc_result: string;
  ml_label: string;
  ml_confidence: number;
  confidence_pct: number;
  domain: string;
  asn?: string;
  threat_badge: 'CRITICAL' | 'ELEVATED' | 'LOW';
  threat_level_label: 'High Risk' | 'Medium Risk' | 'Low Risk';
  verdict_copy: string;
  auth_summary: string;
  indicators: ThreatIndicator[];
  timeline: TimelineStep[];
  content_flags?: string[];
  header_flags?: string[];
  origin_flags?: string[];
  attachments?: string[];
  warnings?: string[];
  analyzed_at?: string;
}

export interface SOCStats {
  total: number;
  phishing: number;
  suspicious: number;
  legitimate: number;
  avg_score: number;
}
