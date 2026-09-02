"""Local SQLite persistence for analyzed email cases."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from src.paths import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    sender TEXT,
    subject TEXT,
    verdict TEXT,
    fraud_score INTEGER,
    spf_result TEXT,
    dkim_result TEXT,
    dmarc_result TEXT,
    origin_ip TEXT,
    origin_country TEXT,
    origin_city TEXT,
    is_vpn_or_hosting INTEGER,
    flags_json TEXT,
    analyzed_at TEXT
);
"""

SEED_CASES = [
    {
        "filename": "paypal_security_alert.eml",
        "sender": "service@paypa1-secure.com",
        "subject": "Your account will be locked in 12 hours",
        "verdict": "Phishing",
        "fraud_score": 91,
        "spf_result": "FAIL",
        "dkim_result": "FAIL",
        "dmarc_result": "FAIL",
        "origin_ip": "45.9.148.22",
        "origin_country": "Russia",
        "origin_city": "Moscow",
        "is_vpn_or_hosting": 1,
        "analyzed_at_offset_hours": 26,
        "result": {
            "verdict": "Phishing",
            "fraud_score": 91,
            "content_flags": [
                "Urgency language detected",
                "Suspicious shortened link found",
                "Lookalike domain detected",
                "Credential harvesting language",
            ],
            "header_flags": [
                "SPF: FAIL",
                "DKIM: FAIL",
                "DMARC: FAIL",
                "Return-Path mismatch with From address",
            ],
            "origin_flags": [
                "IP flagged as VPN/hosting provider",
                "Domain registered 3 days ago",
                "Origin country unusual for claimed brand",
            ],
            "origin_country": "Russia",
            "origin_city": "Moscow",
            "origin_lat": 55.75,
            "origin_lon": 37.61,
            "relay_path": [
                "45.9.148.22 (unknown relay)",
                "mail.paypa1-secure.com",
                "recipient mail server",
            ],
            "sender": "service@paypa1-secure.com",
            "subject": "Your account will be locked in 12 hours",
            "origin_ip": "45.9.148.22",
            "spf_result": "FAIL",
            "dkim_result": "FAIL",
            "dmarc_result": "FAIL",
            "is_vpn_or_hosting": True,
        },
    },
    {
        "filename": "ceo_wire_request.eml",
        "sender": "robert.chen@company-mailer.net",
        "subject": "URGENT: process this wire before close of business",
        "verdict": "Phishing",
        "fraud_score": 84,
        "spf_result": "FAIL",
        "dkim_result": "NONE",
        "dmarc_result": "FAIL",
        "origin_ip": "102.89.33.14",
        "origin_country": "Nigeria",
        "origin_city": "Lagos",
        "is_vpn_or_hosting": 1,
        "analyzed_at_offset_hours": 18,
        "result": {
            "verdict": "Phishing",
            "fraud_score": 84,
            "content_flags": [
                "Urgency language detected",
                "Brand impersonation in display name",
                "Request for payment / gift cards",
            ],
            "header_flags": [
                "SPF: FAIL",
                "DKIM: NONE",
                "DMARC: FAIL",
                "Message-ID domain does not match From domain",
            ],
            "origin_flags": [
                "IP flagged as VPN/hosting provider",
                "Domain registered 5 days ago",
                "ASN belongs to a bulletproof host",
            ],
            "origin_country": "Nigeria",
            "origin_city": "Lagos",
            "origin_lat": 6.52,
            "origin_lon": 3.38,
            "relay_path": [
                "102.89.33.14 (unknown relay)",
                "smtp.company-mailer.net",
                "mx.corporate-gateway.net",
                "recipient mail server",
            ],
            "sender": "robert.chen@company-mailer.net",
            "subject": "URGENT: process this wire before close of business",
            "origin_ip": "102.89.33.14",
            "spf_result": "FAIL",
            "dkim_result": "NONE",
            "dmarc_result": "FAIL",
            "is_vpn_or_hosting": True,
        },
    },
    {
        "filename": "shipping_invoice.eml",
        "sender": "notices@dhl-parcel-status.com",
        "subject": "Invoice attached — outstanding customs fee",
        "verdict": "Suspicious",
        "fraud_score": 58,
        "spf_result": "NONE",
        "dkim_result": "FAIL",
        "dmarc_result": "NONE",
        "origin_ip": "185.220.101.47",
        "origin_country": "Germany",
        "origin_city": "Frankfurt",
        "is_vpn_or_hosting": 1,
        "analyzed_at_offset_hours": 9,
        "result": {
            "verdict": "Suspicious",
            "fraud_score": 58,
            "content_flags": [
                "Suspicious attachment reference",
                "Generic greeting with sensitive ask",
            ],
            "header_flags": [
                "SPF: NONE",
                "DKIM: FAIL",
                "DMARC: NONE",
                "Missing Authentication-Results header",
            ],
            "origin_flags": [
                "IP flagged as VPN/hosting provider",
                "Domain registered 12 days ago",
            ],
            "origin_country": "Germany",
            "origin_city": "Frankfurt",
            "origin_lat": 50.11,
            "origin_lon": 8.68,
            "relay_path": [
                "185.220.101.47 (tor-exit.example.net)",
                "mail.dhl-parcel-status.com",
                "recipient mail server",
            ],
            "sender": "notices@dhl-parcel-status.com",
            "subject": "Invoice attached — outstanding customs fee",
            "origin_ip": "185.220.101.47",
            "spf_result": "NONE",
            "dkim_result": "FAIL",
            "dmarc_result": "NONE",
            "is_vpn_or_hosting": True,
        },
    },
    {
        "filename": "github_signin.eml",
        "sender": "noreply@github.com",
        "subject": "[GitHub] A new sign-in to your account",
        "verdict": "Legitimate",
        "fraud_score": 11,
        "spf_result": "PASS",
        "dkim_result": "PASS",
        "dmarc_result": "PASS",
        "origin_ip": "192.30.252.41",
        "origin_country": "United States",
        "origin_city": "Seattle",
        "is_vpn_or_hosting": 0,
        "analyzed_at_offset_hours": 4,
        "result": {
            "verdict": "Legitimate",
            "fraud_score": 11,
            "content_flags": ["No content anomalies detected"],
            "header_flags": ["SPF: PASS", "DKIM: PASS", "DMARC: PASS"],
            "origin_flags": ["No origin-risk indicators"],
            "origin_country": "United States",
            "origin_city": "Seattle",
            "origin_lat": 47.61,
            "origin_lon": -122.33,
            "relay_path": [
                "192.30.252.41 (out-17.smtp.github.com)",
                "mx.google.com",
                "recipient mail server",
            ],
            "sender": "noreply@github.com",
            "subject": "[GitHub] A new sign-in to your account",
            "origin_ip": "192.30.252.41",
            "spf_result": "PASS",
            "dkim_result": "PASS",
            "dmarc_result": "PASS",
            "is_vpn_or_hosting": False,
        },
    },
    {
        "filename": "hr_benefits_update.eml",
        "sender": "benefits@contoso.com",
        "subject": "Open enrolment reminder — no action required yet",
        "verdict": "Legitimate",
        "fraud_score": 17,
        "spf_result": "PASS",
        "dkim_result": "PASS",
        "dmarc_result": "PASS",
        "origin_ip": "52.96.12.8",
        "origin_country": "Ireland",
        "origin_city": "Dublin",
        "is_vpn_or_hosting": 0,
        "analyzed_at_offset_hours": 1,
        "result": {
            "verdict": "Legitimate",
            "fraud_score": 17,
            "content_flags": ["No content anomalies detected"],
            "header_flags": ["SPF: PASS", "DKIM: PASS", "DMARC: PASS"],
            "origin_flags": ["No origin-risk indicators"],
            "origin_country": "Ireland",
            "origin_city": "Dublin",
            "origin_lat": 53.35,
            "origin_lon": -6.26,
            "relay_path": [
                "52.96.12.8 (mail-ireland.contoso.com)",
                "protection.outlook.com",
                "recipient mail server",
            ],
            "sender": "benefits@contoso.com",
            "subject": "Open enrolment reminder — no action required yet",
            "origin_ip": "52.96.12.8",
            "spf_result": "PASS",
            "dkim_result": "PASS",
            "dmarc_result": "PASS",
            "is_vpn_or_hosting": False,
        },
    },
]


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.execute(SCHEMA)
        count = conn.execute("SELECT COUNT(*) AS n FROM cases").fetchone()["n"]
        if count:
            return
        now = datetime.now(timezone.utc)
        for seed in SEED_CASES:
            analyzed_at = (now - timedelta(hours=seed["analyzed_at_offset_hours"])).strftime(
                "%Y-%m-%d %H:%M:%S UTC"
            )
            result = dict(seed["result"])
            result["filename"] = seed["filename"]
            result["analyzed_at"] = analyzed_at
            conn.execute(
                """
                INSERT INTO cases (
                    filename, sender, subject, verdict, fraud_score,
                    spf_result, dkim_result, dmarc_result, origin_ip,
                    origin_country, origin_city, is_vpn_or_hosting,
                    flags_json, analyzed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    seed["filename"],
                    seed["sender"],
                    seed["subject"],
                    seed["verdict"],
                    seed["fraud_score"],
                    seed["spf_result"],
                    seed["dkim_result"],
                    seed["dmarc_result"],
                    seed["origin_ip"],
                    seed["origin_country"],
                    seed["origin_city"],
                    seed["is_vpn_or_hosting"],
                    json.dumps(result),
                    analyzed_at,
                ),
            )


def save_case(filename: str, result: dict) -> int:
    analyzed_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    payload = dict(result)
    payload["filename"] = filename
    payload["analyzed_at"] = analyzed_at
    with _connect() as conn:
        cursor = conn.execute(
            """
            INSERT INTO cases (
                filename, sender, subject, verdict, fraud_score,
                spf_result, dkim_result, dmarc_result, origin_ip,
                origin_country, origin_city, is_vpn_or_hosting,
                flags_json, analyzed_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                filename,
                result.get("sender") or "unknown",
                result.get("subject") or "(no subject)",
                result["verdict"],
                int(result["fraud_score"]),
                result.get("spf_result") or "NONE",
                result.get("dkim_result") or "NONE",
                result.get("dmarc_result") or "NONE",
                result.get("origin_ip") or "",
                result.get("origin_country") or "",
                result.get("origin_city") or "",
                1 if result.get("is_vpn_or_hosting") else 0,
                json.dumps(payload),
                analyzed_at,
            ),
        )
        return int(cursor.lastrowid)


