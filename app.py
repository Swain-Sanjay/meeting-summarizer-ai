import streamlit as st
from dotenv import load_dotenv
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, asked_question

load_dotenv()

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Vox — AI Video Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════════
# CSS — PREMIUM DARK THEME
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Outfit:wght@200;300;400;500;600;700;800;900&family=JetBrains+Mono:wght@300;400;500;600&display=swap');

/* ── CSS Variables ── */
:root {
    --bg-base:      #060810;
    --bg-surface:   #0c0f1a;
    --bg-raised:    #111528;
    --bg-overlay:   #161b30;
    --bg-hover:     #1c2240;

    --border-dim:   rgba(99,130,255,0.10);
    --border-mid:   rgba(99,130,255,0.20);
    --border-bright:rgba(99,130,255,0.40);

    --cyan:         #00e5ff;
    --cyan-dim:     rgba(0,229,255,0.15);
    --cyan-glow:    rgba(0,229,255,0.35);
    --purple:       #7c6ff7;
    --purple-dim:   rgba(124,111,247,0.15);
    --purple-glow:  rgba(124,111,247,0.35);
    --pink:         #f471b5;
    --pink-dim:     rgba(244,113,181,0.12);
    --green:        #00ffa3;
    --green-dim:    rgba(0,255,163,0.12);
    --amber:        #ffb347;
    --amber-dim:    rgba(255,179,71,0.12);

    --text-primary:  #eef0ff;
    --text-secondary:#8892c4;
    --text-muted:    #3d4670;

    --font-display: 'Outfit', sans-serif;
    --font-body:    'Space Grotesk', sans-serif;
    --font-mono:    'JetBrains Mono', monospace;

    --radius-sm:    8px;
    --radius-md:    14px;
    --radius-lg:    20px;
    --radius-xl:    28px;

    --shadow-card:  0 4px 32px rgba(0,0,0,0.5), 0 0 0 1px rgba(99,130,255,0.08);
    --shadow-glow-c:0 0 40px rgba(0,229,255,0.15);
    --shadow-glow-p:0 0 40px rgba(124,111,247,0.20);
}

/* ── Global Reset ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: var(--font-body);
    color: var(--text-primary);
}

/* ── Animated Background ── */
.stApp {
    background: var(--bg-base);
    min-height: 100vh;
}
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 900px 600px at 15% 0%,   rgba(0,229,255,0.055) 0%, transparent 65%),
        radial-gradient(ellipse 700px 500px at 85% 10%,  rgba(124,111,247,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 600px 800px at 70% 90%,  rgba(244,113,181,0.04) 0%, transparent 60%),
        radial-gradient(ellipse 400px 400px at 10% 80%,  rgba(0,255,163,0.03) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
    animation: bgShift 20s ease-in-out infinite alternate;
}
@keyframes bgShift {
    0%   { opacity: 1; }
    50%  { opacity: 0.7; }
    100% { opacity: 1; }
}

/* ── Noise Texture Overlay ── */
.stApp::after {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
    opacity: 0.4;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #090c18 0%, #060810 100%) !important;
    border-right: 1px solid var(--border-dim) !important;
    width: 280px !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
}
[data-testid="stSidebar"] .block-container {
    padding: 0 !important;
}

/* ── Main Content ── */
.main .block-container {
    padding: 2rem 2.5rem 4rem 2.5rem !important;
    max-width: 1400px !important;
    position: relative;
    z-index: 1;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(99,130,255,0.25);
    border-radius: 2px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(0,229,255,0.4); }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer .stDeployButton {
  display: none !important; 
    }

/* ── Progress Bar ── */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--cyan), var(--purple), var(--pink)) !important;
    border-radius: 999px !important;
    animation: shimmer 2s linear infinite;
    background-size: 200% 100% !important;
}
.stProgress > div {
    background: rgba(99,130,255,0.08) !important;
    border-radius: 999px !important;
    height: 3px !important;
}
@keyframes shimmer {
    0%   { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #1a2050 0%, #242b5e 100%) !important;
    color: var(--cyan) !important;
    border: 1px solid rgba(0,229,255,0.25) !important;
    border-radius: var(--radius-md) !important;
    font-family: var(--font-body) !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 0.6rem 1.5rem !important;
    letter-spacing: 0.04em !important;
    transition: all 0.25s cubic-bezier(0.4,0,0.2,1) !important;
    box-shadow: 0 0 20px rgba(0,229,255,0.08), inset 0 1px 0 rgba(255,255,255,0.05) !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0,229,255,0.08), transparent);
    transition: left 0.4s ease;
}
.stButton > button:hover::before { left: 100%; }
.stButton > button:hover {
    border-color: rgba(0,229,255,0.55) !important;
    box-shadow: 0 0 30px rgba(0,229,255,0.18), 0 4px 20px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.08) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Run button special */
