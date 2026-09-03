"""Single injected stylesheet — light editorial UI over Streamlit chrome."""

DASHBOARD_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
    --bg: #F7F8FA;
    --surface: #FFFFFF;
    --hairline: #E3E7EC;
    --ink: #1E2530;
    --muted: #69707D;
    --accent: #1E6E63;
    --ok: #2F8F6C;
    --warn: #B8863A;
    --bad: #B94A3D;
    --title: 1.75rem;
    --heading: 1.15rem;
    --text: 0.95rem;
}

html, body, [data-testid="stAppViewContainer"], .stApp, .stMarkdown, p, span, label {
    font-family: Inter, "Segoe UI", sans-serif;
    font-size: var(--text);
    color: var(--ink);
}

html, body, [data-testid="stAppViewContainer"], .stApp {
    background: var(--bg) !important;
}

/* Collapse Streamlit's empty top chrome so content sits under the title */
header[data-testid="stHeader"] {
    background: transparent;
    height: 0 !important;
    min-height: 0 !important;
    border: none !important;
}
[data-testid="stToolbar"], #MainMenu, footer { visibility: hidden; height: 0; }

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--hairline);
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
    font-family: Inter, sans-serif !important;
    font-size: var(--text) !important;
    font-weight: 400 !important;
}
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: var(--muted) !important;
    font-size: var(--text) !important;
}

.block-container {
    padding-top: 0.85rem !important;
    padding-bottom: 3.5rem !important;
    max-width: 1080px;
}

/* --- Type scale: title / heading / body only --- */
.page-header { margin: 0 0 1rem 0; }
.page-header h1,
.verdict-word,
.eut-name,
.side-stat .v {
    font-family: "Source Serif 4", Georgia, serif !important;
    font-size: var(--title) !important;
    font-weight: 600 !important;
    line-height: 1.2;
    letter-spacing: -0.015em;
    color: var(--ink);
}
.eut-name { font-size: var(--heading) !important; margin: 0; }
.side-stat .v { font-size: var(--heading) !important; }

.section-heading,
.group-title,
.block-container [data-testid="stWidgetLabel"] p,
.block-container [data-testid="stWidgetLabel"] label,
.block-container label[data-testid="stWidgetLabel"],
.block-container .stSelectbox label p,
.block-container [data-testid="stFileUploader"] label p,
.block-container [data-testid="stTextArea"] label p {
    font-family: "Source Serif 4", Georgia, serif !important;
    font-size: var(--heading) !important;
    font-weight: 600 !important;
    color: var(--ink) !important;
    letter-spacing: -0.01em;
    text-transform: none !important;
}

.page-header p,
.verdict-explain,
.meta-item .k,
.meta-item .v,
.auth-line,
.flag-name,
.flag-why,
.pair-caption,
.history-hint,
.eut-sub,
.eut-kicker,
.side-stat .k,
.hop-role,
p, li, .stMarkdown p {
    font-family: Inter, sans-serif;
    font-size: var(--text) !important;
    font-weight: 400;
    line-height: 1.6;
}

.page-header p,
.verdict-explain,
.meta-item .k,
.flag-why,
.pair-caption,
.history-hint,
.eut-sub,
.side-stat .k,
.hop-role {
    color: var(--muted);
}

.meta-item .v.mono,
.hop-host,
.hop-num,
[data-testid="stTextArea"] textarea {
    font-family: "IBM Plex Mono", ui-monospace, monospace !important;
}

/* Sidebar brand */
.eut-brand { margin: 0 0 0.35rem 0; }
.eut-sub { margin-top: 0.15rem; }

