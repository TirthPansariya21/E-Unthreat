"""SPF / DKIM / DMARC, Return-Path, and Received-chain forensics (FR3)."""

from __future__ import annotations

import re
from typing import Any

from src.email_parser import ParsedEmail

_AUTH_RE = re.compile(r"(spf|dkim|dmarc)\s*=\s*(pass|fail|none|softfail|neutral|permerror|temperror)", re.I)
_IP_RE = re.compile(r"\[?(\d{1,3}(?:\.\d{1,3}){3})\]?")


def _norm_auth(value: str) -> str:
    value = value.upper()
    if value in {"SOFTFAIL", "NEUTRAL", "PERMERROR", "TEMPERROR"}:
        return "FAIL"
    return value


def _from_auth_results(headers: dict[str, str]) -> dict[str, str]:
    blob = " ".join(v for k, v in headers.items() if k.lower() in {"authentication-results", "arc-authentication-results"})
    found: dict[str, str] = {}
    for match in _AUTH_RE.finditer(blob):
        found[match.group(1).lower()] = _norm_auth(match.group(2))
    return found


def _txt_records(name: str) -> list[str]:
    try:
        import dns.resolver  # type: ignore
    except Exception:
        return []
    try:
        answers = dns.resolver.resolve(name, "TXT", lifetime=2.5)
        return [b"".join(r.strings).decode("utf-8", errors="replace") for r in answers]
    except Exception:
        return []


def _spf_from_dns(domain: str) -> str | None:
    if not domain:
        return None
    records = _txt_records(domain)
    if any("v=spf1" in r.lower() for r in records):
        return "PRESENT"
    return "ABSENT" if records == [] else "ABSENT"


def _dmarc_from_dns(domain: str) -> str | None:
    if not domain:
        return None
    records = _txt_records(f"_dmarc.{domain}")
    for rec in records:
        if "v=DMARC1" in rec.upper():
            return rec
    return None


def reconstruct_relay(received: list[str]) -> list[str]:
    hops: list[str] = []
    for header in reversed(received):
        from_match = re.search(r"from\s+([^\s\(]+)", header, re.I)
        by_match = re.search(r"by\s+([^\s\(]+)", header, re.I)
        ip_match = re.search(r"\[(\d{1,3}(?:\.\d{1,3}){3})\]", header)
        if ip_match and from_match:
            hops.append(f"{ip_match.group(1)} ({from_match.group(1)})")
        elif ip_match:
            hops.append(f"{ip_match.group(1)} (unknown relay)")
        elif from_match:
            hops.append(from_match.group(1))
        elif by_match:
            hops.append(by_match.group(1))
    if hops and "recipient" not in hops[-1].lower():
        hops.append("recipient mail server")
    return hops


def _try_dkim_verify(raw: str, msg: Any) -> str | None:
    if msg is None or not msg.get("DKIM-Signature"):
        return None
    try:
        import dkim  # type: ignore
    except Exception:
        return None
    try:
        ok = dkim.verify(raw.encode("utf-8", errors="replace"))
        return "PASS" if ok else "FAIL"
    except Exception:
        return None


def analyze_headers(parsed: ParsedEmail) -> dict:
    auth = _from_auth_results(parsed.headers)
    has_auth = any(k.lower() in {"authentication-results", "arc-authentication-results"} for k in parsed.headers)

    spf = auth.get("spf")
    dkim = auth.get("dkim")
    dmarc = auth.get("dmarc")

    warnings: list[str] = []
    if spf is None:
        dns_spf = _spf_from_dns(parsed.domain)
        if dns_spf == "ABSENT":
            spf = "NONE"
        elif dns_spf == "PRESENT":
            spf = "NONE"
            warnings.append("SPF record exists but could not be evaluated against the sending IP (no Authentication-Results).")
        else:
            spf = "NONE"
    if dkim is None:
        verified = _try_dkim_verify(parsed.raw, parsed.msg)
        if verified:
            dkim = verified
        elif parsed.msg is not None and parsed.msg.get("DKIM-Signature"):
            dkim = "NONE"
            warnings.append("DKIM-Signature present but cryptographic verification could not be completed.")
        else:
            dkim = "NONE"
    if dmarc is None:
        policy = _dmarc_from_dns(parsed.domain)
        if policy is None:
            dmarc = "NONE"
        elif spf == "PASS" or dkim == "PASS":
            dmarc = "PASS"
        elif spf == "FAIL" and dkim == "FAIL":
            dmarc = "FAIL"
        else:
            dmarc = "NONE"

    flags = [f"SPF: {spf}", f"DKIM: {dkim}", f"DMARC: {dmarc}"]
    rp = (parsed.return_path or "").lower()
    frm = (parsed.from_addr or "").lower()
    if rp and frm and rp != frm:
        flags.append("Return-Path mismatch with From address")
    if not has_auth:
        flags.append("Missing Authentication-Results header")

    mid_domain = ""
    mid_match = re.search(r"@([^>]+)", parsed.message_id)
    if mid_match:
        mid_domain = mid_match.group(1).lower().strip()
    if parsed.domain and mid_domain and parsed.domain not in mid_domain and mid_domain not in parsed.domain:
        flags.append("Message-ID domain does not match From domain")

    relay = reconstruct_relay(parsed.received)
    if not relay:
        relay = ["(no Received headers)"]

    return {
        "spf_result": spf,
        "dkim_result": dkim,
        "dmarc_result": dmarc,
        "header_flags": flags,
        "relay_path": relay,
        "warnings": warnings,
    }
