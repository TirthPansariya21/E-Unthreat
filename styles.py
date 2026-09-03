"""E-UNTHREAT — Dark Cyber SOC Design System & Stylesheet."""

DASHBOARD_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root {
    --bg-base: #090D16;
    --bg-surface: #0F172A;
    --bg-card: rgba(17, 24, 39, 0.75);
    --bg-card-solid: #111827;
    --bg-card-hover: rgba(30, 41, 59, 0.75);
    --border-subtle: rgba(255, 255, 255, 0.08);
    --border-card: rgba(255, 255, 255, 0.1);
    --border-accent: rgba(56, 189, 248, 0.25);
    
    --text-primary: #F8FAFC;
    --text-secondary: #94A3B8;
    --text-muted: #64748B;
    
    --cyan: #38BDF8;
    --cyan-glow: rgba(56, 189, 248, 0.15);
    --blue: #3B82F6;
    
    --danger: #EF4444;
    --danger-text: #FCA5A5;
    --danger-bg: rgba(239, 68, 68, 0.12);
    --danger-border: rgba(239, 68, 68, 0.35);
    --danger-glow: rgba(239, 68, 68, 0.2);
    
    --warning: #F59E0B;
    --warning-text: #FCD34D;
    --warning-bg: rgba(245, 158, 11, 0.12);
    --warning-border: rgba(245, 158, 11, 0.35);
    --warning-glow: rgba(245, 158, 11, 0.2);
    
    --success: #10B981;
    --success-text: #6EE7B7;
    --success-bg: rgba(16, 185, 129, 0.12);
    --success-border: rgba(16, 185, 129, 0.35);
    --success-glow: rgba(16, 185, 129, 0.2);
    
    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 14px;
    --radius-full: 9999px;
}

/* Base resets & typography */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

/* Chrome cleanups */
header[data-testid="stHeader"] {
    background: transparent !important;
    height: 0 !important;
    min-height: 0 !important;
}
[data-testid="stToolbar"], #MainMenu, footer { 
    visibility: hidden; 
    height: 0; 
}
[data-testid="stDecoration"] { 
    display: none !important; 
}

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 3.5rem !important;
    max-width: 1220px !important;
}

/* Monospace elements */
code, pre, .mono, [data-testid="stTextArea"] textarea, .hop-host, .tech-val, .ip-badge {
    font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
}

/* =========================================================================
   TOP STATUS BAR & NAVIGATION
   ========================================================================= */
.top-nav-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 1.25rem;
    background: rgba(15, 23, 42, 0.65);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    margin-bottom: 1.5rem;
}

.top-brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.top-brand-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    background: linear-gradient(135deg, rgba(56, 189, 248, 0.2), rgba(59, 130, 246, 0.2));
    border: 1px solid var(--border-accent);
    border-radius: var(--radius-sm);
    color: var(--cyan);
    font-size: 1.1rem;
    box-shadow: 0 0 12px var(--cyan-glow);
}

.top-brand-title {
    font-weight: 700;
    font-size: 1.1rem;
    letter-spacing: 0.05em;
    color: #FFFFFF;
}

.top-brand-badge {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 0.2rem 0.5rem;
    border-radius: var(--radius-full);
    background: rgba(56, 189, 248, 0.12);
    color: var(--cyan);
    border: 1px solid rgba(56, 189, 248, 0.3);
}

.top-status-indicator {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--text-secondary);
    background: rgba(16, 185, 129, 0.08);
    border: 1px solid rgba(16, 185, 129, 0.2);
    padding: 0.35rem 0.85rem;
    border-radius: var(--radius-full);
}

.pulse-dot {
    width: 8px;
    height: 8px;
    background: var(--success);
    border-radius: 50%;
    box-shadow: 0 0 8px var(--success);
    animation: pulse-glow 2s infinite ease-in-out;
}

@keyframes pulse-glow {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.85); }
}

/* =========================================================================
   PAGE HERO HEADER
   ========================================================================= */
.hero-header {
    margin-bottom: 1.5rem;
    padding: 0.25rem 0;
}

.hero-tagline {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--cyan);
    margin-bottom: 0.35rem;
}

.hero-title {
    font-size: 1.85rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #FFFFFF;
    margin: 0 0 0.4rem 0;
    line-height: 1.2;
}

.hero-desc {
    font-size: 0.95rem;
    color: var(--text-secondary);
    max-width: 780px;
    line-height: 1.5;
    margin: 0;
}