def list_cases() -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT id, filename, sender, subject, verdict, fraud_score,
                   origin_country, analyzed_at
            FROM cases
            ORDER BY id DESC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def get_case(case_id: int) -> dict | None:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM cases WHERE id = ?", (case_id,)).fetchone()
    if row is None:
        return None
    record = dict(row)
    flags = json.loads(record["flags_json"] or "{}")
    flags.update(
        {
            "id": record["id"],
            "filename": record["filename"],
            "sender": record["sender"],
            "subject": record["subject"],
            "verdict": record["verdict"],
            "fraud_score": record["fraud_score"],
            "spf_result": record["spf_result"],
            "dkim_result": record["dkim_result"],
            "dmarc_result": record["dmarc_result"],
            "origin_ip": record["origin_ip"],
            "origin_country": record["origin_country"],
            "origin_city": record["origin_city"],
            "is_vpn_or_hosting": bool(record["is_vpn_or_hosting"]),
            "analyzed_at": record["analyzed_at"],
        }
    )
    return flags


def case_stats() -> dict:
    with _connect() as conn:
        total = conn.execute("SELECT COUNT(*) AS n FROM cases").fetchone()["n"]
        phishing = conn.execute(
            "SELECT COUNT(*) AS n FROM cases WHERE verdict = 'Phishing'"
        ).fetchone()["n"]
        suspicious = conn.execute(
            "SELECT COUNT(*) AS n FROM cases WHERE verdict = 'Suspicious'"
        ).fetchone()["n"]
        legitimate = conn.execute(
            "SELECT COUNT(*) AS n FROM cases WHERE verdict = 'Legitimate'"
        ).fetchone()["n"]
        avg_row = conn.execute("SELECT AVG(fraud_score) AS a FROM cases").fetchone()
    avg_score = avg_row["a"] or 0
    return {
        "total": total,
        "phishing": phishing,
        "suspicious": suspicious,
        "legitimate": legitimate,
        "avg_score": round(float(avg_score), 1),
    }
