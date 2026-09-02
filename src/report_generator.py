"""Generate a downloadable forensic PDF report for a case."""

from __future__ import annotations

import io
from datetime import datetime, timezone

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from xml.sax.saxutils import escape as xml_escape
from reportlab.platypus import (
    HRFlowable,
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

NAVY = colors.HexColor("#0b1220")
TEAL = colors.HexColor("#00d4aa")
SLATE = colors.HexColor("#334155")
LIGHT = colors.HexColor("#f8fafc")
MUTED = colors.HexColor("#64748b")
VERDICT_COLORS = {
    "Phishing": colors.HexColor("#dc2626"),
    "Suspicious": colors.HexColor("#d97706"),
    "Legitimate": colors.HexColor("#16a34a"),
}


def _styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "brand": ParagraphStyle(
            "brand",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=11,
            textColor=TEAL,
            tracking=1,
        ),
        "title": ParagraphStyle(
            "title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=18,
            textColor=NAVY,
            spaceAfter=2,
            alignment=TA_LEFT,
        ),
        "meta": ParagraphStyle(
            "meta",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            textColor=MUTED,
            spaceAfter=6,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            textColor=NAVY,
            spaceBefore=12,
            spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            textColor=SLATE,
            leading=13,
        ),
        "flag": ParagraphStyle(
            "flag",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            textColor=NAVY,
            leading=12,
        ),
        "explain": ParagraphStyle(
            "explain",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            textColor=MUTED,
            leading=11,
            leftIndent=4,
        ),
        "footer": ParagraphStyle(
            "footer",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            textColor=MUTED,
        ),
    }


def build_forensic_pdf(case: dict, explain_flag) -> bytes:
    from src.explanations import explain_flag as default_explain

    explainer = explain_flag or default_explain
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title=f"E-UNTHREAT Forensic Report — Case {case.get('id', 'new')}",
        author="E-UNTHREAT",
    )
    styles = _styles()
    verdict = case.get("verdict", "Unknown")
    score = int(case.get("fraud_score") or 0)
    vcolor = VERDICT_COLORS.get(verdict, SLATE)
    verdict_hex = {"Phishing": "#dc2626", "Suspicious": "#d97706", "Legitimate": "#16a34a"}.get(
        verdict, "#334155"
    )
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    story: list = [
        Paragraph("E-UNTHREAT  ·  FORENSIC INTELLIGENCE", styles["brand"]),
        Paragraph("Email Threat Analysis Report", styles["title"]),
        Paragraph(
            f"Case #{case.get('id', '—')}  ·  Generated {generated}  ·  SIH 2026",
            styles["meta"],
        ),
        HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=10),
    ]

    header_tbl = Table(
        [
            [
                Paragraph(f"<b>VERDICT</b><br/><font size='16' color='{verdict_hex}'>{verdict.upper()}</font>", styles["body"]),
                Paragraph(f"<b>FRAUD SCORE</b><br/><font size='16'>{score} / 100</font>", styles["body"]),
                Paragraph(
                    f"<b>ORIGIN</b><br/>{case.get('origin_city', '—')}, {case.get('origin_country', '—')}",
                    styles["body"],
                ),
            ]
        ],
        colWidths=[60 * mm, 55 * mm, 60 * mm],
    )
    header_tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.4, colors.HexColor("#e2e8f0")),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#e2e8f0")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    story += [header_tbl, Spacer(1, 12)]

    identity_data = [
        ["Field", "Value"],
        ["Filename", xml_escape(str(case.get("filename") or "pasted-source.eml"))],
        ["Sender (From)", xml_escape(str(case.get("sender") or "—"))],
        ["Subject", xml_escape(str(case.get("subject") or "—"))],
        ["Origin IP", xml_escape(str(case.get("origin_ip") or "—"))],
        ["SPF / DKIM / DMARC", f"{case.get('spf_result')} / {case.get('dkim_result')} / {case.get('dmarc_result')}"],
        ["VPN / Hosting", "Yes" if case.get("is_vpn_or_hosting") else "No"],
        ["Analyzed at", str(case.get("analyzed_at") or generated)],
    ]
    ident = Table(identity_data, colWidths=[45 * mm, 130 * mm])
    ident.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#e2e8f0")),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story += [Paragraph("Message identity", styles["h2"]), ident]

    def flag_block(title: str, flags: list[str]) -> list:
        items = []
        for flag in flags or ["None"]:
            items.append(
                ListItem(
                    Paragraph(
                        f"<b>{xml_escape(str(flag))}</b><br/>{xml_escape(explainer(flag))}",
                        styles["explain"],
                    ),
                    leftIndent=8,
                    bulletColor=vcolor,
                )
            )
        return [Paragraph(title, styles["h2"]), ListFlowable(items, bulletType="bullet", start="•", leftIndent=12)]

    story += flag_block("NLP / content flags", case.get("content_flags") or [])
    story += flag_block("Header / protocol flags", case.get("header_flags") or [])
    story += flag_block("Origin / IP flags", case.get("origin_flags") or [])

    story.append(Paragraph("Relay path", styles["h2"]))
    hops = case.get("relay_path") or []
    hop_rows = [["Hop", "Mail server"]] + [[str(i + 1), hop] for i, hop in enumerate(hops)]
    hop_tbl = Table(hop_rows, colWidths=[20 * mm, 155 * mm])
    hop_tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#e2e8f0")),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(hop_tbl)
    story.append(Spacer(1, 16))
    story.append(
        Paragraph(
            "This report was produced by E-UNTHREAT for demonstration and analyst review. "
            "Findings combine content NLP, header authentication (SPF/DKIM/DMARC), and origin/GeoIP intelligence. "
            "Treat scores as decision support, not a sole basis for enforcement.",
            styles["footer"],
        )
    )

    def _on_page(canvas, _doc):
        canvas.saveState()
        canvas.setFillColor(NAVY)
        canvas.rect(0, A4[1] - 6 * mm, A4[0], 6 * mm, fill=1, stroke=0)
        canvas.setFillColor(TEAL)
        canvas.rect(0, 0, A4[0], 4 * mm, fill=1, stroke=0)
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 8)
        canvas.drawString(18 * mm, 6 * mm, "E-UNTHREAT  ·  Confidential forensic work product")
        canvas.drawRightString(A4[0] - 18 * mm, 6 * mm, f"Page {canvas.getPageNumber()}")
        canvas.restoreState()

    doc.build(story, onFirstPage=_on_page, onLaterPages=_on_page)
    return buffer.getvalue()