.run-btn .stButton > button {
    background: linear-gradient(135deg, #0d3b4f 0%, #0a2d3d 100%) !important;
    border-color: rgba(0,229,255,0.4) !important;
    color: var(--cyan) !important;
    font-size: 0.9rem !important;
    box-shadow: 0 0 30px rgba(0,229,255,0.12), inset 0 1px 0 rgba(0,229,255,0.1) !important;
}

/* ── Text Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--bg-raised) !important;
    border: 1px solid var(--border-dim) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.82rem !important;
    padding: 0.65rem 1rem !important;
    transition: all 0.2s ease !important;
    caret-color: var(--cyan) !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(0,229,255,0.4) !important;
    box-shadow: 0 0 0 3px rgba(0,229,255,0.08), 0 0 20px rgba(0,229,255,0.06) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder { color: var(--text-muted) !important; }

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: var(--bg-raised) !important;
    border: 1px solid var(--border-dim) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
    font-size: 0.85rem !important;
}
.stSelectbox > div > div:hover { border-color: var(--border-mid) !important; }

/* ── Download Button ── */
.stDownloadButton > button {
    background: var(--bg-raised) !important;
    border: 1px solid var(--border-dim) !important;
    color: var(--text-secondary) !important;
    border-radius: var(--radius-md) !important;
    font-family: var(--font-body) !important;
    font-size: 0.82rem !important;
}
.stDownloadButton > button:hover {
    border-color: rgba(0,255,163,0.35) !important;
    color: var(--green) !important;
    box-shadow: 0 0 20px rgba(0,255,163,0.08) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-surface) !important;
    border-radius: var(--radius-lg) !important;
    padding: 5px !important;
    gap: 2px !important;
    border: 1px solid var(--border-dim) !important;
    display: inline-flex !important;
    margin-bottom: 1.5rem !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    font-family: var(--font-body) !important;
    font-weight: 500 !important;
    font-size: 0.84rem !important;
    letter-spacing: 0.02em !important;
    border-radius: var(--radius-md) !important;
    border: none !important;
    padding: 0.5rem 1.4rem !important;
    transition: all 0.2s ease !important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--text-secondary) !important; }
.stTabs [aria-selected="true"] {
    background: var(--bg-overlay) !important;
    color: var(--cyan) !important;
    box-shadow: 0 0 20px rgba(0,229,255,0.1), inset 0 1px 0 rgba(0,229,255,0.1) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ── Spinner ── */
.stSpinner > div {
    border-color: var(--cyan) transparent transparent transparent !important;
}

/* ── Warning / Error / Success ── */
.stAlert {
    background: var(--bg-raised) !important;
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border-dim) !important;
    font-family: var(--font-body) !important;
    font-size: 0.85rem !important;
}
.stSuccess {
    border-color: rgba(0,255,163,0.3) !important;
    color: var(--green) !important;
}
.stWarning { border-color: rgba(255,179,71,0.3) !important; }
.stError   { border-color: rgba(255,80,80,0.3) !important; }

/* ════════════════════════════════════════
   CUSTOM COMPONENTS
════════════════════════════════════════ */

/* ── Sidebar Brand ── */
.sb-brand {
    padding: 1.75rem 1.5rem 1.25rem;
    border-bottom: 1px solid var(--border-dim);
    margin-bottom: 0.5rem;
}
.sb-logo {
    font-family: var(--font-display);
    font-weight: 900;
    font-size: 1.6rem;
    letter-spacing: -0.04em;
    background: linear-gradient(135deg, var(--cyan) 0%, var(--purple) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}
.sb-tagline {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-top: 0.25rem;
}

/* ── Sidebar Nav Labels ── */
.sb-label {
    font-family: var(--font-mono);
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--text-muted);
    padding: 0.8rem 1.5rem 0.3rem;
    margin: 0;
}

/* ── Sidebar Divider ── */
.sb-divider {
    height: 1px;
    background: var(--border-dim);
    margin: 0.75rem 1.5rem;
}

