"""Single entry point: analyze_email(raw_eml) → forensic result dict."""

from __future__ import annotations

from src.content_signals import extra_content_flags, lookalike_hit
from src.email_parser import parse_email
from src.explanations import explain_flag
from src.header_forensics import analyze_headers
from src.ip_tracer import trace_origin
from src.ml_classifier import classify_content, lookalike_brand


def _verdict_from_score(score: int) -> str:
    if score >= 70:
        return "Phishing"
    if score >= 40:
        return "Suspicious"
    return "Legitimate"


def analyze_email(raw_eml: str) -> dict:
    """Run NLP + header forensics + origin tracing and return the dashboard bundle.

    Shape is stable so the Streamlit UI can swap implementations without changes.
    """
    warnings: list[str] = []
    try:
        parsed = parse_email(raw_eml)
    except Exception as exc:
        parsed = parse_email("")
        parsed.body = raw_eml or ""
        parsed.parse_warning = "Partial analysis: malformed MIME"
        warnings.append(f"Parser recovered from {exc.__class__.__name__}")

    if parsed.parse_warning:
        warnings.append(parsed.parse_warning)

    nlp = classify_content(parsed)
    headers = analyze_headers(parsed)
    origin = trace_origin(parsed)
    warnings.extend(headers.get("warnings") or [])

    content_flags = [f for f in nlp["content_flags"] if f]
    for flag in extra_content_flags(parsed):
        if flag not in content_flags:
            content_flags.append(flag)
    header_flags = headers["header_flags"]
    origin_flags = origin["origin_flags"]

    auth_fails = sum(1 for v in (headers["spf_result"], headers["dkim_result"], headers["dmarc_result"]) if v == "FAIL")
    auth_pass = {headers["spf_result"], headers["dkim_result"], headers["dmarc_result"]} == {"PASS"}
    risk_content = [f for f in content_flags if not f.startswith("No content") and not f.startswith("ML classifier")]
    risk_origin = [f for f in origin_flags if not f.startswith("No origin")]

    p_phish = float(nlp.get("ml_p_phishing") or 0)
    # ML is weighted above per-keyword flags (55 vs 40) so a confident model
    # call still moves the needle when the rule list has never seen this brand
    # or phrasing. Empty-rule floor: P>=0.60 can reach the Suspicious band
    # by itself instead of collapsing to ~20 points.
    ml_term = int(round(55 * p_phish)) if nlp.get("ml_available") else 0
    if nlp.get("ml_available") and p_phish >= 0.60 and len(risk_content) == 0 and not auth_pass:
        ml_term = max(ml_term, int(round(48 + 30 * (p_phish - 0.60))))
    rule_term = min(40, 8 * len(risk_content))
    header_term = 10 * auth_fails + 3 * sum(1 for f in header_flags if f.startswith("Return-Path") or f.startswith("Missing") or f.startswith("Message-ID"))
    origin_term = min(30, 7 * len(risk_origin))
    score = ml_term + rule_term + header_term + origin_term

    severe = any(
        f in content_flags
        for f in (
            "Lookalike domain detected",
            "Request for payment / gift cards",
            "Brand impersonation in display name",
            "Suspicious link to lookalike domain",
        )
    ) or lookalike_brand(parsed.domain) or lookalike_hit(parsed.domain)
    # Three independent axes: auth failure, risky content, hostile origin.
    # Any one or two of these can still land Suspicious; all three together is phishing.
    stacked = (
        auth_fails >= 2
        and len(risk_content) >= 2
        and any(
            f.startswith("IP flagged as VPN") or f.startswith("TOR")
            for f in origin_flags
        )
    )
    if severe:
        score = max(score, 74)
    if stacked:
        score = max(score, 74)
    if auth_pass and not severe and not stacked and len(risk_content) <= 1:
        score = min(max(score, 8), 22)
    if not severe and not stacked and not auth_pass and 2 <= len(risk_content) <= 3:
        score = min(max(score, 42), 68)

    score = max(4, min(98, int(score)))
    verdict = _verdict_from_score(score)

    if verdict == "Legitimate" and not risk_content:
        content_flags = ["No content anomalies detected"]
    if verdict == "Legitimate" and not risk_origin:
        origin_flags = ["No origin-risk indicators"]

    return {
        "verdict": verdict,
        "fraud_score": score,
        "content_flags": content_flags,
        "header_flags": header_flags,
        "origin_flags": origin_flags,
        "origin_country": origin["origin_country"],
        "origin_city": origin["origin_city"],
        "origin_lat": origin["origin_lat"],
        "origin_lon": origin["origin_lon"],
        "relay_path": headers["relay_path"],
        "sender": parsed.from_addr,
        "subject": parsed.subject,
        "origin_ip": origin["origin_ip"],
        "spf_result": headers["spf_result"],
        "dkim_result": headers["dkim_result"],
        "dmarc_result": headers["dmarc_result"],
        "is_vpn_or_hosting": origin["is_vpn_or_hosting"],
        "ml_label": nlp["ml_label"],
        "ml_confidence": nlp["ml_confidence"],
        "ml_available": nlp["ml_available"],
        "attachments": parsed.attachments,
        "warnings": warnings,
        "from_name": parsed.from_name,
        "to": parsed.to,
        "origin_isp": origin.get("origin_isp") or "",
    }


# Re-exported for the dashboard PDF/UI.
__all__ = ["analyze_email", "explain_flag"]