/* =========================================================================
   SIDEBAR STYLING
   ========================================================================= */
[data-testid="stSidebar"] {
    background: #0B0F19 !important;
    border-right: 1px solid var(--border-subtle) !important;
}

.sidebar-header {
    padding: 0.5rem 0 1.25rem 0;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 1.25rem;
}

.sidebar-brand-name {
    font-size: 1.15rem;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: 0.02em;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.sidebar-brand-sub {
    font-size: 0.78rem;
    color: var(--text-muted);
    margin-top: 0.2rem;
}

/* Sidebar Radio Buttons -> Clean Nav Tabs */
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] {
    gap: 0.35rem !important;
    flex-direction: column !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid transparent !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.55rem 0.85rem !important;
    margin: 0 !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(255, 255, 255, 0.05) !important;
    border-color: var(--border-subtle) !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label p,
[data-testid="stSidebar"] [data-testid="stRadio"] label span {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: rgba(56, 189, 248, 0.1) !important;
    border-color: rgba(56, 189, 248, 0.3) !important;
    box-shadow: 0 0 10px rgba(56, 189, 248, 0.1) !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p,
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) span {
    color: var(--cyan) !important;
    font-weight: 600 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child,
[data-testid="stSidebar"] [data-testid="stRadio"] [data-baseweb="radio"] > div:first-child,
[data-testid="stSidebar"] [data-testid="stRadio"] svg {
    display: none !important;
}

/* Sidebar SOC Telemetry Metrics */
.soc-metrics-container {
    margin-top: 1.5rem;
    padding: 1rem;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
}

.soc-metrics-title {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

.soc-stat-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.6rem;
}

.soc-stat-tile {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-sm);
    padding: 0.5rem 0.65rem;
}

.soc-stat-tile.phish { border-left: 3px solid var(--danger); }
.soc-stat-tile.sus { border-left: 3px solid var(--warning); }
.soc-stat-tile.total { border-left: 3px solid var(--cyan); }
.soc-stat-tile.avg { border-left: 3px solid var(--blue); }

.soc-stat-label {
    font-size: 0.7rem;
    color: var(--text-muted);
    font-weight: 500;
}

.soc-stat-val {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-top: 0.15rem;
}

.sidebar-footer-note {
    margin-top: 1.5rem;
    padding: 0.75rem;
    background: rgba(56, 189, 248, 0.03);
    border: 1px dashed rgba(56, 189, 248, 0.2);
    border-radius: var(--radius-sm);
    font-size: 0.72rem;
    color: var(--text-muted);
    line-height: 1.4;
}

/* =========================================================================
   INVESTIGATION CONSOLE (INPUT SECTION)
   ========================================================================= */
.console-card {
    background: var(--bg-card);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border-card);
    border-radius: var(--radius-lg);
    padding: 1.5rem 1.5rem 1.25rem 1.5rem;
    margin-bottom: 1.75rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
    position: relative;
    overflow: hidden;
}

.console-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--cyan), var(--blue), transparent);
}

.console-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.25rem;
    padding-bottom: 0.85rem;
    border-bottom: 1px solid var(--border-subtle);
}

.console-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    letter-spacing: -0.01em;
}

.console-subtitle {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-top: 0.2rem;
}

/* Segmented Control / Input Method Selector */
[data-testid="stSegmentedControl"], [data-testid="stButtonGroup"] {
    background: rgba(15, 23, 42, 0.8) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    padding: 0.25rem !important;
    margin-bottom: 1.25rem !important;
}

[data-testid="stSegmentedControl"] button, [data-testid="stButtonGroup"] button {
    background: transparent !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-secondary) !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 0.45rem 1rem !important;
    transition: all 0.2s ease !important;
}

[data-testid="stSegmentedControl"] button[aria-checked="true"],
[data-testid="stSegmentedControl"] button[aria-pressed="true"],
[data-testid="stButtonGroup"] button[aria-pressed="true"],
[data-testid="stButtonGroup"] button[kind="primary"] {
    background: rgba(56, 189, 248, 0.15) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(56, 189, 248, 0.4) !important;
    box-shadow: 0 0 12px var(--cyan-glow) !important;
    font-weight: 600 !important;
}

/* Styled Inputs inside console */
[data-testid="stSelectbox"] > div > div {
    background: rgba(15, 23, 42, 0.75) !important;
    border: 1px solid var(--border-card) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
}

