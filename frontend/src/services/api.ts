import type { CaseRecord, SampleItem, SOCStats, ThreatAnalysisResult } from '../types/threat';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api';

export async function fetchStats(): Promise<SOCStats> {
  const res = await fetch(`${API_BASE}/stats`);
  if (!res.ok) throw new Error('Failed to fetch SOC statistics');
  return res.json();
}

export async function fetchSamples(): Promise<SampleItem[]> {
  const res = await fetch(`${API_BASE}/samples`);
  if (!res.ok) throw new Error('Failed to fetch demo samples');
  return res.json();
}

export async function fetchSampleContent(sampleId: string): Promise<string> {
  const res = await fetch(`${API_BASE}/samples/${sampleId}`);
  if (!res.ok) throw new Error('Failed to fetch sample source');
  const data = await res.json();
  return data.raw_text;
}

export async function analyzeEmailRaw(rawText: string, filename = 'pasted_email.eml'): Promise<ThreatAnalysisResult> {
  const res = await fetch(`${API_BASE}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ raw_text: rawText, filename }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Email analysis failed');
  }
  return res.json();
}

export async function analyzeEmailUpload(file: File): Promise<ThreatAnalysisResult> {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${API_BASE}/analyze/upload`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'File upload analysis failed');
  }
  return res.json();
}

export async function fetchCases(): Promise<CaseRecord[]> {
  const res = await fetch(`${API_BASE}/cases`);
  if (!res.ok) throw new Error('Failed to fetch archived cases');
  return res.json();
}

export async function fetchCaseById(caseId: number): Promise<ThreatAnalysisResult> {
  const res = await fetch(`${API_BASE}/cases/${caseId}`);
  if (!res.ok) throw new Error('Failed to fetch case record');
  return res.json();
}

export function getPdfDownloadUrl(caseId: number | string): string {
  return `${API_BASE}/cases/${caseId}/pdf`;
}
