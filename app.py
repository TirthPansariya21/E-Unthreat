"""
E-UNTHREAT — AI-Powered Email Threat Detection
GeoLocation & Forensic Intelligence  ·  SIH 2026

Pipeline: src.email_parser → ml_classifier + header_forensics + ip_tracer
           → fraud_aggregator.analyze_email → dashboard / PDF / SQLite.
"""

from __future__ import annotations

import html
import time
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.db import case_stats, get_case, init_db, list_cases, save_case
from src.explanations import explain_flag
from src.fraud_aggregator import analyze_email
from src.report_generator import build_forensic_pdf
from styles import DASHBOARD_CSS

ROOT = Path(__file__).resolve().parent
SAMPLES_DIR = ROOT / "samples"

VERDICT_COLORS = {
    "Phishing": "#B94A3D",
    "Suspicious": "#B8863A",
    "Legitimate": "#2F8F6C",
}
VERDICT_COPY = {
    "Phishing": "High confidence this message is a hostile lure. Do not click links or open attachments.",
    "Suspicious": "Multiple weak signals. Treat as untrusted until an analyst clears it.",
    "Legitimate": "Authentication and content checks look consistent with a genuine sender.",
}

SAMPLE_CHOICES = {
    "— choose a demo sample —": None,
    "PayPal account lock (phishing)": "paypal_phish.eml",
    "CEO wire-transfer BEC (phishing)": "ceo_bec.eml",
    "DHL customs invoice (suspicious)": "dhl_invoice.eml",
    "Microsoft password reset (phishing)": "microsoft_phish.eml",
    "GitHub sign-in notice (legitimate)": "github_legit.eml",
    "HR benefits reminder (legitimate)": "hr_benefits.eml",
}


def _inject_styles() -> None:
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)


def _flag_tone(flag: str) -> str:
    upper = flag.upper()
    if upper.startswith("NO ") or upper.endswith("PASS"):
        return "ok"
    if upper.endswith("NONE") or "MISSING" in upper:
        return "warn"
    return "bad"


def _tone_mark(tone: str) -> str:
    if tone == "ok":
        return "✓"
    if tone == "warn":
        return "–"
    return "✕"


def _auth_display(value: object) -> tuple[str, str, str]:
    raw = str(value or "NONE").upper()
    if raw == "PASS":
        return "Pass", "ok", "✓"
    if raw == "FAIL":
        return "Fail", "bad", "✕"
    return "None", "warn", "–"


def _role_for_hop(index: int, total: int) -> str:
    if index == 0:
        return "Originating mail server"
    if index == total - 1:
        return "Destination / recipient MX"
    return "Intermediate relay"


def render_sidebar() -> str:
    stats = case_stats()
    with st.sidebar:
        st.markdown(
            """
            <div class="eut-brand">
              <div class="eut-name">E-Unthreat</div>
              <div class="eut-sub">Email threat intelligence</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption("SIH 2026")
        page = st.radio(
            "Navigation",
            ["Analyze email", "Case history"],
            key="nav_page",
            label_visibility="collapsed",
        )
        st.markdown(
            f"""
            <div class="side-stats">
              <div class="side-stat"><div class="k">Cases</div><div class="v">{stats["total"]}</div></div>
              <div class="side-stat"><div class="k">Phishing</div><div class="v">{stats["phishing"]}</div></div>
              <div class="side-stat"><div class="k">Suspicious</div><div class="v">{stats["suspicious"]}</div></div>
              <div class="side-stat"><div class="k">Average score</div><div class="v">{stats["avg_score"]}</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption("Classifier, header checks, and GeoIP run locally. Offline fallbacks keep the demo working.")
    return page


def fraud_gauge(score: int, verdict: str) -> go.Figure:
    color = VERDICT_COLORS.get(verdict, "#69707D")
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"font": {"size": 28, "color": "#1E2530", "family": "Source Serif 4, Georgia, serif"}, "suffix": ""},
            title={"text": "Fraud score", "font": {"size": 15, "color": "#69707D", "family": "Source Serif 4, Georgia, serif"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#E3E7EC", "tickfont": {"color": "#69707D"}},
                "bar": {"color": color, "thickness": 0.22},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 40], "color": "rgba(47, 143, 108, 0.10)"},
                    {"range": [40, 70], "color": "rgba(184, 134, 58, 0.10)"},
                    {"range": [70, 100], "color": "rgba(185, 74, 61, 0.10)"},
                ],
                "threshold": {"line": {"color": color, "width": 2}, "thickness": 0.75, "value": score},
            },
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=12, r=12, t=40, b=8),
        height=230,
        font={"color": "#1E2530", "family": "Inter, sans-serif"},
    )
    return fig