[data-testid="stFileUploader"] section {
    background: rgba(15, 23, 42, 0.5) !important;
    border: 2px dashed rgba(56, 189, 248, 0.25) !important;
    border-radius: var(--radius-md) !important;
    padding: 1.5rem !important;
    transition: all 0.2s ease !important;
}

[data-testid="stFileUploader"] section:hover {
    border-color: var(--cyan) !important;
    background: rgba(56, 189, 248, 0.05) !important;
}

[data-testid="stTextArea"] textarea {
    background: rgba(15, 23, 42, 0.75) !important;
    border: 1px solid var(--border-card) !important;
    border-radius: var(--radius-md) !important;
    color: var(--cyan) !important;
    font-size: 0.85rem !important;
    line-height: 1.5 !important;
    padding: 0.75rem !important;
}

/* Primary Action Buttons */
.block-container [data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
    border: 1px solid rgba(56, 189, 248, 0.4) !important;
    color: #FFFFFF !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.6rem !important;
    border-radius: var(--radius-md) !important;
    box-shadow: 0 0 20px rgba(2, 132, 199, 0.35) !important;
    transition: all 0.25s ease !important;
    letter-spacing: 0.02em;
}

.block-container [data-testid="stButton"] > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #0369A1 0%, #0284C7 100%) !important;
    border-color: var(--cyan) !important;
    box-shadow: 0 0 25px rgba(56, 189, 248, 0.5) !important;
    transform: translateY(-1px);
}

.block-container [data-testid="stButton"] > button[kind="secondary"],
.block-container [data-testid="stDownloadButton"] > button {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid var(--border-card) !important;
    color: var(--text-primary) !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    padding: 0.55rem 1.25rem !important;
    border-radius: var(--radius-md) !important;
    transition: all 0.2s ease !important;
}

.block-container [data-testid="stButton"] > button[kind="secondary"]:hover,
.block-container [data-testid="stDownloadButton"] > button:hover {
    background: rgba(255, 255, 255, 0.08) !important;
    border-color: rgba(255, 255, 255, 0.2) !important;
    color: #FFFFFF !important;
}

/* =========================================================================
   EMPTY STATE / READY FOR INVESTIGATION
   ========================================================================= */
.empty-state-card {
    background: rgba(17, 24, 39, 0.4);
    border: 1px dashed var(--border-card);
    border-radius: var(--radius-lg);
    padding: 3rem 2rem;
    text-align: center;
    margin: 1.5rem 0;
}

.empty-state-icon {
    width: 56px;
    height: 56px;
    background: rgba(56, 189, 248, 0.08);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 1.6rem;
    color: var(--cyan);
    margin-bottom: 1.25rem;
    box-shadow: 0 0 20px rgba(56, 189, 248, 0.15);
}

.empty-state-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 0.5rem;
}

.empty-state-text {
    font-size: 0.9rem;
    color: var(--text-secondary);
    max-width: 500px;
    margin: 0 auto 1.5rem auto;
    line-height: 1.5;
}

.capability-tags {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.6rem;
    max-width: 700px;
    margin: 0 auto;
}

.capability-tag {
    font-size: 0.75rem;
    font-weight: 500;
    padding: 0.35rem 0.75rem;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-full);
    color: var(--text-secondary);
}

/* =========================================================================
   ANALYSIS RESULTS: VERDICT BANNER & THREAT SCORE
   ========================================================================= */
.verdict-card {
    background: var(--bg-card);
    backdrop-filter: blur(16px);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    margin-bottom: 1.25rem;
    border: 1px solid var(--border-card);
    position: relative;
    overflow: hidden;
}

.verdict-card.phishing {
    border-color: var(--danger-border);
    box-shadow: 0 0 30px var(--danger-glow);
}
.verdict-card.phishing::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, var(--danger), #F87171);
}

.verdict-card.suspicious {
    border-color: var(--warning-border);
    box-shadow: 0 0 30px var(--warning-glow);
}
.verdict-card.suspicious::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, var(--warning), #FBBF24);
}

.verdict-card.legitimate {
    border-color: var(--success-border);
    box-shadow: 0 0 30px var(--success-glow);
}
.verdict-card.legitimate::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, var(--success), #34D399);
}

.verdict-top-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.5rem;
}

