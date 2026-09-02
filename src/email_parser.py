"""RFC 822 / .eml parser → structured object (FR1)."""

from __future__ import annotations

import email
import re
from dataclasses import dataclass, field
from email import policy
from email.utils import parseaddr
from html import unescape
from typing import Any


@dataclass
class ParsedEmail:
    raw: str
    from_name: str = ""
    from_addr: str = ""
    to: str = ""
    subject: str = ""
    date: str = ""
    body: str = ""
    html_body: str = ""
    headers: dict[str, str] = field(default_factory=dict)
    received: list[str] = field(default_factory=list)
    attachments: list[str] = field(default_factory=list)
    message_id: str = ""
    return_path: str = ""
    parse_warning: str | None = None
    msg: Any = None

    @property
    def domain(self) -> str:
        if "@" in self.from_addr:
            return self.from_addr.rsplit("@", 1)[-1].lower().strip()
        return ""

    @property
    def combined_text(self) -> str:
        return f"{self.subject}\n{self.body}"


def _strip_html(html: str) -> str:
    text = re.sub(r"(?is)<script.*?>.*?</script>", " ", html)
    text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
    text = re.sub(r"(?is)<br\s*/?>", "\n", text)
    text = re.sub(r"(?is)</p>", "\n", text)
    text = re.sub(r"(?is)<[^>]+>", " ", text)
    return unescape(re.sub(r"\s+", " ", text)).strip()


def _decode_part(part) -> str:
    try:
        content = part.get_content()
        return content if isinstance(content, str) else str(content)
    except Exception:
        payload = part.get_payload(decode=True) or b""
        if isinstance(payload, bytes):
            return payload.decode(part.get_content_charset() or "utf-8", errors="replace")
        return str(payload)


def parse_email(raw_eml_text: str) -> ParsedEmail:
    raw = raw_eml_text or ""
    warning = None
    msg = None
    try:
        msg = email.message_from_string(raw, policy=policy.default)
    except Exception:
        try:
            msg = email.message_from_string(raw, policy=policy.compat32)
            warning = "Partial analysis: malformed MIME"
        except Exception:
            parsed = ParsedEmail(raw=raw, parse_warning="Partial analysis: malformed MIME")
            parsed.body = raw
            parsed.subject = "(unparseable)"
            parsed.from_addr = "unknown"
            return parsed

    from_header = str(msg.get("From", "") or "")
    name, addr = parseaddr(from_header)
    body_plain: list[str] = []
    body_html: list[str] = []
    attachments: list[str] = []

    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disp = str(part.get_content_disposition() or "")
            filename = part.get_filename()
            if filename:
                attachments.append(str(filename))
                continue
            if disp == "attachment":
                attachments.append(part.get_content_type())
                continue
            if ctype == "text/plain":
                body_plain.append(_decode_part(part))
            elif ctype == "text/html":
                body_html.append(_decode_part(part))
    else:
        ctype = msg.get_content_type()
        if ctype == "text/html":
            body_html.append(_decode_part(msg))
        else:
            body_plain.append(_decode_part(msg))

    html = "\n".join(body_html)
    plain = "\n".join(body_plain).strip() or _strip_html(html)

    headers = {}
    for key, value in msg.items():
        headers[key] = str(value)

    return ParsedEmail(
        raw=raw,
        from_name=name or "",
        from_addr=(addr or from_header or "unknown").strip(),
        to=str(msg.get("To", "") or ""),
        subject=(str(msg.get("Subject") or "") or "(no subject)").strip(),
        date=str(msg.get("Date", "") or ""),
        body=plain,
        html_body=html,
        headers=headers,
        received=[str(h) for h in (msg.get_all("Received") or [])],
        attachments=attachments,
        message_id=str(msg.get("Message-ID", "") or ""),
        return_path=str(msg.get("Return-Path", "") or "").strip("<> "),
        parse_warning=warning,
        msg=msg,
    )