/* ── Sidebar Status ── */
.sb-status {
    margin: 0.75rem 1.5rem;
    padding: 0.65rem 1rem;
    background: rgba(0,255,163,0.05);
    border: 1px solid rgba(0,255,163,0.18);
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.sb-status-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 8px var(--green);
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; box-shadow: 0 0 8px var(--green); }
    50%       { opacity: 0.6; box-shadow: 0 0 16px var(--green); }
}
.sb-status-text {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--green);
}

/* ── Sidebar Info Items ── */
.sb-info-grid {
    padding: 0.5rem 1.5rem 1rem;
    display: grid;
    gap: 0.4rem;
}
.sb-info-item {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.5rem 0.75rem;
    border-radius: var(--radius-sm);
    background: rgba(99,130,255,0.04);
    font-family: var(--font-body);
    font-size: 0.78rem;
    color: var(--text-secondary);
    letter-spacing: 0.01em;
    transition: all 0.2s;
}
.sb-info-item:hover {
    background: rgba(0,229,255,0.06);
    color: var(--text-primary);
}

/* ── Hero ── */
.hero-wrap {
    padding: 0.5rem 0 2rem;
}
.hero-eyebrow {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--cyan);
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.hero-eyebrow::before {
    content: '';
    display: inline-block;
    width: 20px; height: 1px;
    background: var(--cyan);
    opacity: 0.7;
}
.hero-title {
    font-family: var(--font-display);
    font-weight: 800;
    font-size: clamp(2rem, 4vw, 3.2rem);
    letter-spacing: -0.04em;
    line-height: 1.05;
    color: var(--text-primary);
    margin: 0;
    padding: 0;
}
.hero-title span {
    background: linear-gradient(135deg, var(--cyan) 0%, var(--purple) 50%, var(--pink) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-family: var(--font-body);
    font-size: 0.92rem;
    color: var(--text-muted);
    margin-top: 0.6rem;
    letter-spacing: 0.01em;
}

/* ── Card ── */
.card {
    background: var(--bg-surface);
    border: 1px solid var(--border-dim);
    border-radius: var(--radius-lg);
    padding: 1.5rem 1.75rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
    box-shadow: var(--shadow-card);
}
.card:hover {
    border-color: var(--border-mid);
}
.card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg,
        transparent 0%,
        rgba(0,229,255,0.3) 30%,
        rgba(124,111,247,0.3) 70%,
        transparent 100%);
    opacity: 0;
    transition: opacity 0.3s;
}
.card:hover::after { opacity: 1; }

/* Accented card variants */
.card-cyan  { border-color: rgba(0,229,255,0.18) !important; }
.card-purple{ border-color: rgba(124,111,247,0.18) !important; }
.card-pink  { border-color: rgba(244,113,181,0.18) !important; }
.card-green { border-color: rgba(0,255,163,0.18) !important; }

/* ── Card Label ── */
.card-label {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.card-label-accent { color: var(--cyan); }

/* ── Card Content ── */
.card-content {
    color: var(--text-secondary);
    font-size: 0.875rem;
    line-height: 1.85;
    font-family: var(--font-body);
}

/* ── Title Banner ── */
.title-banner {
    background: linear-gradient(135deg, rgba(0,229,255,0.04) 0%, rgba(124,111,247,0.04) 100%);
    border: 1px solid rgba(0,229,255,0.15);
    border-radius: var(--radius-lg);
    padding: 1.25rem 1.75rem;
    margin-bottom: 1.75rem;
    position: relative;
    overflow: hidden;
}
.title-banner::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, var(--cyan), var(--purple));
    border-radius: 0 2px 2px 0;
}
.title-banner-label {
    font-family: var(--font-mono);
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--cyan);
    margin-bottom: 0.4rem;
    opacity: 0.7;
}
.title-banner-text {
    font-family: var(--font-display);
    font-weight: 700;
    font-size: 1.3rem;
    color: var(--text-primary);
    letter-spacing: -0.02em;
    line-height: 1.3;
}

/* ── Action Item Row ── */
.action-item {
    display: flex;
    gap: 0.75rem;
    padding: 0.65rem 0;
    border-bottom: 1px solid var(--border-dim);
    align-items: flex-start;
    transition: background 0.15s;
}
.action-item:last-child { border-bottom: none; }
.action-item:hover { background: rgba(0,229,255,0.03); border-radius: 8px; }
.action-bullet {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--cyan);
    margin-top: 0.42rem;
    flex-shrink: 0;
    box-shadow: 0 0 6px var(--cyan-glow);
}
.action-text {
    font-size: 0.855rem;
    color: var(--text-secondary);
    line-height: 1.65;
    font-family: var(--font-body);
}