.verdict-badge {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 0.25rem 0.65rem;
    border-radius: var(--radius-full);
}
.verdict-badge.phishing {
    background: var(--danger-bg);
    color: var(--danger-text);
    border: 1px solid var(--danger-border);
}
.verdict-badge.suspicious {
    background: var(--warning-bg);
    color: var(--warning-text);
    border: 1px solid var(--warning-border);
}
.verdict-badge.legitimate {
    background: var(--success-bg);
    color: var(--success-text);
    border: 1px solid var(--success-border);
}

.verdict-headline {
    font-size: 1.6rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 0 0 0.4rem 0;
    color: #FFFFFF;
}
.verdict-headline.phishing { color: #FCA5A5; }
.verdict-headline.suspicious { color: #FCD34D; }
.verdict-headline.legitimate { color: #6EE7B7; }

.verdict-summary {
    font-size: 0.95rem;
    color: var(--text-secondary);
    line-height: 1.5;
    margin: 0;
}

/* =========================================================================
   EMAIL METADATA OVERVIEW CARDS
   ========================================================================= */
.meta-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 0.85rem;
    margin-bottom: 1.25rem;
}

.meta-card {
    background: rgba(17, 24, 39, 0.7);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 0.9rem 1.1rem;
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.meta-card:hover {
    border-color: rgba(255, 255, 255, 0.15);
    transform: translateY(-1px);
}

.meta-card-label {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    margin-bottom: 0.35rem;
}

.meta-card-value {
    font-size: 0.92rem;
    font-weight: 500;
    color: var(--text-primary);
    word-break: break-word;
    line-height: 1.4;
}

.meta-card-value.mono {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem;
    color: #E2E8F0;
}

/* =========================================================================
   AUTHENTICATION MATRIX & ML CLASSIFIER CARDS
   ========================================================================= */
.section-title-wrap {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 1.5rem 0 0.85rem 0;
}

.soc-section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    letter-spacing: -0.01em;
}

.soc-panel {
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    border-radius: var(--radius-lg);
    padding: 1.25rem;
    margin-bottom: 1.25rem;
    height: 100%;
}

.panel-header-title {
    font-size: 0.88rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-secondary);
    margin-bottom: 0.85rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

.auth-cards-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.65rem;
}

.auth-badge-box {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 0.75rem 0.85rem;
    text-align: center;
}

.auth-badge-box.ok {
    border-color: var(--success-border);
    background: rgba(16, 185, 129, 0.05);
}
.auth-badge-box.bad {
    border-color: var(--danger-border);
    background: rgba(239, 68, 68, 0.05);
}
.auth-badge-box.warn {
    border-color: var(--warning-border);
    background: rgba(245, 158, 11, 0.05);
}

.auth-proto-name {
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--text-muted);
    letter-spacing: 0.06em;
    margin-bottom: 0.35rem;
}

.auth-status-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    font-size: 0.82rem;
    font-weight: 700;
    padding: 0.2rem 0.6rem;
    border-radius: var(--radius-sm);
}

.auth-badge-box.ok .auth-status-chip {
    color: var(--success-text);
    background: var(--success-bg);
}
.auth-badge-box.bad .auth-status-chip {
    color: var(--danger-text);
    background: var(--danger-bg);
}
.auth-badge-box.warn .auth-status-chip {
    color: var(--warning-text);
    background: var(--warning-bg);
}

/* ML Classifier Card Styling */
.ml-metric-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.6rem;
}

.ml-metric-label {
    font-size: 0.8rem;
    color: var(--text-secondary);
}

.ml-metric-val {
    font-size: 0.88rem;
    font-weight: 700;
    color: #FFFFFF;
}

.ml-bar-bg {
    width: 100%;
    height: 8px;
    background: rgba(255, 255, 255, 0.06);
    border-radius: var(--radius-full);
    overflow: hidden;
    margin-top: 0.4rem;
}

.ml-bar-fill {
    height: 100%;
    border-radius: var(--radius-full);
    transition: width 0.6s ease;
}

