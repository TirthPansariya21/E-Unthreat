"""
E-UNTHREAT — AI-Powered Email Threat Detection & SOC Forensic Intelligence
SIH 2026

Pipeline: src.email_parser → ml_classifier + header_forensics + ip_tracer
           → fraud_aggregator.analyze_email → dashboard / PDF / SQLite.
"""

from __future__ import annotations

import html
import time
import urllib.request
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
    "Phishing": "#EF4444",
    "Suspicious": "#F59E0B",
    "Legitimate": "#10B981",
}
VERDICT_HEADLINES = {
    "Phishing": "THREAT DETECTED — PHISHING",
    "Suspicious": "SUSPICIOUS ACTIVITY DETECTED",
    "Legitimate": "VERIFIED LEGITIMATE EMAIL",
}
VERDICT_BADGES = {
    "Phishing": "CRITICAL RISK",
    "Suspicious": "ELEVATED RISK",
    "Legitimate": "LOW RISK",
}
VERDICT_COPY = {
    "Phishing": "High confidence this message is a hostile lure. Do not click links, execute attachments, or reply with credentials.",
    "Suspicious": "Multiple risk signals detected. Message exhibits anomalous patterns; treat as untrusted until validated.",
    "Legitimate": "Cryptographic authentication and NLP content analysis indicate a legitimate sender with no hostile indicators.",
}

SAMPLE_CHOICES = {
    "— Select a demo case —": None,
    "🚨 PayPal account lock (Phishing lure)": "paypal_phish.eml",
    "🚨 CEO wire-transfer BEC (Executive impersonation)": "ceo_bec.eml",
    "⚠️ DHL customs invoice (Suspicious invoice)": "dhl_invoice.eml",
    "🚨 Microsoft password reset (Credential harvesting)": "microsoft_phish.eml",
    "✅ GitHub sign-in alert (Legitimate transactional)": "github_legit.eml",
    "✅ HR benefits update (Legitimate internal)": "hr_benefits.eml",
}


def _inject_styles() -> None:
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)


def _flag_tone(flag: str) -> str:
    upper = flag.upper()
    if upper.startswith("NO ") or upper.endswith("PASS"):
        return "ok"
    if upper.endswith("NONE") or "MISSING" in upper or "UNUSUAL" in upper:
        return "warn"
    return "bad"


def _tone_mark(tone: str) -> str:
    if tone == "ok":
        return "✓"
    if tone == "warn":
        return "!"
    return "✕"


def _tone_tag(tone: str) -> str:
    if tone == "ok":
        return "PASS"
    if tone == "warn":
        return "WARNING"
    return "CRITICAL"


def _auth_display(value: object) -> tuple[str, str, str]:
    raw = str(value or "NONE").upper()
    if raw == "PASS":
        return "PASS", "ok", "✓"
    if raw == "FAIL":
        return "FAIL", "bad", "✕"
    return "NONE", "warn", "–"


def _role_for_hop(index: int, total: int) -> str:
    if index == 0:
        return "Originating Mail Server"
    if index == total - 1:
        return "Destination / Recipient MX Gateway"
    return "Intermediate MTA Relay"