/* ── Pill Tags ── */
.pill {
    display: inline-flex;
    align-items: center;
    background: var(--bg-overlay);
    border: 1px solid var(--border-dim);
    color: var(--text-secondary);
    border-radius: 999px;
    padding: 0.3rem 0.9rem;
    font-size: 0.78rem;
    font-family: var(--font-body);
    margin: 0.2rem 0.2rem 0.2rem 0;
    transition: all 0.2s;
    cursor: default;
}
.pill:hover { border-color: var(--border-mid); color: var(--text-primary); }
.pill-cyan {
    background: var(--cyan-dim);
    border-color: rgba(0,229,255,0.25);
    color: var(--cyan);
}
.pill-cyan:hover { box-shadow: 0 0 16px rgba(0,229,255,0.15); }
.pill-purple {
    background: var(--purple-dim);
    border-color: rgba(124,111,247,0.25);
    color: #a79cfa;
}
.pill-pink {
    background: var(--pink-dim);
    border-color: rgba(244,113,181,0.25);
    color: var(--pink);
}
.pill-green {
    background: var(--green-dim);
    border-color: rgba(0,255,163,0.25);
    color: var(--green);
}
.pill-amber {
    background: var(--amber-dim);
    border-color: rgba(255,179,71,0.25);
    color: var(--amber);
}

/* ── Chat Bubbles ── */
.chat-wrap {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-height: 480px;
    overflow-y: auto;
    padding: 0.25rem 0.25rem 0.5rem;
    scroll-behavior: smooth;
}
.chat-row-user {
    display: flex;
    justify-content: flex-end;
}
.chat-row-bot {
    display: flex;
    justify-content: flex-start;
    gap: 0.6rem;
    align-items: flex-start;
}
.chat-avatar {
    width: 28px; height: 28px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--purple), var(--cyan));
    display: flex; align-items: center; justify-content: center;
    font-size: 0.65rem;
    flex-shrink: 0;
    margin-top: 0.1rem;
    box-shadow: 0 0 12px rgba(124,111,247,0.4);
}
.chat-bubble-user {
    background: linear-gradient(135deg, rgba(0,229,255,0.12), rgba(124,111,247,0.12));
    border: 1px solid rgba(0,229,255,0.2);
    border-radius: 16px 16px 4px 16px;
    padding: 0.75rem 1.1rem;
    max-width: 72%;
    font-family: var(--font-body);
    font-size: 0.865rem;
    color: var(--text-primary);
    line-height: 1.6;
    box-shadow: 0 2px 16px rgba(0,0,0,0.3);
}
.chat-bubble-bot {
    background: var(--bg-raised);
    border: 1px solid var(--border-dim);
    border-radius: 16px 16px 16px 4px;
    padding: 0.85rem 1.1rem;
    max-width: 78%;
    font-family: var(--font-body);
    font-size: 0.865rem;
    color: var(--text-secondary);
    line-height: 1.7;
    box-shadow: 0 2px 16px rgba(0,0,0,0.3);
}
.chat-meta {
    font-family: var(--font-mono);
    font-size: 0.58rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    opacity: 0.4;
    margin-bottom: 0.3rem;
}

/* ── Chat Input Row ── */
.chat-input-wrap {
    display: flex;
    gap: 0.5rem;
    align-items: center;
    margin-top: 0.75rem;
    padding: 0.75rem;
    background: var(--bg-raised);
    border: 1px solid var(--border-dim);
    border-radius: var(--radius-lg);
    transition: border-color 0.2s;
}
.chat-input-wrap:focus-within {
    border-color: rgba(0,229,255,0.3);
    box-shadow: 0 0 0 3px rgba(0,229,255,0.06);
}

/* ── Empty State ── */
.empty-state {
    text-align: center;
    padding: 3.5rem 2rem;
    border: 1px dashed rgba(99,130,255,0.15);
    border-radius: var(--radius-xl);
    background: rgba(99,130,255,0.02);
}
.empty-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    display: block;
    filter: drop-shadow(0 0 12px rgba(0,229,255,0.3));
}
.empty-title {
    font-family: var(--font-display);
    font-weight: 700;
    font-size: 1.1rem;
    color: var(--text-primary);
    margin-bottom: 0.4rem;
}
.empty-sub {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
}

