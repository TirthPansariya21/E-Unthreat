import React from 'react';
import { Globe, ExternalLink, ShieldAlert } from 'lucide-react';

interface OriginGeolocationCardProps {
  ip: string;
  city: string;
  country: string;
  isp?: string;
  asn?: string;
  lat: number;
  lon: number;
  isVpn?: boolean;
}

export const OriginGeolocationCard: React.FC<OriginGeolocationCardProps> = ({
  ip,
  city,
  country,
  isp,
  asn,
  lat,
  lon,
  isVpn,
}) => {
  const locationString = city && country ? `${city}, ${country}` : country || 'Unknown Origin';

  // Calculate approximate SVG pinpoint coordinates on natural earth projection
  const pinX = Math.max(10, Math.min(90, ((lon + 180) / 360) * 100));
  const pinY = Math.max(15, Math.min(85, ((90 - lat) / 180) * 100));

  return (
    <div className="bg-[#0F1626] border border-[#1E2D4A] rounded-2xl p-5 flex flex-col justify-between h-full">
      <div>
        <div className="flex items-center justify-between mb-3.5">
          <h3 className="text-xs font-bold uppercase tracking-wider text-cyber-muted flex items-center gap-2">
            <Globe className="w-3.5 h-3.5 text-cyber-cyan" />
            ORIGIN & GEOLOCATION
          </h3>
          {isVpn && (
            <span className="text-[10px] font-bold text-amber-400 bg-amber-500/10 border border-amber-500/30 px-2 py-0.5 rounded-full flex items-center gap-1">
              <ShieldAlert className="w-3 h-3" />
              VPN / Hosting Range
            </span>
          )}
        </div>

        {/* Dark World Map SVG Frame */}
        <div className="w-full h-32 rounded-xl bg-[#090D16] border border-[#1E2D4A]/80 relative overflow-hidden mb-4 flex items-center justify-center">
          {/* Subtle World Map Silhouette SVG */}
          <svg className="w-full h-full opacity-40" viewBox="0 0 1000 500" fill="#1E293B">
            <path d="M150,120 Q180,80 240,110 Q280,150 250,220 Q200,280 260,380 Q290,440 240,460 Q210,400 180,310 Q140,240 120,180 Z" />
            <path d="M480,80 Q530,60 580,100 Q560,160 520,170 Q550,260 520,360 Q480,420 450,330 Q440,240 460,180 Q440,120 480,80 Z" />
            <path d="M620,80 Q750,60 860,130 Q840,220 760,260 Q720,200 640,180 Z" />
            <path d="M780,320 Q860,310 880,370 Q840,420 780,400 Z" />
          </svg>

          {/* Grid lines */}
          <div className="absolute inset-0 bg-[linear-gradient(to_right,#1E2D4A10_1px,transparent_1px),linear-gradient(to_bottom,#1E2D4A10_1px,transparent_1px)] bg-[size:20px_20px]" />

          {/* Glowing Pinpoint Marker */}
          <div
            className="absolute transform -translate-x-1/2 -translate-y-1/2 flex items-center justify-center transition-all duration-700"
            style={{ left: `${pinX}%`, top: `${pinY}%` }}
          >
            <span className="w-6 h-6 rounded-full bg-red-500/20 animate-ping absolute" />
            <span className="w-3.5 h-3.5 rounded-full bg-red-500/40 border border-red-500 flex items-center justify-center shadow-danger-glow">
              <span className="w-1.5 h-1.5 rounded-full bg-white" />
            </span>
          </div>
        </div>

        {/* Details Grid */}
        <div className="space-y-2 text-xs">
          <div className="flex items-baseline justify-between">
            <span className="text-cyber-muted text-[11px] font-bold uppercase">IP ADDRESS</span>
            <span className="font-mono text-white font-bold">{ip || '—'}</span>
          </div>

          <div className="flex items-baseline justify-between">
            <span className="text-cyber-muted text-[11px] font-bold uppercase">LOCATION</span>
            <span className="text-cyber-text font-medium text-right truncate max-w-[180px]" title={locationString}>
              {locationString}
            </span>
          </div>

          <div className="flex items-baseline justify-between">
            <span className="text-cyber-muted text-[11px] font-bold uppercase">ISP / ORG</span>
            <span className="text-cyber-cyan font-medium text-right truncate max-w-[180px]" title={isp || 'Microsoft Corporation'}>
              {isp || 'Microsoft Corporation'}
            </span>
          </div>

          <div className="flex items-baseline justify-between">
            <span className="text-cyber-muted text-[11px] font-bold uppercase">ASN</span>
            <span className="text-cyber-text-secondary font-mono text-[11px] text-right truncate max-w-[180px]">
              {asn || 'AS8075 Microsoft Corporation'}
            </span>
          </div>
        </div>
      </div>

      <div className="mt-4 pt-3 border-t border-[#1E2D4A]/60 flex justify-end">
        <a
          href={`https://www.google.com/maps/search/?api=1&query=${lat},${lon}`}
          target="_blank"
          rel="noreferrer"
          className="text-xs text-cyber-cyan hover:underline inline-flex items-center gap-1 font-semibold"
        >
          <span>View on Map</span>
          <ExternalLink className="w-3 h-3" />
        </a>
      </div>
    </div>
  );
};