def render_top_bar() -> None:
    st.markdown(
        """
        <div class="top-nav-bar">
          <div class="top-brand">
            <div class="top-brand-icon">🛡️</div>
            <div>
              <span class="top-brand-title">E-UNTHREAT</span>
              <span class="top-brand-badge">SOC INTELLIGENCE</span>
            </div>
          </div>
          <div class="top-status-indicator">
            <div class="pulse-dot"></div>
            <span>Threat Engine Online · Real-Time Heuristics Active</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> str:
    stats = case_stats()
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-header">
              <div class="sidebar-brand-name">
                <span>🛡️</span> E-UNTHREAT
              </div>
              <div class="sidebar-brand-sub">Email Threat Intelligence & Forensics</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        page = st.radio(
            "Navigation",
            ["⚡ Threat Analysis", "🗂️ Case History"],
            key="nav_page",
            label_visibility="collapsed",
        )
        st.markdown(
            f"""
            <div class="soc-metrics-container">
              <div class="soc-metrics-title">📊 SOC Telemetry</div>
              <div class="soc-stat-grid">
                <div class="soc-stat-tile total">
                  <div class="soc-stat-label">Total Cases</div>
                  <div class="soc-stat-val">{stats["total"]}</div>
                </div>
                <div class="soc-stat-tile phish">
                  <div class="soc-stat-label">Phishing</div>
                  <div class="soc-stat-val">{stats["phishing"]}</div>
                </div>
                <div class="soc-stat-tile sus">
                  <div class="soc-stat-label">Suspicious</div>
                  <div class="soc-stat-val">{stats["suspicious"]}</div>
                </div>
                <div class="soc-stat-tile avg">
                  <div class="soc-stat-label">Avg Risk</div>
                  <div class="soc-stat-val">{stats["avg_score"]}</div>
                </div>
              </div>
            </div>
            <div class="sidebar-footer-note">
              🔒 <strong>Local Execution:</strong> NLP classifiers, cryptographic header alignment, and GeoIP heuristics run in a sandboxed offline environment.
            </div>
            """,
            unsafe_allow_html=True,
        )
    return page


def fraud_gauge(score: int, verdict: str) -> go.Figure:
    color = VERDICT_COLORS.get(verdict, "#38BDF8")
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={
                "font": {"size": 36, "color": "#F8FAFC", "family": "JetBrains Mono, monospace"},
                "suffix": " / 100",
            },
            title={
                "text": "THREAT SCORE",
                "font": {"size": 13, "color": "#94A3B8", "family": "Inter, sans-serif"},
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickcolor": "#334155",
                    "tickfont": {"color": "#64748B", "size": 10},
                    "tickwidth": 1,
                },
                "bar": {"color": color, "thickness": 0.24},
                "bgcolor": "rgba(15, 23, 42, 0.6)",
                "borderwidth": 1,
                "bordercolor": "rgba(255,255,255,0.08)",
                "steps": [
                    {"range": [0, 40], "color": "rgba(16, 185, 129, 0.12)"},
                    {"range": [40, 70], "color": "rgba(245, 158, 11, 0.12)"},
                    {"range": [70, 100], "color": "rgba(239, 68, 68, 0.12)"},
                ],
                "threshold": {
                    "line": {"color": color, "width": 3},
                    "thickness": 0.8,
                    "value": score,
                },
            },
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=15, r=15, t=35, b=10),
        height=210,
        font={"color": "#F8FAFC", "family": "Inter, sans-serif"},
    )
    return fig


def _map_api_key() -> str:
    try:
        return str(st.secrets["MAP_API_KEY"]).strip()
    except Exception:
        return ""


def _geoapify_tiles_available(api_key: str) -> bool:
    if not api_key:
        return False
    cached = st.session_state.get("_geoapify_ok")
    if cached is not None:
        return bool(cached)
    url = f"https://maps.geoapify.com/v1/tile/osm-carto/2/2/1.png?apiKey={api_key}"
    ok = False
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "E-Unthreat"})
        with urllib.request.urlopen(request, timeout=4) as response:
            content_type = (response.headers.get("content-type") or "").lower()
            ok = response.status == 200 and "image" in content_type
    except Exception:
        ok = False
    st.session_state._geoapify_ok = ok
    return ok


def _scattergeo_map(lat: float, lon: float, city: str, country: str, color: str) -> None:
    fig = go.Figure(
        go.Scattergeo(
            lon=[lon],
            lat=[lat],
            text=[f"{city}, {country}"],
            mode="markers+text",
            textposition="top center",
            textfont=dict(family="Inter, sans-serif", size=11, color="#F8FAFC"),
            marker=dict(
                size=16,
                color=color,
                line=dict(width=2, color="#FFFFFF"),
                opacity=0.9,
            ),
        )
    )
    fig.update_geos(
        projection_type="natural earth",
        showland=True,
        landcolor="#1E293B",
        showocean=True,
        oceancolor="#0B0F19",
        showcountries=True,
        countrycolor="#334155",
        bgcolor="#0B0F19",
        showframe=False,
        lataxis_showgrid=True,
        lataxis_gridcolor="rgba(255,255,255,0.05)",
        lonaxis_showgrid=True,
        lonaxis_gridcolor="rgba(255,255,255,0.05)",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=320,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_origin_map(case: dict) -> None:
    lat = float(case.get("origin_lat") or 0)
    lon = float(case.get("origin_lon") or 0)
    city = case.get("origin_city") or "Unknown"
    country = case.get("origin_country") or "Unknown"
    color = VERDICT_COLORS.get(case.get("verdict"), "#38BDF8")
    api_key = _map_api_key()
    attr = "© OpenStreetMap contributors © Geoapify"

    if _geoapify_tiles_available(api_key):
        try:
            import folium
            from streamlit_folium import st_folium

            tile_url = (
                "https://maps.geoapify.com/v1/tile/osm-carto/{z}/{x}/{y}.png"
                f"?apiKey={api_key}"
            )
            fmap = folium.Map(location=[lat, lon], zoom_start=4, tiles=None, attr=attr)
            folium.TileLayer(
                tiles=tile_url,
                attr=attr,
                name="Geoapify",
                overlay=False,
                control=False,
            ).add_to(fmap)
            folium.CircleMarker(
                location=[lat, lon],
                radius=14,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.85,
                popup=folium.Popup(
                    f"<b>{city}, {country}</b><br/>IP {case.get('origin_ip', '—')}",
                    max_width=260,
                ),
            ).add_to(fmap)
            folium.Circle(
                location=[lat, lon],
                radius=180000,
                color=color,
                fill=True,
                fill_opacity=0.08,
                weight=1,
            ).add_to(fmap)
            st_folium(fmap, height=320, use_container_width=True, returned_objects=[])
            return
        except Exception:
            st.session_state._geoapify_ok = False

    _scattergeo_map(lat, lon, city, country, color)


def _flag_cards_html(flags: list[str]) -> str:
    cards = []
    for flag in flags or []:
        tone = _flag_tone(flag)
        mark = _tone_mark(tone)
        tag = _tone_tag(tone)
        why = explain_flag(flag)
        cards.append(
            f'<div class="flag-card {tone}">'
            f'<div class="flag-status-icon">{mark}</div>'
            f'<div class="flag-info">'
            f'<div class="flag-title-row">'
            f'<span class="flag-name">{html.escape(flag)}</span>'
            f'<span class="flag-tag">{tag}</span>'
            f'</div>'
            f'<div class="flag-explanation">{html.escape(why)}</div>'
            f'</div>'
            f'</div>'
        )
    if not cards:
        cards.append(
            '<div class="flag-card ok">'
            '<div class="flag-status-icon">✓</div>'
            '<div class="flag-info">'
            '<div class="flag-title-row">'
            '<span class="flag-name">No anomalies detected</span>'
            '<span class="flag-tag">PASS</span>'
            '</div>'
            '<div class="flag-explanation">All inspection heuristics in this channel passed baseline security thresholds.</div>'
            '</div>'
            '</div>'
        )
    return "".join(cards)


def render_evidence(case: dict) -> None:
    groups = [
        ("🔍 Content & NLP Signals", case.get("content_flags") or []),
        ("📑 Email Headers & Protocol Alignment", case.get("header_flags") or []),
        ("🌐 Origin & Domain Intelligence", case.get("origin_flags") or []),
    ]
    body = "".join(
        f'<div class="evidence-category-title">{title}</div>{_flag_cards_html(flags)}'
        for title, flags in groups
    )
    st.markdown(
        f"""
        <div class="soc-section-title">🛡️ Threat Evidence & Forensic Findings</div>
        <div class="evidence-container">
          {body}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_relay_path(hops: list[str]) -> None:
    if not hops:
        st.info("No Received headers present to reconstruct MTA relay path.")
        return
    parts = []
    total = len(hops)
    for i, hop in enumerate(hops):
        role = _role_for_hop(i, total)
        parts.append(
            f'<div class="timeline-node">'
            f'<div class="node-marker">{i + 1}</div>'
            f'<div class="node-card">'
            f'<div class="node-role">{role}</div>'
            f'<div class="node-host">{html.escape(str(hop))}</div>'
            f'</div>'
            f'</div>'
        )
    st.markdown(f'<div class="timeline-container">{"".join(parts)}</div>', unsafe_allow_html=True)


def _new_analysis() -> None:
    st.session_state.active_case_id = None
    st.session_state.from_history = False
    st.session_state.nav_page = "⚡ Threat Analysis"


def _back_to_history() -> None:
    st.session_state.active_case_id = None
    st.session_state.from_history = False
    st.session_state.nav_page = "🗂️ Case History"


def render_results(case: dict, *, from_history: bool = False) -> None:
    verdict = case.get("verdict", "Unknown")
    klass = verdict.lower()
    score = int(case.get("fraud_score") or 0)
    badge_text = VERDICT_BADGES.get(verdict, "INVESTIGATION")
    headline = VERDICT_HEADLINES.get(verdict, "ANALYSIS COMPLETE")

    if from_history:
        when = case.get("analyzed_at") or ""
        extra = f" · Analyzed: {when}" if when else ""
        st.info(f"📂 Reviewing Archived Case #{case.get('id')}{extra}")

    for warning in case.get("warnings") or []:
        st.warning(f"⚠️ {warning}")

    # Top Row: Verdict Banner & Threat Score Gauge
    top_col, gauge_col = st.columns([1.35, 1], gap="medium")
    with top_col:
        st.markdown(
            f"""
            <div class="verdict-card {klass}">
              <div class="verdict-top-row">
                <span class="verdict-badge {klass}">{badge_text}</span>
              </div>
              <div class="verdict-headline {klass}">{headline}</div>
              <p class="verdict-summary">{html.escape(VERDICT_COPY.get(verdict, ''))}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with gauge_col:
        st.plotly_chart(
            fraud_gauge(score, verdict),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    # 4-Card Overview Grid
    sender = html.escape(str(case.get("sender") or "—"))
    subject = html.escape(str(case.get("subject") or "—"))
    origin_ip = html.escape(str(case.get("origin_ip") or "—"))
    isp = html.escape(str(case.get("origin_isp") or "—"))
    to_addr = html.escape(str(case.get("to") or "—"))

    st.markdown(
        f"""
        <div class="meta-grid">
          <div class="meta-card">
            <div class="meta-card-label">👤 Sender (From)</div>
            <div class="meta-card-value mono">{sender}</div>
          </div>
          <div class="meta-card">
            <div class="meta-card-label">🎯 Recipient (To)</div>
            <div class="meta-card-value mono">{to_addr}</div>
          </div>
          <div class="meta-card">
            <div class="meta-card-label">📝 Subject Line</div>
            <div class="meta-card-value">{subject}</div>
          </div>
          <div class="meta-card">
            <div class="meta-card-label">🌐 Origin IP & ISP</div>
            <div class="meta-card-value mono">{origin_ip} <span style="color:var(--text-muted);font-size:0.75rem;">({isp})</span></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Row: Authentication Matrix & ML Content Classifier
    auth_col, ml_col = st.columns([1, 1], gap="medium")
    with auth_col:
        spf_txt, spf_tone, spf_mark = _auth_display(case.get("spf_result"))
        dkim_txt, dkim_tone, dkim_mark = _auth_display(case.get("dkim_result"))
        dmarc_txt, dmarc_tone, dmarc_mark = _auth_display(case.get("dmarc_result"))

        st.markdown(
            f"""
            <div class="soc-panel">
              <div class="panel-header-title">🔐 Cryptographic Email Authentication</div>
              <div class="auth-cards-row">
                <div class="auth-badge-box {spf_tone}">
                  <div class="auth-proto-name">SPF</div>
                  <div class="auth-status-chip">{spf_mark} {spf_txt}</div>
                </div>
                <div class="auth-badge-box {dkim_tone}">
                  <div class="auth-proto-name">DKIM</div>
                  <div class="auth-status-chip">{dkim_mark} {dkim_txt}</div>
                </div>
                <div class="auth-badge-box {dmarc_tone}">
                  <div class="auth-proto-name">DMARC</div>
                  <div class="auth-status-chip">{dmarc_mark} {dmarc_txt}</div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with ml_col:
        ml_label = html.escape(str(case.get("ml_label") or "Unknown"))
        ml_conf = float(case.get("ml_confidence") or 0.0)
        ml_pct = int(round(ml_conf * 100)) if ml_conf <= 1.0 else int(ml_conf)
        ml_bar_class = "phish" if ml_label.lower() == "phishing" else "legit"
        st.markdown(
            f"""
            <div class="soc-panel">
              <div class="panel-header-title">🤖 Machine Learning NLP Classifier</div>
              <div class="ml-metric-row">
                <span class="ml-metric-label">Model Architecture:</span>
                <span class="ml-metric-val">TF-IDF + Calibrated Logistic Regression</span>
              </div>
              <div class="ml-metric-row">
                <span class="ml-metric-label">Predicted Classification:</span>
                <span class="ml-metric-val" style="color: {'var(--danger)' if ml_label.lower() == 'phishing' else 'var(--success)'}; font-weight:700;">{ml_label}</span>
              </div>
              <div class="ml-metric-row">
                <span class="ml-metric-label">Confidence Probability:</span>
                <span class="ml-metric-val mono">{ml_pct}%</span>
              </div>
              <div class="ml-bar-bg">
                <div class="ml-bar-fill {ml_bar_class}" style="width: {ml_pct}%;"></div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Evidence Breakdown
    render_evidence(case)

    # Origin Geolocation & Relay Hop Path
    map_col, hop_col = st.columns([1.1, 1], gap="medium")
    with map_col:
        loc = f"{case.get('origin_city', 'Unknown')}, {case.get('origin_country', 'Unknown')}"
        vpn_flag = bool(case.get("is_vpn_or_hosting"))
        vpn_pill_class = "flagged" if vpn_flag else "clean"
        vpn_text = "VPN / Cloud Host Range" if vpn_flag else "Standard Residential / Enterprise ISP"

        st.markdown(
            f"""
            <div class="soc-section-title">📍 Estimated Sender Geolocation</div>
            <div class="map-frame-container">
              <div class="location-meta-bar">
                <span class="loc-pill">{html.escape(loc)}</span>
                <span class="vpn-pill {vpn_pill_class}">{vpn_text}</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_origin_map(case)

    with hop_col:
        st.markdown(
            """
            <div class="soc-section-title">⛓️ MTA Relay Traversal (Hop-by-Hop)</div>
            """,
            unsafe_allow_html=True,
        )
        render_relay_path(case.get("relay_path") or [])

    # Action Toolbar
    pdf_bytes = build_forensic_pdf(case, explain_flag)
    case_id = case.get("id", "new")
    safe_verdict = str(verdict).lower()

    st.markdown('<div class="action-toolbar">', unsafe_allow_html=True)
    dl, again, back = st.columns([1.5, 1, 1])
    with dl:
        st.download_button(
            "📄 Download Forensic Report (PDF)",
            data=pdf_bytes,
            file_name=f"e-unthreat_case_{case_id}_{safe_verdict}.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary",
        )
    with again:
        st.button(
            "🔄 Analyze Another Email",
            use_container_width=True,
            on_click=_new_analysis,
        )
    with back:
        if from_history:
            st.button(
                "🗂️ Return to Case Archive",
                use_container_width=True,
                on_click=_back_to_history,
            )
    st.markdown("</div>", unsafe_allow_html=True)


def _read_upload(uploaded) -> tuple[str, str]:
    raw_bytes = uploaded.getvalue()
    text = raw_bytes.decode("utf-8", errors="replace")
    return text, uploaded.name


def _run_pipeline(raw_text: str, filename: str) -> None:
    with st.status("🔍 Executing Deep Threat Pipeline...", expanded=True) as status:
        st.write("⚙️ Parsing MIME multi-part structure & header graph...")
        time.sleep(0.2)
        st.write("🤖 Evaluating NLP / ML classifiers & lexical lure heuristics...")
        time.sleep(0.2)
        st.write("🔐 Verifying SPF, DKIM, and DMARC cryptographic alignment...")
        time.sleep(0.15)
        st.write("🌐 Performing GeoIP triangulation, Autonomous System lookup, and relay reconstruction...")
        result = analyze_email(raw_text)
        status.update(label="✅ Forensic Analysis Complete", state="complete")
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


def render_upload() -> None:
    uploaded = None
    options = ["📂 Demo Cases", "📤 Upload Email", "📋 Paste Raw Email"]

    st.markdown(
        """
        <div class="console-card">
          <div class="console-header">
            <div>
              <div class="console-title">⚡ Threat Investigation Console</div>
              <div class="console-subtitle">Inspect suspicious messages via preloaded samples, .eml upload, or raw header/body strings.</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if hasattr(st, "segmented_control"):
        mode = st.segmented_control(
            "Input Method",
            options,
            default="📂 Demo Cases",
            key="input_mode",
            label_visibility="collapsed",
        )
    else:
        mode = st.radio(
            "Input Method",
            options,
            horizontal=True,
            key="input_mode",
            label_visibility="collapsed",
        )
    mode = mode or "📂 Demo Cases"

    if mode == "📂 Demo Cases":
        st.selectbox(
            "Select Demo Case",
            list(SAMPLE_CHOICES.keys()),
            key="sample_choice",
            on_change=_on_sample_change,
        )
    elif mode == "📤 Upload Email":
        uploaded = st.file_uploader(
            "Upload Email (.eml / .txt)",
            type=["eml", "txt", "msg"],
            help="Select an email message file to deconstruct.",
        )
    else:
        st.text_area(
            "Raw Email MIME Source / Headers",
            height=220,
            placeholder="From: security@paypal-verify.com\nTo: victim@company.com\nSubject: Critical Security Alert\nReceived: from unknown (185.220.101.47)...\n\nDear Customer, your account has been flagged. Click here to verify...",
            key="raw_source",
        )

    col_btn, _ = st.columns([1.5, 3])
    with col_btn:
        analyze = st.button("🛡️ Run Forensic Analysis", type="primary", use_container_width=True)

    if not analyze:
        # Show empty state guidance when idle
        st.markdown(
            """
            <div class="empty-state-card">
              <div class="empty-state-icon">🛡️</div>
              <div class="empty-state-title">Ready for Threat Investigation</div>
              <div class="empty-state-text">
                Select a sample above or provide an email source to trigger multi-layered forensic inspection.
              </div>
              <div class="capability-tags">
                <span class="capability-tag">MIME Deconstruction</span>
                <span class="capability-tag">TF-IDF & Logistic NLP</span>
                <span class="capability-tag">SPF / DKIM / DMARC Verification</span>
                <span class="capability-tag">GeoIP & ASN Lookup</span>
                <span class="capability-tag">MTA Relay Traversal</span>
                <span class="capability-tag">Forensic PDF Generation</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    filename = "pasted-source.eml"
    source = ""
    if mode == "📤 Upload Email":
        if uploaded is None:
            st.error("Please choose a valid .eml file to upload.")
            return
        source, filename = _read_upload(uploaded)
    elif mode == "📂 Demo Cases":
        choice = st.session_state.get("sample_choice")
        name = SAMPLE_CHOICES.get(choice)
        if not name:
            st.error("Please select a valid demo case from the list.")
            return
        path = SAMPLES_DIR / name
        source = path.read_text(encoding="utf-8", errors="replace")
        filename = name
    else:
        source = (st.session_state.get("raw_source") or "").strip()
        if not source:
            st.error("Please paste the raw email headers and body text.")
            return

    if not source.strip():
        st.error("No email source content available to analyze.")
        return
    _run_pipeline(source, filename)


def render_history() -> None:
    st.markdown(
        """
        <div class="console-card">
          <div class="console-header">
            <div>
              <div class="console-title">🗂️ SOC Forensic Case Archive</div>
              <div class="console-subtitle">Browse previously analyzed incidents. Select any case row to reopen the full intelligence report.</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    rows = list_cases()
    if not rows:
        st.warning("No archived cases found. Execute an analysis to populate the repository.")
        return

    frame = pd.DataFrame(rows)
    frame = frame.rename(
        columns={
            "id": "Case ID",
            "filename": "Filename",
            "sender": "Sender Address",
            "subject": "Subject",
            "verdict": "Verdict",
            "fraud_score": "Risk Index",
            "origin_country": "Origin",
            "analyzed_at": "Timestamp (UTC)",
        }
    )
    event = st.dataframe(
        frame,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        column_config={
            "Case ID": st.column_config.NumberColumn("ID", width="small"),
            "Risk Index": st.column_config.ProgressColumn(
                "Risk Index", min_value=0, max_value=100, format="%d"
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
        case_id = int(frame.iloc[selected[0]]["Case ID"])
        st.session_state.active_case_id = case_id
        st.session_state.from_history = True
        st.rerun()


def main() -> None:
    st.set_page_config(
        page_title="E-UNTHREAT | SOC Threat Intelligence Console",
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
        st.session_state.nav_page = "⚡ Threat Analysis"

    # Backward compatibility for nav string
    current_nav = st.session_state.get("nav_page", "")
    if "History" in current_nav or "history" in current_nav:
        st.session_state.nav_page = "🗂️ Case History"
    else:
        st.session_state.nav_page = "⚡ Threat Analysis"

    page = render_sidebar()

    # Top Status Bar
    render_top_bar()

    # Hero Banner
    st.markdown(
        """
        <div class="hero-header">
          <div class="hero-tagline">
            <span>⚡ NEXT-GEN SOC ENGINE</span>
          </div>
          <h1 class="hero-title">E-Unthreat Intelligence Console</h1>
          <p class="hero-desc">
            Autonomous multi-layer email threat analysis evaluating machine learning content signatures, SPF/DKIM/DMARC cryptographic alignment, sender geolocation, and hop-by-hop MTA relay trajectories.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    active = st.session_state.active_case_id

    if "History" in page or "🗂️" in page:
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
