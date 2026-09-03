"""Lookalike-domain and body-link checks used by the fraud aggregator.

Kept separate from ml_classifier.py so the trained model and its rule list stay frozen.
"""

from __future__ import annotations

import re
from urllib.parse import urlparse

from src.email_parser import ParsedEmail

# Maps a brand token to domains that organisation actually sends mail / hosts from.
BRAND_OFFICIAL: dict[str, tuple[str, ...]] = {
    "paypal": ("paypal.com", "paypal.me", "py.pl"),
    "microsoft": (
        "microsoft.com",
        "microsoftonline.com",
        "office.com",
        "live.com",
        "aka.ms",
        "outlook.com",
        "azure.com",
    ),
    "apple": ("apple.com", "icloud.com", "me.com"),
    "amazon": ("amazon.com", "amazon.in", "amzn.to", "a.co"),
    "google": ("google.com", "gmail.com", "youtube.com", "g.co", "googleusercontent.com"),
    "facebook": ("facebook.com", "fb.com", "meta.com", "messenger.com"),
    "instagram": ("instagram.com",),
    "netflix": ("netflix.com",),
    "linkedin": ("linkedin.com", "lnkd.in"),
    "github": ("github.com", "github.io", "githubusercontent.com"),
    "wellsfargo": ("wellsfargo.com",),
    "chase": ("chase.com",),
    "bankofamerica": ("bankofamerica.com", "bofa.com"),
    "dhl": ("dhl.com", "dhl.de"),
    "fedex": ("fedex.com",),
    "ups": ("ups.com",),
    "adobe": ("adobe.com",),
    "dropbox": ("dropbox.com", "db.tt"),
    "whatsapp": ("whatsapp.com", "wa.me"),
    "hdfc": ("hdfcbank.com", "hdfc.com"),
    "hdfcbank": ("hdfcbank.com",),
    "sbi": ("onlinesbi.sbi", "sbi.co.in", "sbi.com"),
    "icici": ("icicibank.com",),
    "axis": ("axisbank.com",),
    "kotak": ("kotak.com", "kotakbank.com"),
    "paytm": ("paytm.com",),
    "phonepe": ("phonepe.com",),
}

# Extra tokens that turn "brand + filler" into a credential-harvesting lure.
# Deliberately excludes shipping words like "parcel" / "status" so DHL-style
# suspicious (not phishing) samples are not auto-promoted.
BAIT_TOKENS = {
    "secure",
    "login",
    "account",
    "verify",
    "support",
    "alert",
    "security",
    "notify",
    "signin",
    "sign-in",
    "netbanking",
    "banking",
    "update",
    "confirm",
    "unlock",
    "password",
    "validation",
    "authenticate",
    "webmail",
    "portal",
    "careers",
    "career",
    "claim",
    "rewards",
    "reward",
}

# Tokens that look like infrastructure or marketing, not a company name.
GENERIC_TOKENS = {
    "mail",
    "email",
    "info",
    "news",
    "update",
    "updates",
    "online",
    "official",
    "service",
    "services",
    "customer",
    "welcome",
    "noreply",
    "message",
    "notification",
    "system",
    "server",
    "host",
    "web",
    "site",
    "domain",
    "contact",
    "help",
    "desk",
    "team",
    "http",
    "https",
    "www",
    "cloud",
    "data",
    "tech",
    "digital",
    "global",
    "world",
    "india",
    "best",
    "free",
    "new",
    "real",
    "true",
    "smart",
    "super",
    "plus",
    "pro",
    "net",
    "app",
    "mega",
    "top",
    "fast",
    "my",
    "the",
    "get",
    "shop",
    "store",
    "deals",
    "offer",
    "offers",
    "sale",
    "promo",
    "marketing",
    "newsletter",
    "billing",
    "invoice",
    "order",
    "orders",
    "shipping",
    "parcel",
    "status",
    "package",
    "delivery",
    "track",
    "tracking",
    "hosting",
    "network",
}

URL_RE = re.compile(r"https?://[^\s<>\"')\]]+", re.I)
HREF_RE = re.compile(r"""href\s*=\s*['"]([^'"]+)['"]""", re.I)


def _levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        curr = [i]
        for j, cb in enumerate(b, 1):
            curr.append(min(curr[j - 1] + 1, prev[j] + 1, prev[j - 1] + (ca != cb)))
        prev = curr
    return prev[-1]


def _normalize(value: str) -> str:
    table = str.maketrans({"0": "o", "1": "l", "3": "e", "4": "a", "5": "s", "7": "t"})
    return value.lower().replace("-", "").replace("_", "").translate(table)


def _strip_www(host: str) -> str:
    host = (host or "").lower().split(":")[0].strip().strip(".")
    if host.startswith("www."):
        host = host[4:]
    return host


def _host_is_official(host: str, officials: tuple[str, ...]) -> bool:
    host = _strip_www(host)
    if not host:
        return False
    for official in officials:
        if host == official or host.endswith("." + official):
            return True
    return False


def _is_known_official_host(host: str) -> bool:
    return any(_host_is_official(host, officials) for officials in BRAND_OFFICIAL.values())


def _is_brand_shaped(token: str) -> bool:
    """Company-name-like label: 5+ letters, not bait, not generic filler."""
    t = _normalize(token)
    if len(t) < 5:
        return False
    if t in BAIT_TOKENS or t in GENERIC_TOKENS:
        return False
    if not re.fullmatch(r"[a-z][a-z0-9]+", t):
        return False
    return sum(c.isalpha() for c in t) >= 4