/* ── Feature Cards (empty home) ── */
.feature-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-dim);
    border-radius: var(--radius-xl);
    padding: 2rem 1.5rem;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
    position: relative;
    overflow: hidden;
}
.feature-card::before {
    content: '';
    position: absolute;
    top: -80px; left: -80px;
    width: 200px; height: 200px;
    border-radius: 50%;
    opacity: 0;
    transition: opacity 0.4s, transform 0.4s;
    transform: scale(0.5);
}
.feature-card-cyan::before  { background: radial-gradient(circle, rgba(0,229,255,0.08), transparent 70%); }
.feature-card-purple::before{ background: radial-gradient(circle, rgba(124,111,247,0.08), transparent 70%); }
.feature-card-pink::before  { background: radial-gradient(circle, rgba(244,113,181,0.08), transparent 70%); }
.feature-card:hover::before { opacity: 1; transform: scale(1.5); }
.feature-card:hover {
    border-color: var(--border-mid);
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.4), 0 0 0 1px rgba(99,130,255,0.12);
}
.feature-icon {
    font-size: 2.2rem;
    margin-bottom: 0.9rem;
    display: block;
}
.feature-title {
    font-family: var(--font-display);
    font-weight: 700;
    font-size: 1rem;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
    letter-spacing: -0.01em;
}
.feature-desc {
    font-size: 0.82rem;
    color: var(--text-muted);
    line-height: 1.65;
}

/* ── Transcript Viewer ── */
.transcript-viewer {
    font-family: var(--font-mono);
    font-size: 0.8rem;
    line-height: 2.1;
    color: var(--text-secondary);
    max-height: 500px;
    overflow-y: auto;
    padding-right: 0.5rem;
}

/* ── Status Step ── */
.step-status {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.4rem 0;
    font-family: var(--font-mono);
    font-size: 0.76rem;
    letter-spacing: 0.06em;
    color: var(--text-secondary);
    animation: fadeInUp 0.3s ease forwards;
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Analytics Stat Card ── */
.stat-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-dim);
    border-radius: var(--radius-lg);
    padding: 1.25rem 1.5rem;
    position: relative;
    overflow: hidden;
    transition: all 0.2s;
}
.stat-card:hover {
    border-color: var(--border-mid);
    transform: translateY(-2px);
}
.stat-value {
    font-family: var(--font-display);
    font-weight: 800;
    font-size: 2rem;
    letter-spacing: -0.04em;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.stat-label {
    font-family: var(--font-mono);
    font-size: 0.64rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--text-muted);
}
.stat-glow {
    position: absolute;
    bottom: -20px; right: -20px;
    width: 80px; height: 80px;
    border-radius: 50%;
    opacity: 0.15;
    filter: blur(20px);
}

/* ── Glow Divider ── */
.glow-divider {
    height: 1px;
    background: linear-gradient(90deg,
        transparent,
        rgba(0,229,255,0.25) 30%,
        rgba(124,111,247,0.2) 70%,
        transparent);
    margin: 1.5rem 0;
}

/* ── Upload Zone ── */
.upload-zone {
    border: 2px dashed rgba(0,229,255,0.2);
    border-radius: var(--radius-xl);
    padding: 2rem 1.5rem;
    text-align: center;
    background: rgba(0,229,255,0.02);
    transition: all 0.3s;
    cursor: pointer;
    margin-bottom: 0.75rem;
}
.upload-zone:hover {
    border-color: rgba(0,229,255,0.45);
    background: rgba(0,229,255,0.04);
    box-shadow: 0 0 30px rgba(0,229,255,0.06);
}