def render_origin_map(case: dict) -> None:
    lat = float(case.get("origin_lat") or 0)
    lon = float(case.get("origin_lon") or 0)
    city = case.get("origin_city") or "Unknown"
    country = case.get("origin_country") or "Unknown"
    color = VERDICT_COLORS.get(case.get("verdict"), "#38bdf8")

    # Plotly Scattergeo only — no tile server, no API key, no network
    # dependency at render time. Reliable for a live demo on any network.
    fig = go.Figure(
        go.Scattergeo(
            lon=[lon],
            lat=[lat],
            text=[f"{city}, {country}"],
            hovertemplate=f"<b>{html.escape(city)}, {html.escape(country)}</b><br>IP {case.get('origin_ip', '—')}<extra></extra>",
            mode="markers",
            marker=dict(
                size=16,
                color=color,
                line=dict(width=1.5, color="#FFFFFF"),
                opacity=0.9,
            ),
        )
    )
    fig.update_geos(
        projection_type="natural earth",
        showland=True,
        landcolor="#EEF1F4",
        showocean=True,
        oceancolor="#F7F8FA",
        showcountries=True,
        countrycolor="#D5DAE0",
        coastlinecolor="#D5DAE0",
        bgcolor="rgba(0,0,0,0)",
        lataxis_showgrid=False,
        lonaxis_showgrid=False,
        center=dict(lat=lat, lon=lon),
        projection_scale=3.2,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=380,
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _flag_rows_html(flags: list[str]) -> str:
    rows = []
    for flag in flags or []:
        tone = _flag_tone(flag)
        rows.append(
            f'<div class="flag {tone}">'
            f'<div class="mark">{_tone_mark(tone)}</div>'
            f'<div><div class="flag-name">{html.escape(flag)}</div>'
            f'<div class="flag-why">{html.escape(explain_flag(flag))}</div></div>'
            f"</div>"
        )
    if not rows:
        rows.append(
            '<div class="flag ok"><div class="mark">✓</div>'
            "<div><div class=\"flag-name\">No flags</div>"
            '<div class="flag-why">This evidence channel did not raise a finding.</div></div></div>'
        )
    return "".join(rows)


def render_evidence(case: dict) -> None:
    groups = [
        ("Content", case.get("content_flags") or []),
        ("Header & protocol", case.get("header_flags") or []),
        ("Origin & domain", case.get("origin_flags") or []),
    ]
    body = "".join(
        f'<div class="evidence-group"><div class="group-title">{title}</div>{_flag_rows_html(flags)}</div>'
        for title, flags in groups
    )
    st.markdown(
        f'<div class="evidence"><div class="section-heading">Evidence</div>{body}</div>',
        unsafe_allow_html=True,
    )


def render_relay_path(hops: list[str]) -> None:
    if not hops:
        st.info("No Received headers were present to reconstruct a hop path.")
        return
    parts = []
    total = len(hops)
    for i, hop in enumerate(hops):
        parts.append(
            f'<div class="hop"><div class="hop-num">{i + 1}</div>'
            f'<div><div class="hop-host">{html.escape(str(hop))}</div>'
            f'<div class="hop-role">{_role_for_hop(i, total)}</div></div></div>'
        )
    st.markdown("".join(parts), unsafe_allow_html=True)


def _new_analysis() -> None:
    st.session_state.active_case_id = None
    st.session_state.from_history = False
    st.session_state.nav_page = "Analyze email"


def _back_to_history() -> None:
    st.session_state.active_case_id = None
    st.session_state.from_history = False
    st.session_state.nav_page = "Case history"


def render_results(case: dict, *, from_history: bool = False) -> None:
    verdict = case.get("verdict", "Unknown")
    klass = verdict.lower()
    score = int(case.get("fraud_score") or 0)

    if from_history:
        when = case.get("analyzed_at") or ""
        extra = f", analyzed {when}" if when else ""
        st.info(f"Viewing archived case #{case.get('id')}{extra}")
    for warning in case.get("warnings") or []:
        st.warning(warning)

    top, gauge = st.columns([1.45, 0.9], gap="large")
    with top:
        st.markdown(
            f"""
            <div class="verdict-banner {klass}">
              <p class="verdict-word {klass}">{html.escape(verdict)}</p>
              <p class="verdict-explain">{html.escape(VERDICT_COPY.get(verdict, ""))}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with gauge:
        st.plotly_chart(fraud_gauge(score, verdict), use_container_width=True, config={"displayModeBar": False})

    sender = html.escape(str(case.get("sender") or "—"))
    subject = html.escape(str(case.get("subject") or "—"))
    origin_ip = html.escape(str(case.get("origin_ip") or "—"))
    st.markdown(
        f"""
        <div class="meta-row">
          <div class="meta-item"><div class="k">Sender</div><div class="v mono">{sender}</div></div>
          <div class="meta-item"><div class="k">Subject</div><div class="v">{subject}</div></div>
          <div class="meta-item"><div class="k">Origin IP</div><div class="v mono">{origin_ip}</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    auth_html = []
    for label, key in (("SPF", "spf_result"), ("DKIM", "dkim_result"), ("DMARC", "dmarc_result")):
        text, tone, mark = _auth_display(case.get(key))
        auth_html.append(
            f'<div class="auth-line {tone}"><span class="mark">{mark}</span>'
            f'<span class="lbl">{label}:</span> <span class="val">{text}</span></div>'
        )
    st.markdown(f'<div class="auth-stack">{"".join(auth_html)}</div>', unsafe_allow_html=True)

    render_evidence(case)

    map_col, hop_col = st.columns([1.15, 1], gap="large")
    with map_col:
        st.markdown('<div class="section-heading">Estimated sender origin</div>', unsafe_allow_html=True)
        loc = f"{case.get('origin_city', 'Unknown')}, {case.get('origin_country', 'Unknown')}"
        vpn = "VPN or hosting range" if case.get("is_vpn_or_hosting") else "Not flagged as VPN or hosting"
        st.markdown(f'<p class="pair-caption">{html.escape(loc)}. {vpn}.</p>', unsafe_allow_html=True)
        render_origin_map(case)
    with hop_col:
        st.markdown('<div class="section-heading">Relay path</div>', unsafe_allow_html=True)
        st.markdown(
            '<p class="pair-caption">Hop-by-hop path reconstructed from Received headers, origin to destination.</p>',
            unsafe_allow_html=True,
        )
        render_relay_path(case.get("relay_path") or [])

    st.markdown("")
    pdf_bytes = build_forensic_pdf(case, explain_flag)
    case_id = case.get("id", "new")
    safe_verdict = str(verdict).lower()
    dl, again, back = st.columns([1.4, 1, 1])
    with dl:
        st.download_button(
            "Download forensic report (PDF)",
            data=pdf_bytes,
            file_name=f"e-unthreat_case_{case_id}_{safe_verdict}.pdf",
            mime="application/pdf",
            use_container_width=False,
            type="primary",
        )
    with again:
        st.button(
            "New analysis",
            use_container_width=False,
            on_click=_new_analysis,
        )
    with back:
        if from_history:
            st.button(
                "Back to history",
                use_container_width=False,
                on_click=_back_to_history,
            )


def _read_upload(uploaded) -> tuple[str, str]:
    raw_bytes = uploaded.getvalue()
    text = raw_bytes.decode("utf-8", errors="replace")
    return text, uploaded.name


def _run_pipeline(raw_text: str, filename: str) -> None:
    with st.status("Running forensic pipeline…", expanded=True) as status:
        st.write("Parsing MIME structure and header graph…")
        time.sleep(0.2)
        st.write("NLP / ML classifier — TF-IDF + rule-based lure signals…")
        time.sleep(0.2)
        st.write("SPF / DKIM / DMARC authentication and alignment…")
        time.sleep(0.15)
        st.write("GeoIP origin tracing, WHOIS, relay reconstruction…")
        result = analyze_email(raw_text)
        status.update(label="Analysis complete", state="complete")
    case_id = save_case(filename, result)
    st.session_state.active_case_id = case_id
    st.session_state.from_history = False
    st.rerun()


def _on_sample_change() -> None:
    choice = st.session_state.get("sample_choice")
    name = SAMPLE_CHOICES.get(choice)
    if not name:
        return
    path = SAMPLES_DIR / name
    if path.exists():
        st.session_state.raw_source = path.read_text(encoding="utf-8", errors="replace")


def _render_landing_strip() -> None:
    st.markdown(
        """
        <div class="landing-strip">
          <div class="landing-col">
            <div class="landing-title">Content</div>
            <div class="landing-body">A TF-IDF classifier trained on 164k+ labeled emails,
            plus rule-based checks for urgency language, obfuscated links, and lookalike
            domains (e.g. paypa1-secure.com).</div>
          </div>
          <div class="landing-col">
            <div class="landing-title">Header &amp; protocol</div>
            <div class="landing-body">SPF, DKIM, and DMARC validated against the sending
            domain's real DNS records, with the Received-header relay chain reconstructed
            hop by hop to catch spoofed From/Return-Path pairs.</div>
          </div>
          <div class="landing-col">
            <div class="landing-title">Origin &amp; domain</div>
            <div class="landing-body">The earliest public IP in the relay chain is geolocated
            and checked against known VPN/hosting ranges; the sending domain's WHOIS age is
            checked for recent registration.</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_upload() -> None:
    uploaded = None
    options = ["Demo sample", "Upload", "Paste"]
    with st.container():
        st.markdown('<div class="input-panel-marker"></div>', unsafe_allow_html=True)
        if hasattr(st, "segmented_control"):
            mode = st.segmented_control(
                "Input method",
                options,
                default="Demo sample",
                key="input_mode",
                label_visibility="collapsed",
            )
        else:
            mode = st.radio(
                "Input method",
                options,
                horizontal=True,
                key="input_mode",
                label_visibility="collapsed",
            )
        mode = mode or "Demo sample"

        if mode == "Demo sample":
            st.selectbox(
                "Demo sample",
                list(SAMPLE_CHOICES.keys()),
                key="sample_choice",
                on_change=_on_sample_change,
                label_visibility="collapsed",
            )
        elif mode == "Upload":
            uploaded = st.file_uploader(
                "Upload email",
                type=["eml", "txt"],
                label_visibility="collapsed",
            )
        else:
            st.text_area(
                "Paste source",
                height=200,
                placeholder="From: ...\nReceived: ...\nSubject: ...\n\nDear customer, ...",
                key="raw_source",
                label_visibility="collapsed",
            )

    analyze = st.button("Analyze", type="primary")
    if not analyze:
        _render_landing_strip()
        return

    filename = "pasted-source.eml"
    source = ""
    if mode == "Upload":
        if uploaded is None:
            st.error("Choose a .eml file to upload first.")
            return
        source, filename = _read_upload(uploaded)
    elif mode == "Demo sample":
        choice = st.session_state.get("sample_choice")
        name = SAMPLE_CHOICES.get(choice)
        if not name:
            st.error("Choose a demo sample first.")
            return
        path = SAMPLES_DIR / name
        source = path.read_text(encoding="utf-8", errors="replace")
        filename = name
    else:
        source = (st.session_state.get("raw_source") or "").strip()
        if not source:
            st.error("Paste the raw email source first.")
            return

    if not source.strip():
        st.error("No email source to analyze.")
        return
    _run_pipeline(source, filename)


def render_history() -> None:
    st.markdown(
        '<p class="history-hint">Select a row to reopen the full forensic view for that case.</p>',
        unsafe_allow_html=True,
    )
    rows = list_cases()
    if not rows:
        st.warning("No cases yet. Analyze an email to populate history.")
        return

    frame = pd.DataFrame(rows)
    frame = frame.rename(
        columns={
            "id": "ID",
            "filename": "Filename",
            "sender": "Sender",
            "subject": "Subject",
            "verdict": "Verdict",
            "fraud_score": "Fraud score",
            "origin_country": "Origin",
            "analyzed_at": "Analyzed",
        }
    )
    event = st.dataframe(
        frame,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        column_config={
            "ID": st.column_config.NumberColumn("ID", width="small"),
            "Fraud score": st.column_config.ProgressColumn(
                "Fraud score", min_value=0, max_value=100, format="%d"
            ),
            "Verdict": st.column_config.TextColumn("Verdict", width="small"),
        },
    )
    selected = []
    if event is not None and getattr(event, "selection", None) is not None:
        selection = event.selection
        selected = getattr(selection, "rows", None) or (
            selection.get("rows", []) if isinstance(selection, dict) else []
        )
    if selected:
        case_id = int(frame.iloc[selected[0]]["ID"])
        st.session_state.active_case_id = case_id
        st.session_state.from_history = True
        st.rerun()


def main() -> None:
    st.set_page_config(
        page_title="E-UNTHREAT | Email Threat Intelligence",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    init_db()
    _inject_styles()

    if "active_case_id" not in st.session_state:
        st.session_state.active_case_id = None
    if "from_history" not in st.session_state:
        st.session_state.from_history = False
    if "raw_source" not in st.session_state:
        st.session_state.raw_source = ""
    if "nav_page" not in st.session_state:
        st.session_state.nav_page = "Analyze email"

    if st.session_state.get("nav_page") == "Analyze Email":
        st.session_state.nav_page = "Analyze email"
    if st.session_state.get("nav_page") == "Case History":
        st.session_state.nav_page = "Case history"

    page = render_sidebar()

    st.markdown(
        """
        <div class="page-header">
          <h1>E-Unthreat</h1>
          <p>Email threat detection, geolocation, and forensic intelligence.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    active = st.session_state.active_case_id

    if page == "Case history":
        if active and st.session_state.from_history:
            case = get_case(int(active))
            if case:
                render_results(case, from_history=True)
                return
        render_history()
        return

    if active and not st.session_state.from_history:
        case = get_case(int(active))
        if case:
            render_results(case, from_history=False)
            return
        st.session_state.active_case_id = None

    render_upload()


if __name__ == "__main__":
    main()