def generic_lure_brand(domain: str) -> str | None:
    """Flag brand-shaped + bait domains even when the brand is not in our list.

    infosys-careers-portal.com and flipkart-rewards-claim.com match.
    github.com, myntra.com, and dhl-parcel-status.com do not.
    """
    host = _strip_www(domain)
    if not host or _is_known_official_host(host):
        return None
    sld = host.split(".")[0]
    tokens = [t for t in re.split(r"[-_]", sld) if t]
    bait_tokens = [t for t in tokens if _normalize(t) in BAIT_TOKENS or t.lower() in BAIT_TOKENS]
    shaped = [t for t in tokens if _is_brand_shaped(t)]
    if bait_tokens and shaped:
        return shaped[0].lower()

    compact_n = _normalize(sld)
    for bait in sorted((b for b in BAIT_TOKENS if len(b) >= 6), key=len, reverse=True):
        if bait not in compact_n:
            continue
        remainder = compact_n.replace(bait, "", 1)
        if _is_brand_shaped(remainder):
            return remainder
    return None


def lookalike_hit(domain: str) -> str | None:
    """Known-brand impersonation or generic brand-shaped + bait lure."""
    return impersonated_brand(domain) or generic_lure_brand(domain)


def impersonated_brand(domain: str) -> str | None:
    """Return the listed brand a From/link host is impersonating, or None.

    Matches:
    - hyphenated lures like hdfc-netbanking-verify.com (brand token + bait)
    - homographs / typos (paypa1, micros0ft) via edit distance
    - brand.tld that is not the organisation's real domain (paypal.tk)
    Does not match official domains, or brand+benign filler (dhl-parcel-status).
    """
    host = _strip_www(domain)
    if not host or _is_known_official_host(host):
        return None

    sld = host.split(".")[0]
    tokens = [t for t in re.split(r"[-_]", sld) if t]
    compact = sld.replace("-", "").replace("_", "")
    bait_hit = any(_normalize(t) in BAIT_TOKENS or t.lower() in BAIT_TOKENS for t in tokens)
    bait_hit = bait_hit or any(bait in _normalize(compact) for bait in BAIT_TOKENS)

    for brand, officials in BRAND_OFFICIAL.items():
        if _host_is_official(host, officials):
            continue
        brand_key = _normalize(brand)
        if not brand_key:
            continue
        first = _normalize(tokens[0]) if tokens else ""
        compact_n = _normalize(compact)

        if compact_n.startswith(brand_key) and len(compact_n) > len(brand_key) and bait_hit:
            return brand
        if brand_key in [_normalize(t) for t in tokens] and bait_hit:
            return brand
        if len(brand_key) >= 4 and len(compact_n) >= 4 and compact_n != brand_key:
            if _levenshtein(compact_n, brand_key) <= 2:
                return brand
        if len(brand_key) >= 4 and len(first) >= 4 and first != brand_key:
            if _levenshtein(first, brand_key) <= 2:
                return brand
        if compact_n == brand_key or (len(tokens) == 1 and first == brand_key):
            return brand
    return None


def claimed_brand(parsed: ParsedEmail) -> str | None:
    """Brand the message pretends to be, from display name / subject / From host."""
    from_brand = lookalike_hit(parsed.domain)
    if from_brand:
        return from_brand
    blob = f"{parsed.from_name} {parsed.subject}".lower()
    compact = re.sub(r"[^a-z0-9]", "", blob)
    # Longer keys first so hdfcbank wins over hdfc when both present.
    for brand in sorted(BRAND_OFFICIAL, key=len, reverse=True):
        if brand in blob.replace(" ", "") or brand in compact:
            return brand
    return None


def _iter_urls(parsed: ParsedEmail) -> list[str]:
    blob = f"{parsed.subject}\n{parsed.body}\n{parsed.html_body}"
    found = URL_RE.findall(blob)
    found.extend(HREF_RE.findall(parsed.html_body or ""))
    return list(dict.fromkeys(found))


def _url_host(url: str) -> str:
    raw = (url or "").strip()
    if not raw or raw.lower().startswith(("mailto:", "javascript:", "#")):
        return ""
    if "://" not in raw:
        raw = "https://" + raw
    try:
        host = urlparse(raw).hostname or ""
    except Exception:
        host = ""
    return _strip_www(host)


def _same_site(host: str, domain: str) -> bool:
    host, domain = _strip_www(host), _strip_www(domain)
    if not host or not domain:
        return False
    return host == domain or host.endswith("." + domain) or domain.endswith("." + host)


def extra_content_flags(parsed: ParsedEmail) -> list[str]:
    """Lookalike From-domain and untrusted body-link flags (deduped, stable order)."""
    flags: list[str] = []
    if lookalike_hit(parsed.domain):
        flags.append("Lookalike domain detected")

    brand = claimed_brand(parsed)
    officials = BRAND_OFFICIAL.get(brand or "", ())
    from_is_official = bool(brand and officials and _host_is_official(parsed.domain, officials))

    for url in _iter_urls(parsed):
        host = _url_host(url)
        if not host:
            continue
        if lookalike_hit(host):
            flags.append("Suspicious link to lookalike domain")
            break
        if brand and officials and not from_is_official:
            if not _host_is_official(host, officials) and not _same_site(host, parsed.domain):
                flags.append("Link domain does not match claimed sender")
                break
            if not _host_is_official(host, officials) and _same_site(host, parsed.domain):
                # From host and link share a lure domain that is not the real brand.
                flags.append("Link domain does not match claimed sender")
                break

    return list(dict.fromkeys(flags))