.ml-bar-fill.phish {
    background: linear-gradient(90deg, #EF4444, #F87171);
    box-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
}
.ml-bar-fill.legit {
    background: linear-gradient(90deg, #10B981, #34D399);
    box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
}

/* =========================================================================
   THREAT EVIDENCE SECTION
   ========================================================================= */
.evidence-container {
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    border-radius: var(--radius-lg);
    padding: 1.25rem;
    margin-bottom: 1.5rem;
}

.evidence-category-title {
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--cyan);
    margin: 1rem 0 0.65rem 0;
    display: flex;
    align-items: center;
    gap: 0.45rem;
}

.evidence-category-title:first-child {
    margin-top: 0;
}

.flag-card {
    display: flex;
    align-items: flex-start;
    gap: 0.85rem;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 0.75rem 1rem;
    margin-bottom: 0.55rem;
    transition: border-color 0.2s ease;
}

.flag-card.bad {
    border-left: 3px solid var(--danger);
}
.flag-card.warn {
    border-left: 3px solid var(--warning);
}
.flag-card.ok {
    border-left: 3px solid var(--success);
}

.flag-status-icon {
    font-size: 0.95rem;
    font-weight: 700;
    margin-top: 0.1rem;
}
.flag-card.bad .flag-status-icon { color: var(--danger); }
.flag-card.warn .flag-status-icon { color: var(--warning); }
.flag-card.ok .flag-status-icon { color: var(--success); }

.flag-info {
    flex: 1;
}

.flag-title-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
}

.flag-name {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-primary);
}

.flag-tag {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 0.15rem 0.45rem;
    border-radius: var(--radius-sm);
}

.flag-card.bad .flag-tag { background: var(--danger-bg); color: var(--danger-text); }
.flag-card.warn .flag-tag { background: var(--warning-bg); color: var(--warning-text); }
.flag-card.ok .flag-tag { background: var(--success-bg); color: var(--success-text); }

.flag-explanation {
    font-size: 0.82rem;
    color: var(--text-secondary);
    line-height: 1.45;
    margin-top: 0.25rem;
}

/* =========================================================================
   HOP-BY-HOP RELAY PATH TIMELINE
   ========================================================================= */
.timeline-container {
    position: relative;
    padding: 0.5rem 0 0.5rem 1.75rem;
}

.timeline-container::before {
    content: '';
    position: absolute;
    top: 15px;
    bottom: 15px;
    left: 11px;
    width: 2px;
    background: linear-gradient(180deg, var(--cyan), var(--blue));
    opacity: 0.4;
}

.timeline-node {
    position: relative;
    margin-bottom: 1rem;
}

.timeline-node:last-child {
    margin-bottom: 0;
}

.node-marker {
    position: absolute;
    left: -1.75rem;
    top: 0.2rem;
    width: 20px;
    height: 20px;
    background: #0F172A;
    border: 2px solid var(--cyan);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--cyan);
    box-shadow: 0 0 10px var(--cyan-glow);
}

.node-card {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 0.65rem 0.85rem;
}

.node-role {
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--cyan);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.2rem;
}

.node-host {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: var(--text-primary);
    word-break: break-all;
}

/* =========================================================================
   MAP & LOCATION STYLING
   ========================================================================= */
.map-frame-container {
    border: 1px solid var(--border-card);
    border-radius: var(--radius-md);
    overflow: hidden;
    background: #0B0F19;
}

.location-meta-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.6rem 0.85rem;
    background: rgba(15, 23, 42, 0.7);
    border-bottom: 1px solid var(--border-subtle);
    font-size: 0.8rem;
}

.loc-pill {
    font-weight: 600;
    color: #FFFFFF;
}

.vpn-pill {
    font-size: 0.72rem;
    font-weight: 600;
    padding: 0.15rem 0.5rem;
    border-radius: var(--radius-full);
}

.vpn-pill.flagged {
    background: var(--warning-bg);
    color: var(--warning-text);
    border: 1px solid var(--warning-border);
}
.vpn-pill.clean {
    background: var(--success-bg);
    color: var(--success-text);
    border: 1px solid var(--success-border);
}

/* =========================================================================
   ACTION FOOTER TOOLBAR
   ========================================================================= */
.action-toolbar {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 1.5rem;
    padding-top: 1.25rem;
    border-top: 1px solid var(--border-subtle);
}

/* =========================================================================
   CASE HISTORY DATAFRAME TWEAKS
   ========================================================================= */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border-card) !important;
    border-radius: var(--radius-md) !important;
    overflow: hidden;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .block-container {
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
    }
    .auth-cards-row {
        grid-template-columns: 1fr;
    }
    .top-nav-bar {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.75rem;
    }
    .action-toolbar {
        flex-direction: column;
        align-items: stretch;
    }
}
</style>
"""