</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════
def init_state():
    defaults = {
        "pipeline_result": None,
        "chat_history": [],
        "processing": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:

    # Brand
    st.markdown("""
    <div class="sb-brand">
        <div class="sb-logo">◈ Vox</div>
        <div class="sb-tagline">AI Video Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    # Input section
    st.markdown('<div class="sb-label">Source</div>', unsafe_allow_html=True)
    source = st.text_input(
        "source",
        placeholder="YouTube URL or /path/to/file.mp4",
        label_visibility="collapsed",
    )

    st.markdown('<div class="sb-label" style="margin-top:0.5rem;">Language</div>', unsafe_allow_html=True)
    language = st.selectbox(
        "language",
        options=["english", "hinglish"],
        label_visibility="collapsed",
    )

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

    # Run button
    st.markdown('<div class="run-btn">', unsafe_allow_html=True)
    run_btn = st.button("▶  Run Pipeline", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

    # Capabilities
    st.markdown('<div class="sb-label">Capabilities</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sb-info-grid">
        <div class="sb-info-item"><span>📼</span> YouTube & local video</div>
        <div class="sb-info-item"><span>🌐</span> English & Hinglish</div>
        <div class="sb-info-item"><span>📋</span> Smart summarization</div>
        <div class="sb-info-item"><span>🧠</span> RAG-powered chat</div>
        <div class="sb-info-item"><span>⚡</span> Instant extraction</div>
    </div>
    """, unsafe_allow_html=True)

    # Ready badge
    if st.session_state.pipeline_result:
        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="sb-status">
            <div class="sb-status-dot"></div>
            <div class="sb-status-text">Session active</div>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HERO HEADER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow">Meeting Intelligence Platform</div>
    <h1 class="hero-title">
        Understand every<br><span>conversation instantly</span>
    </h1>
    <p class="hero-sub">Transcribe · Summarize · Extract insights · Chat with your content</p>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PIPELINE RUNNER
# ═══════════════════════════════════════════════════════════════════════════════
def run_pipeline_ui(source: str, language: str):
    progress_bar = st.progress(0)
    status_box = st.empty()

    def step(msg, pct, icon="◆"):
        status_box.markdown(
            f'<div class="step-status"><span style="color:var(--cyan)">{icon}</span>'
            f'<span>{msg}</span></div>',
            unsafe_allow_html=True,
        )
        progress_bar.progress(pct)

    try:
        step("Processing audio chunks…",        10, "◈")
        chunks = process_input(source)

        step("Transcribing audio…",             25, "◎")
        transcript = transcribe_all(chunks, language=language)

        step("Generating title…",               43, "◇")
        title = generate_title(transcript)

        step("Summarizing content…",            55, "◈")
        summary = summarize(transcript)

        step("Extracting action items…",        67, "◆")
        action_items = extract_action_items(transcript)

        step("Extracting key decisions…",       77, "◈")
        decisions = extract_key_decisions(transcript)

        step("Extracting open questions…",      87, "◎")
        questions = extract_questions(transcript)

        step("Building RAG engine…",            95, "◇")
        rag_chain = build_rag_chain(transcript)

        step("Complete",                       100, "✦")

        progress_bar.empty()
        status_box.empty()

        return {
            "title":         title,
            "transcript":    transcript,
            "summary":       summary,
            "action_items":  action_items,
            "key_decisions": decisions,
            "open_questions":questions,
            "rag_chain":     rag_chain,
        }

    except Exception as e:
        progress_bar.empty()
        status_box.empty()
        st.error(f"Pipeline error: {e}")
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# TRIGGER PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════
if run_btn:
    if not source.strip():
        st.warning("⚠  Enter a YouTube URL or file path in the sidebar.")
    else:
        with st.spinner(""):
            result = run_pipeline_ui(source.strip(), language)
        if result:
            st.session_state.pipeline_result = result
            st.session_state.chat_history = []
            st.success("✦  Analysis complete — explore your results below.")


# ═══════════════════════════════════════════════════════════════════════════════
# RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.pipeline_result:
    result = st.session_state.pipeline_result

    # ── Title Banner ────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="title-banner">
        <div class="title-banner-label">Detected title</div>
        <div class="title-banner-text">{result['title']}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs ────────────────────────────────────────────────────────────────
    tab_results, tab_transcript, tab_analytics, tab_chat = st.tabs([
        "📊  Insights",
        "📜  Transcript",
        "📈  Analytics",
        "💬  Chat",
    ])

    # ── INSIGHTS TAB ────────────────────────────────────────────────────────
    with tab_results:
        col_left, col_right = st.columns([1.15, 1], gap="large")

        with col_left:
            # Summary
            st.markdown(f"""
            <div class="card card-cyan">
                <div class="card-label card-label-accent">◈ Summary</div>
                <div class="card-content">{result['summary']}</div>
            </div>
            """, unsafe_allow_html=True)

            # Action Items
            items = result['action_items']
            if isinstance(items, list):
                items_html = "".join(
                    f'<div class="action-item"><div class="action-bullet"></div>'
                    f'<div class="action-text">{item}</div></div>'
                    for item in items
                )
            else:
                items_html = f'<div class="card-content">{items}</div>'

            st.markdown(f"""
            <div class="card">
                <div class="card-label">◆ Action Items</div>
                {items_html}
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            # Key Decisions
            decisions = result['key_decisions']
            if isinstance(decisions, list):
                pills_html = "".join(
                    f'<span class="pill pill-purple">{d}</span>' for d in decisions
                )
            else:
                pills_html = f'<div class="card-content">{decisions}</div>'

            st.markdown(f"""
            <div class="card card-purple">
                <div class="card-label">◈ Key Decisions</div>
                <div style="margin-top:0.3rem;line-height:2">{pills_html}</div>
            </div>
            """, unsafe_allow_html=True)

            # Open Questions
            questions = result['open_questions']
            if isinstance(questions, list):
                q_html = "".join(
                    f'<span class="pill pill-green">{q}</span>' for q in questions
                )
            else:
                q_html = f'<div class="card-content">{questions}</div>'

            st.markdown(f"""
            <div class="card card-green">
                <div class="card-label">◎ Open Questions</div>
                <div style="margin-top:0.3rem;line-height:2">{q_html}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── TRANSCRIPT TAB ───────────────────────────────────────────────────────
    with tab_transcript:
        st.markdown(f"""
        <div class="card">
            <div class="card-label card-label-accent">◎ Full Transcript</div>
            <div class="transcript-viewer">{result['transcript']}</div>
        </div>
        """, unsafe_allow_html=True)

        col_dl, col_pad = st.columns([1, 3])
        with col_dl:
            st.download_button(
                label="⬇  Download .txt",
                data=result['transcript'],
                file_name="transcript.txt",
                mime="text/plain",
                use_container_width=True,
            )

    # ── ANALYTICS TAB ────────────────────────────────────────────────────────
    with tab_analytics:
        transcript_text = result['transcript']
        word_count      = len(transcript_text.split())
        char_count      = len(transcript_text)
        sent_count      = transcript_text.count('.') + transcript_text.count('?') + transcript_text.count('!')
        ai_count        = len(result['action_items']) if isinstance(result['action_items'], list) else 1
        kd_count        = len(result['key_decisions']) if isinstance(result['key_decisions'], list) else 1
        oq_count        = len(result['open_questions']) if isinstance(result['open_questions'], list) else 1
        est_minutes     = max(1, round(word_count / 130))

        c1, c2, c3, c4 = st.columns(4, gap="medium")

        def stat_card(col, value, label, color, icon):
            with col:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value" style="color:{color}">{value}</div>
                    <div class="stat-label">{label}</div>
                    <div class="stat-glow" style="background:{color}"></div>
                    <div style="position:absolute;top:1.1rem;right:1.25rem;
                                font-size:1.3rem;opacity:0.18">{icon}</div>
                </div>
                """, unsafe_allow_html=True)

        stat_card(c1, f"{word_count:,}",    "Words transcribed",  "var(--cyan)",   "◎")
        stat_card(c2, f"~{est_minutes}m",   "Est. meeting length","var(--purple)", "◈")
        stat_card(c3, f"{ai_count}",        "Action items",       "var(--green)",  "◆")
        stat_card(c4, f"{kd_count}",        "Key decisions",      "var(--pink)",   "✦")

        st.markdown('<div class="glow-divider" style="margin:1.5rem 0;"></div>', unsafe_allow_html=True)

        col_a, col_b = st.columns(2, gap="large")
        with col_a:
            st.markdown(f"""
            <div class="card">
                <div class="card-label">◈ Content Breakdown</div>
                <div style="display:grid;gap:0.8rem;margin-top:0.5rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span class="card-content">Sentences detected</span>
                        <span class="pill pill-cyan">{sent_count}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span class="card-content">Characters (raw)</span>
                        <span class="pill pill-purple">{char_count:,}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span class="card-content">Open questions</span>
                        <span class="pill pill-green">{oq_count}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span class="card-content">Avg words/sentence</span>
                        <span class="pill">{round(word_count/max(sent_count,1))}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_b:
            st.markdown(f"""
            <div class="card card-green">
                <div class="card-label">◆ Extraction Summary</div>
                <div style="margin-top:0.5rem;">
                    <div style="margin-bottom:0.85rem;">
                        <div style="font-family:var(--font-mono);font-size:0.68rem;
                                    letter-spacing:0.12em;text-transform:uppercase;
                                    color:var(--text-muted);margin-bottom:0.3rem;">
                            Actions identified
                        </div>
                        <div style="background:rgba(0,229,255,0.08);border-radius:999px;
                                    height:6px;overflow:hidden;">
                            <div style="width:{min(ai_count*10,100)}%;height:100%;
                                        background:linear-gradient(90deg,var(--cyan),var(--purple));
                                        border-radius:999px;"></div>
                        </div>
                    </div>
                    <div style="margin-bottom:0.85rem;">
                        <div style="font-family:var(--font-mono);font-size:0.68rem;
                                    letter-spacing:0.12em;text-transform:uppercase;
                                    color:var(--text-muted);margin-bottom:0.3rem;">
                            Decisions captured
                        </div>
                        <div style="background:rgba(124,111,247,0.08);border-radius:999px;
                                    height:6px;overflow:hidden;">
                            <div style="width:{min(kd_count*12,100)}%;height:100%;
                                        background:linear-gradient(90deg,var(--purple),var(--pink));
                                        border-radius:999px;"></div>
                        </div>
                    </div>
                    <div>
                        <div style="font-family:var(--font-mono);font-size:0.68rem;
                                    letter-spacing:0.12em;text-transform:uppercase;
                                    color:var(--text-muted);margin-bottom:0.3rem;">
                            Questions flagged
                        </div>
                        <div style="background:rgba(0,255,163,0.08);border-radius:999px;
                                    height:6px;overflow:hidden;">
                            <div style="width:{min(oq_count*14,100)}%;height:100%;
                                        background:linear-gradient(90deg,var(--green),var(--cyan));
                                        border-radius:999px;"></div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── CHAT TAB ─────────────────────────────────────────────────────────────
    with tab_chat:

        # Chat history
        if st.session_state.chat_history:
            chat_msgs = ""
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    chat_msgs += f"""
                    <div class="chat-row-user">
                        <div class="chat-bubble-user">
                            <div class="chat-meta" style="text-align:right;">You</div>
                            {msg['content']}
                        </div>
                    </div>"""
                else:
                    chat_msgs += f"""
                    <div class="chat-row-bot">
                        <div class="chat-avatar">◈</div>
                        <div class="chat-bubble-bot">
                            <div class="chat-meta">Vox AI</div>
                            {msg['content']}
                        </div>
                    </div>"""

            st.markdown(f'<div class="chat-wrap">{chat_msgs}</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="empty-state">
                <span class="empty-icon">💬</span>
                <div class="empty-title">Ask anything about your meeting</div>
                <div class="empty-sub">Powered by RAG — grounded in your transcript</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div style="height:0.75rem"></div>', unsafe_allow_html=True)

        # Input row
        col_input, col_send = st.columns([5, 1], gap="small")
        with col_input:
            user_question = st.text_input(
                "chat_input",
                placeholder="e.g. What were the main decisions made?",
                label_visibility="collapsed",
                key="chat_input",
            )
        with col_send:
            send = st.button("Send", use_container_width=True)

        # Suggested prompts
        if not st.session_state.chat_history:
            st.markdown('<div style="margin-top:0.5rem;display:flex;flex-wrap:wrap;gap:0.4rem;">', unsafe_allow_html=True)
            prompts = [
                "Summarize in 3 bullet points",
                "What were the action items?",
                "Who needs to do what?",
                "What decisions were made?",
            ]
            for p in prompts:
                st.markdown(f'<span class="pill pill-cyan" style="cursor:pointer;">{p}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if send and user_question.strip():
            q = user_question.strip()
            st.session_state.chat_history.append({"role": "user", "content": q})
            with st.spinner(""):
                answer = asked_question(result["rag_chain"], q)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# EMPTY HOME STATE
# ═══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3, gap="large")
    features = [
        ("🎙️", "Transcribe", "Supports YouTube links and local video/audio in English and Hinglish with high accuracy.", "feature-card-cyan"),
        ("📋", "Analyze",    "Auto-generates summaries, action items, key decisions, and open questions.", "feature-card-purple"),
        ("💬", "Chat",       "Ask follow-up questions via a RAG-powered conversational AI grounded in your content.", "feature-card-pink"),
    ]
    for col, (icon, title, desc, variant) in zip([col_a, col_b, col_c], features):
        with col:
            st.markdown(f"""
            <div class="feature-card {variant}">
                <span class="feature-icon">{icon}</span>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;margin-top:2.5rem;padding:1.5rem;">
        <div style="font-family:var(--font-mono);font-size:0.7rem;
                    letter-spacing:0.18em;text-transform:uppercase;
                    color:var(--text-muted);">
            ← Enter a source URL or file path in the sidebar to begin
        </div>
    </div>
    """, unsafe_allow_html=True)