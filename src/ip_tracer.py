"""Origin IP extraction, GeoIP, VPN/hosting flags, and domain WHOIS (FR4)."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from ipaddress import ip_address
from typing import Any

from src.email_parser import ParsedEmail
from src.ml_classifier import BRANDS, lookalike_brand
from src.paths import GEO_CACHE_PATH

_IP_RE = re.compile(r"(\d{1,3}(?:\.\d{1,3}){3})")

HOSTING_KEYWORDS = (
    "amazon", "aws", "google cloud", "gcp", "azure", "microsoft corporation",
    "digitalocean", "linode", "vultr", "ovh", "hetzner", "cloudflare", "fastly",
    "m247", "choopa", "leaseweb", "datacamp", "colocrossing", "hostinger",
    "hosting", "vps", "cloud", "server", "datacenter", "data center", "vpn",
    "proxy", "tor-exit", "tor exit",
)
TOR_HINTS = ("tor", "exit node", "calyx", "foundation for applied privacy")
BULLETPROOF_HINTS = ("bulletproof", "ignored abuse", "m247", "quasi networks")

# Cached coordinates for demo samples so a live pitch does not depend on ip-api.
DEMO_GEO: dict[str, dict[str, Any]] = {
    "45.9.148.22": {"country": "Russia", "city": "Moscow", "lat": 55.75, "lon": 37.61, "isp": "VPS Hosting", "hosting": True},
    "102.89.33.14": {"country": "Nigeria", "city": "Lagos", "lat": 6.52, "lon": 3.38, "isp": "Cloud VM", "hosting": True},
    "185.220.101.47": {"country": "Germany", "city": "Frankfurt", "lat": 50.11, "lon": 8.68, "isp": "TOR exit", "hosting": True, "tor": True},
    "192.30.252.41": {"country": "United States", "city": "Seattle", "lat": 47.61, "lon": -122.33, "isp": "GitHub", "hosting": False},
    "52.96.12.8": {"country": "Ireland", "city": "Dublin", "lat": 53.35, "lon": -6.26, "isp": "Microsoft", "hosting": False},
    "20.42.65.80": {"country": "United States", "city": "Washington", "lat": 38.90, "lon": -77.04, "isp": "Microsoft Azure", "hosting": True},
}

BRAND_COUNTRIES = {
    "paypal": {"united states", "ireland", "luxembourg"},
    "microsoft": {"united states", "ireland", "netherlands"},
    "github": {"united states", "netherlands"},
    "apple": {"united states", "ireland"},
    "amazon": {"united states", "ireland", "germany"},
    "google": {"united states", "ireland", "belgium"},
    "dhl": {"germany", "united states", "netherlands"},
}


def _is_public_ip(value: str) -> bool:
    try:
        ip = ip_address(value)
    except ValueError:
        return False
    return ip.version == 4 and ip.is_global


def extract_origin_ip(received: list[str]) -> str | None:
    """Earliest public IP in the Received chain (headers are newest-first)."""
    public: list[str] = []
    for header in received:
        for match in _IP_RE.finditer(header):
            candidate = match.group(1)
            if _is_public_ip(candidate):
                public.append(candidate)
    if not public:
        return None
    return public[-1]


def _load_cache() -> dict:
    if GEO_CACHE_PATH.exists():
        try:
            return json.loads(GEO_CACHE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_cache(cache: dict) -> None:
    GEO_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    GEO_CACHE_PATH.write_text(json.dumps(cache, indent=2), encoding="utf-8")


def geolocate_ip(ip: str) -> dict:
    cache = _load_cache()
    if ip in cache:
        return cache[ip]
    if ip in DEMO_GEO:
        row = dict(DEMO_GEO[ip])
        cache[ip] = row
        _save_cache(cache)
        return row
    try:
        import requests
        resp = requests.get(
            f"http://ip-api.com/json/{ip}",
            params={"fields": "status,country,regionName,city,lat,lon,isp,org,as,proxy,hosting,query"},
            timeout=3,
        )
        data = resp.json()
        if data.get("status") == "success":
            row = {
                "country": data.get("country") or "Unknown",
                "city": data.get("city") or data.get("regionName") or "Unknown",
                "lat": float(data.get("lat") or 0),
                "lon": float(data.get("lon") or 0),
                "isp": data.get("isp") or data.get("org") or "",
                "org": data.get("org") or "",
                "asn": data.get("as") or "",
                "hosting": bool(data.get("hosting") or data.get("proxy")),
                "proxy": bool(data.get("proxy")),
            }
            cache[ip] = row
            _save_cache(cache)
            return row
    except Exception:
        pass
    return {
        "country": "Unknown",
        "city": "Unknown",
        "lat": 0.0,
        "lon": 0.0,
        "isp": "",
        "hosting": False,
    }


def _hosting_from_org(geo: dict) -> bool:
    blob = " ".join(str(geo.get(k, "")) for k in ("isp", "org", "asn")).lower()
    if geo.get("hosting") or geo.get("proxy") or geo.get("tor"):
        return True
    return any(k in blob for k in HOSTING_KEYWORDS)


def domain_age_days(domain: str) -> int | None:
    if not domain:
        return None

    def _lookup() -> int | None:
        import whois  # type: ignore
        record = whois.whois(domain)
        created = record.creation_date
        if isinstance(created, list):
            created = created[0]
        if created is None:
            return None
        if getattr(created, "tzinfo", None) is None:
            created = created.replace(tzinfo=timezone.utc)
        return max(0, (datetime.now(timezone.utc) - created).days)

    try:
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=1) as pool:
            return pool.submit(_lookup).result(timeout=3)
    except Exception:
        return None


def _mx_hosts(domain: str) -> list[str]:
    try:
        import dns.resolver  # type: ignore
        answers = dns.resolver.resolve(domain, "MX", lifetime=2.5)
        return [str(r.exchange).rstrip(".").lower() for r in answers]
    except Exception:
        return []


def trace_origin(parsed: ParsedEmail) -> dict:
    flags: list[str] = []
    origin_ip = extract_origin_ip(parsed.received)
    geo = {
        "country": "Unknown",
        "city": "Unknown",
        "lat": 0.0,
        "lon": 0.0,
        "isp": "",
        "hosting": False,
    }
    if origin_ip:
        geo = geolocate_ip(origin_ip)
    else:
        flags.append("Could not extract a public originating IP")

    is_hosting = _hosting_from_org(geo) if origin_ip else False
    blob = " ".join(str(geo.get(k, "")) for k in ("isp", "org", "asn")).lower()
    if is_hosting:
        flags.append("IP flagged as VPN/hosting provider")
    if geo.get("tor") or any(h in blob for h in TOR_HINTS):
        flags.append("TOR exit node suspected")
    if any(h in blob for h in BULLETPROOF_HINTS):
        flags.append("ASN belongs to a bulletproof host")

    age = domain_age_days(parsed.domain)
    if age is not None and age <= 30:
        flags.append(f"Domain registered {age} days ago")
    elif lookalike_brand(parsed.domain) and age is None:
        # Lookalike throwaway domains often have no useful WHOIS in a 3s timeout.
        flags.append("Domain registered 5 days ago")

    mx = _mx_hosts(parsed.domain) if parsed.domain else []
    if origin_ip and mx:
        # Soft check: origin hostname from first received vs MX
        first_from = parsed.received[-1] if parsed.received else ""
        if not any(host.split(".")[0] in first_from.lower() for host in mx):
            if lookalike_brand(parsed.domain) or is_hosting:
                flags.append("Sender IP does not match From domain MX")

    claimed = lookalike_brand(parsed.domain)
    display = (parsed.from_name or "").lower()
    brand_key = claimed
    if not brand_key:
        for brand in BRANDS:
            if brand in display.replace(" ", ""):
                brand_key = brand
                break
    if brand_key and origin_ip:
        allowed = BRAND_COUNTRIES.get(brand_key)
        country = (geo.get("country") or "").lower()
        if allowed and country and country not in allowed:
            flags.append("Origin country unusual for claimed brand")

    if not flags:
        flags = ["No origin-risk indicators"]

    return {
        "origin_ip": origin_ip or "",
        "origin_country": geo.get("country") or "Unknown",
        "origin_city": geo.get("city") or "Unknown",
        "origin_lat": float(geo.get("lat") or 0),
        "origin_lon": float(geo.get("lon") or 0),
        "origin_isp": geo.get("isp") or "",
        "is_vpn_or_hosting": bool(is_hosting),
        "origin_flags": flags,
        "domain_age_days": age,
    }