/* Sidebar nav: hide radio discs, treat labels as text links */
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] {
    gap: 0 !important;
    flex-direction: column !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: transparent !important;
    border: none !important;
    border-left: 2px solid transparent !important;
    border-radius: 0 !important;
    padding: 0.38rem 0.2rem 0.38rem 0.7rem !important;
    margin: 0 !important;
    box-shadow: none !important;
    justify-content: flex-start !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label p,
[data-testid="stSidebar"] [data-testid="stRadio"] label span {
    font-family: Inter, sans-serif !important;
    font-size: var(--text) !important;
    font-weight: 400 !important;
    color: var(--muted) !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    border-left-color: var(--accent) !important;
    background: transparent !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p,
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) span {
    color: var(--accent) !important;
    font-weight: 500 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child,
[data-testid="stSidebar"] [data-testid="stRadio"] [data-baseweb="radio"] > div:first-child,
[data-testid="stSidebar"] [data-testid="stRadio"] svg {
    display: none !important;
}

/* Stats as one tight group */
.side-stats {
    display: flex;
    flex-direction: column;
    gap: 0.45rem;
    margin: 1.15rem 0 0.9rem 0;
}
.side-stat { margin: 0; }
.side-stat .k { margin-bottom: 0; line-height: 1.3; }
.side-stat .v { line-height: 1.2; }

/* Unified input panel: one outer hairline, no inner boxes */
.input-panel-marker { display: none; }
[data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .input-panel-marker) {
    border: 1px solid var(--hairline) !important;
    background: var(--surface);
    border-radius: 4px;
    padding: 0.65rem 1.15rem 0.85rem !important;
    gap: 0.35rem !important;
}
[data-testid="stVerticalBlock"]:has(.input-panel-marker) [data-testid="stWidgetLabel"] {
    display: none !important;
}

/* Segmented control → quiet text tabs */
[data-testid="stVerticalBlock"]:has(.input-panel-marker) [data-testid="stButtonGroup"],
[data-testid="stVerticalBlock"]:has(.input-panel-marker) [data-testid="stSegmentedControl"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 0 0.35rem 0 !important;
    margin-bottom: 0.25rem;
}
[data-testid="stVerticalBlock"]:has(.input-panel-marker) [data-testid="stButtonGroup"] button,
[data-testid="stVerticalBlock"]:has(.input-panel-marker) [data-testid="stSegmentedControl"] button {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    color: var(--muted) !important;
    font-family: Inter, sans-serif !important;
    font-size: var(--text) !important;
    font-weight: 400 !important;
    padding: 0.3rem 0.8rem 0.45rem !important;
}
[data-testid="stVerticalBlock"]:has(.input-panel-marker) [data-testid="stButtonGroup"] button[kind="primary"],
[data-testid="stVerticalBlock"]:has(.input-panel-marker) [data-testid="stButtonGroup"] button[aria-pressed="true"],
[data-testid="stVerticalBlock"]:has(.input-panel-marker) [data-testid="stSegmentedControl"] button[aria-checked="true"],
[data-testid="stVerticalBlock"]:has(.input-panel-marker) [data-testid="stSegmentedControl"] button[aria-pressed="true"] {
    background: transparent !important;
    color: var(--ink) !important;
    border-bottom-color: var(--accent) !important;
    font-weight: 500 !important;
}

/* Strip select / upload / textarea chrome inside the panel */
[data-testid="stVerticalBlock"]:has(.input-panel-marker) [data-testid="stSelectbox"] > div > div,
[data-testid="stVerticalBlock"]:has(.input-panel-marker) [data-baseweb="select"] > div {
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid var(--hairline) !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    min-height: 2.4rem;
}
[data-testid="stVerticalBlock"]:has(.input-panel-marker) [data-testid="stFileUploader"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
[data-testid="stVerticalBlock"]:has(.input-panel-marker) [data-testid="stFileUploader"] section,
[data-testid="stVerticalBlock"]:has(.input-panel-marker) [data-testid="stFileUploaderDropzone"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0.35rem 0 !important;
}
[data-testid="stVerticalBlock"]:has(.input-panel-marker) [data-testid="stFileUploaderDropzoneInstructions"] {
    color: var(--muted) !important;
}
[data-testid="stVerticalBlock"]:has(.input-panel-marker) [data-testid="stTextArea"] textarea {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    border-radius: 0 !important;
    padding: 0.4rem 0 !important;
    color: var(--ink) !important;
    font-size: var(--text) !important;
}

/* Analyze button: hug the label, 4px corners, left aligned */
[data-testid="stVerticalBlock"]:has(.input-panel-marker) [data-testid="stRadio"] [role="radiogroup"] {
    flex-direction: row !important;
    gap: 0.15rem !important;
    background: transparent !important;
}
[data-testid="stVerticalBlock"]:has(.input-panel-marker) [data-testid="stRadio"] label {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    padding: 0.3rem 0.8rem 0.45rem !important;
    box-shadow: none !important;
}
[data-testid="stVerticalBlock"]:has(.input-panel-marker) [data-testid="stRadio"] label > div:first-child {
    display: none !important;
}
[data-testid="stVerticalBlock"]:has(.input-panel-marker) [data-testid="stRadio"] label:has(input:checked) {
    border-bottom-color: var(--accent) !important;
}

.block-container [data-testid="stButton"] {
    width: auto !important;
    text-align: left;
}
.block-container [data-testid="stButton"] > button,
.block-container [data-testid="stDownloadButton"] > button {
    width: auto !important;
    min-width: 0 !important;
    border-radius: 4px !important;
    font-family: Inter, sans-serif !important;
    font-size: var(--text) !important;
    font-weight: 500 !important;
    padding: 0.42rem 1.1rem !important;
    box-shadow: none !important;
}
.block-container [data-testid="stButton"] > button[kind="primary"],
.block-container [data-testid="stDownloadButton"] > button[kind="primary"] {
    background: var(--accent) !important;
    border: 1px solid var(--accent) !important;
    color: #fff !important;
}
.block-container [data-testid="stButton"] > button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid var(--hairline) !important;
    color: var(--ink) !important;
}

.verdict-banner {
    padding: 0.2rem 0 0.2rem 1.1rem;
    margin: 0 0 1.25rem 0;
    border-left: 3px solid var(--muted);
    animation: result-fade 0.55s ease;
}
.verdict-banner.phishing { border-left-color: var(--bad); }
.verdict-banner.suspicious { border-left-color: var(--warn); }
.verdict-banner.legitimate { border-left-color: var(--ok); }
.verdict-word { margin: 0; }
.verdict-word.phishing { color: var(--bad) !important; }
.verdict-word.suspicious { color: var(--warn) !important; }
.verdict-word.legitimate { color: var(--ok) !important; }
.verdict-explain { margin: 0.4rem 0 0 0; max-width: 40rem; }

@keyframes result-fade {
    from { opacity: 0; }
    to { opacity: 1; }
}

.meta-row {
    display: flex;
    flex-wrap: wrap;
    gap: 1.4rem 2.75rem;
    margin: 0 0 1.35rem 0;
}
.meta-item .k { margin-bottom: 0.15rem; }
.meta-item .v { color: var(--ink); word-break: break-word; }

.auth-stack {
    margin: 0 0 1.75rem 0;
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
}
.auth-line {
    display: flex;
    align-items: baseline;
    gap: 0.45rem;
}
.auth-line .lbl { color: var(--muted); }
.auth-line.ok .mark, .auth-line.ok .val { color: var(--ok); }
.auth-line.warn .mark, .auth-line.warn .val { color: var(--warn); }
.auth-line.bad .mark, .auth-line.bad .val { color: var(--bad); }

.evidence { margin: 0.2rem 0 2rem 0; }
.section-heading { margin: 0 0 0.85rem 0; }
.evidence-group { padding: 0.1rem 0 1.1rem 0; }
.evidence-group + .evidence-group {
    border-top: 1px solid var(--hairline);
    padding-top: 1.15rem;
}
.group-title { margin: 0 0 0.7rem 0; }
.flag {
    display: grid;
    grid-template-columns: 1.1rem 1fr;
    column-gap: 0.55rem;
    margin: 0 0 0.85rem 0;
}
.flag .mark { margin-top: 0.2rem; color: var(--muted); }
.flag.ok .mark { color: var(--ok); }
.flag.warn .mark { color: var(--warn); }
.flag.bad .mark { color: var(--bad); }
.flag-name { color: var(--ink) !important; }
.flag-why { margin-top: 0.1rem; max-width: 42rem; }
.pair-caption { margin: -0.2rem 0 0.75rem 0; }

.hop {
    display: grid;
    grid-template-columns: 1.5rem 1fr;
    column-gap: 0.65rem;
    margin: 0 0 0.85rem 0;
}
.hop-num { color: var(--muted); padding-top: 0.1rem; }
.hop-host { color: var(--ink); line-height: 1.5; }

.history-hint { margin: 0 0 0.85rem 0; }

/* Landing strip: three signal channels shown before first analysis */
.landing-strip {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0 2.5rem;
    margin: 2.75rem 0 0 0;
    padding-top: 2rem;
    border-top: 1px solid var(--hairline);
}
.landing-col { max-width: 24rem; }
.landing-title {
    font-family: "Source Serif 4", Georgia, serif;
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--ink);
    margin-bottom: 0.5rem;
    letter-spacing: -0.01em;
}
.landing-body {
    font-family: Inter, sans-serif;
    font-size: 0.88rem;
    line-height: 1.6;
    color: var(--muted);
}
@media (max-width: 900px) {
    .landing-strip { grid-template-columns: 1fr; gap: 1.75rem; }
}

hr { border-color: var(--hairline) !important; }
</style>
"""
