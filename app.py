import streamlit as st
import random
import pandas as pd
import time

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Leaders Network Circles | دوائر التواصل القيادي",
    page_icon="🔵",
    layout="wide",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500;600&family=Tajawal:wght@400;500;700&display=swap');

/* ══ GLOBAL — override Streamlit defaults ══ */
.stApp { background-color: #f6f6f3 !important; }
.stApp, .stApp * { font-family: 'DM Sans', sans-serif !important; }

/* Force all text to dark so nothing disappears on white */
.stApp p, .stApp span, .stApp div, .stApp label, .stApp li,
.stApp h1, .stApp h2, .stApp h3,
.stApp .stMarkdown, .stApp .stMarkdown *,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] * { color: #12122a !important; }

/* Widget labels */
.stNumberInput label,
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] * {
    color: #12122a !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
}

/* Number input box */
.stNumberInput input {
    background-color: #ffffff !important;
    color: #12122a !important;
    border: 1px solid rgba(0,0,0,0.18) !important;
    border-radius: 20px !important;
    font-size: 0.85rem !important;
    text-align: center !important;
}
.stNumberInput input::placeholder { color: #9999bb !important; }

/* Expander headers */
.streamlit-expanderHeader,
.streamlit-expanderHeader *,
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary * { color: #12122a !important; font-weight: 600 !important; }

/* Tabs */
.stTabs [data-baseweb="tab"]       { color: #6b6b8a !important; }
.stTabs [aria-selected="true"]     { color: #12122a !important; font-weight: 600 !important; }

/* Dataframe */
.stDataFrame, .stDataFrame *       { color: #12122a !important; }

/* Hide chrome */
#MainMenu, header, footer { visibility: hidden; }

/* ══ PAGE HEADER ══ */
.page-header {
    background: #ffffff;
    border-bottom: 1px solid rgba(0,0,0,0.07);
    padding: 22px 0 16px;
    text-align: center;
}
.main-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 2rem; font-weight: 700;
    color: #12122a !important;
    margin-bottom: 2px; letter-spacing: 0.3px;
}
.main-title-ar {
    font-family: 'Tajawal', sans-serif !important;
    font-size: 1.05rem; direction: rtl;
    color: #6b6b8a !important; margin-bottom: 4px;
}
.sub-line { font-size: 0.76rem; color: #6b6b8a !important; letter-spacing: 0.5px; margin-bottom: 10px; }
.org-badges { display:flex; align-items:center; justify-content:center; gap:10px; flex-wrap:wrap; margin-top:8px; }
.org-badge {
    display:inline-flex; align-items:center; gap:6px;
    background:#f0f0ec; border:1px solid rgba(0,0,0,0.08);
    border-radius:20px; padding:4px 12px;
    font-size:0.68rem !important; font-weight:600 !important;
    color:#4a4a6a !important; text-transform:uppercase; letter-spacing:0.8px;
}
.org-dot { display:inline-block; width:7px; height:7px; border-radius:50%; flex-shrink:0; }
.aus-badge {
    background:#12122a; color:#ffffff !important;
    font-size:0.68rem !important; font-weight:700 !important;
    letter-spacing:1.5px; padding:4px 14px;
    border-radius:20px; text-transform:uppercase;
}
.event-badge {
    display:inline-flex; align-items:center; gap:6px;
    background:#fdf0da; border:1px solid rgba(184,112,15,0.25);
    border-radius:20px; padding:4px 12px;
    font-family:'Tajawal',sans-serif !important;
    font-size:0.72rem !important; font-weight:600 !important;
    color:#7a4800 !important;
}
.pulse-dot {
    display:inline-block; width:7px; height:7px;
    border-radius:50%; background:#B8700F;
    animation:pulse 2s infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* ══ STAT CARDS ══ */
.stat-card {
    background:#ffffff; border:1px solid rgba(0,0,0,0.07);
    border-radius:14px; padding:20px 10px; text-align:center;
    box-shadow:0 2px 12px rgba(0,0,0,0.04);
}
.stat-val {
    font-family:'Playfair Display',serif !important;
    font-size:2.1rem; font-weight:700;
    color:#12122a !important; line-height:1; display:block;
}
.stat-lbl {
    font-size:0.65rem; color:#6b6b8a !important;
    margin-top:5px; text-transform:uppercase; letter-spacing:1px; display:block;
}

/* ══ ROUND BUTTONS ══ */
.stButton > button {
    background:#ffffff !important;
    color:#4a4a6a !important;
    border:1px solid rgba(0,0,0,0.14) !important;
    border-radius:20px !important;
    font-weight:500 !important; font-size:0.8rem !important;
    transition:all 0.18s !important;
}
.stButton > button:hover {
    background:#12122a !important; color:#ffffff !important;
    border-color:#12122a !important;
}

/* Section labels */
.section-label {
    font-size:0.68rem; font-weight:700;
    color:#6b6b8a !important; text-transform:uppercase; letter-spacing:1.2px; margin-bottom:8px;
}
.section-title {
    font-family:'Playfair Display',serif !important;
    font-size:1rem; font-weight:700; color:#12122a !important;
}

/* ══ CIRCLE CARDS ══ */
.circle-card {
    border-radius:16px; background:#ffffff;
    border:1px solid rgba(0,0,0,0.07); overflow:hidden;
    box-shadow:0 4px 20px rgba(0,0,0,0.05);
    transition:box-shadow 0.2s, transform 0.2s; margin-bottom:8px;
}
.circle-card:hover { box-shadow:0 10px 36px rgba(0,0,0,0.10); transform:translateY(-3px); }

.ch-impact  { background:#dff4ec; border-bottom:1px solid rgba(29,158,117,0.2);  padding:22px 20px 16px; text-align:center; }
.ch-connect { background:#deeef9; border-bottom:1px solid rgba(24,95,165,0.2);   padding:22px 20px 16px; text-align:center; }
.ch-grow    { background:#eceafe; border-bottom:1px solid rgba(83,74,183,0.2);   padding:22px 20px 16px; text-align:center; }

.circle-logo { display:block; margin:0 auto 10px; }

.circle-name {
    font-family:'Playfair Display',serif !important;
    font-size:1.05rem; font-weight:700; margin-bottom:2px; display:block;
}
.circle-name-ar {
    font-family:'Tajawal',sans-serif !important;
    font-size:0.82rem; color:#6b6b8a !important;
    direction:rtl; display:block; margin-bottom:3px;
}
.circle-meta { font-size:0.68rem; color:#6b6b8a !important; text-transform:uppercase; letter-spacing:0.8px; display:block; }

.cn-impact  { color:#0e7a57 !important; }
.cn-connect { color:#0e4a82 !important; }
.cn-grow    { color:#3b3490 !important; }

.cpbar { height:3px; background:rgba(0,0,0,0.08); margin-top:12px; border-radius:2px; overflow:hidden; }
.cpf-i { height:100%; background:#1D9E75; border-radius:2px; }
.cpf-c { height:100%; background:#185FA5; border-radius:2px; }
.cpf-g { height:100%; background:#534AB7; border-radius:2px; }

.card-body { padding:14px 18px; }

/* Table labels inside card body */
.tbl-label {
    font-size:0.65rem; color:#8888aa !important;
    text-transform:uppercase; letter-spacing:1.3px; font-weight:700;
    margin-top:12px; margin-bottom:6px;
    display:flex; align-items:center; gap:6px;
}
.tbl-label::after { content:''; flex:1; height:1px; background:rgba(0,0,0,0.07); }

/* ══ CHIPS ══ */
.chips-row { display:flex; gap:7px; flex-wrap:wrap; padding-bottom:8px; }
.chip {
    display:inline-flex; align-items:center; justify-content:center;
    width:40px; height:40px; border-radius:50%;
    font-size:12px; font-weight:700;
    border:1.5px solid transparent; cursor:default;
    transition:transform 0.15s, box-shadow 0.15s;
    animation:popIn 0.35s ease both;
}
.chip:hover { transform:scale(1.2); }
@keyframes popIn {
    0%   { transform:scale(0.3); opacity:0; }
    60%  { transform:scale(1.15); }
    100% { transform:scale(1); opacity:1; }
}
.chip-impact  { background:#dff4ec; color:#0e7a57 !important; border-color:#5DCAA5; }
.chip-connect { background:#deeef9; color:#0e4a82 !important; border-color:#85B7EB; }
.chip-grow    { background:#eceafe; color:#3b3490 !important; border-color:#AFA9EC; }
.chip-highlight {
    box-shadow:0 0 0 3px #B8700F, 0 4px 16px rgba(184,112,15,0.35) !important;
    transform:scale(1.25) !important;
    background:#fdf0da !important; color:#7a4800 !important; border-color:#B8700F !important;
}

/* ══ INFO BAR ══ */
.info-box {
    background:#ffffff; border:1px solid rgba(0,0,0,0.07);
    border-radius:10px; padding:10px 18px; margin-top:12px;
    display:flex; align-items:center; justify-content:center;
    gap:14px; flex-wrap:wrap; font-size:0.78rem; color:#6b6b8a !important;
}
.info-dot { display:inline-block; width:6px; height:6px; border-radius:50%; margin-right:4px; }
.info-sep { display:inline-block; width:1px; height:12px; background:rgba(0,0,0,0.1); }

/* ══ EMPTY STATE ══ */
.empty-state { text-align:center; padding:60px 0; }
.empty-title { font-family:'Playfair Display',serif !important; font-size:1.2rem; color:#12122a !important; margin-bottom:6px; }
.empty-sub   { font-size:0.85rem; color:#6b6b8a !important; }

/* ══ PROGRESS GRID ══ */
.prog-grid { display:grid; grid-template-columns:repeat(10,1fr); gap:5px; margin-top:8px; }
.prog-cell {
    background:#ffffff; border:1px solid rgba(0,0,0,0.07);
    border-radius:8px; padding:6px 3px; text-align:center; transition:transform 0.15s;
}
.prog-cell:hover { transform:translateY(-2px); }
.prog-num { font-size:13px; font-weight:700; display:block; }
.prog-id  { font-size:9px; color:#9999bb !important; margin-top:1px; display:block; }
.p0  { color:#cccccc !important; }
.p1  { color:#534AB7 !important; }
.p4  { color:#185FA5 !important; }
.p8  { color:#1D9E75 !important; }
.p12 { color:#B8700F !important; }

/* ══ LEGEND ══ */
.legend-row { display:flex; gap:16px; flex-wrap:wrap; margin-top:10px; }
.leg { display:flex; align-items:center; gap:5px; font-size:0.75rem; color:#6b6b8a !important; }
.leg-dot { width:8px; height:8px; border-radius:50%; }

hr { border-color:rgba(0,0,0,0.07) !important; }
</style>
""", unsafe_allow_html=True)


# ─── Circle SVG Logos ─────────────────────────────────────────────────────────

IMPACT_LOGO = """<svg width="72" height="72" viewBox="0 0 72 72" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="36" cy="36" r="31" stroke="#1D9E75" stroke-width="1.5" stroke-dasharray="5 3.5" opacity="0.35"/>
  <circle cx="36" cy="36" r="22" stroke="#1D9E75" stroke-width="1.8" opacity="0.6"/>
  <circle cx="36" cy="36" r="13" stroke="#1D9E75" stroke-width="2.2" opacity="0.85"/>
  <line x1="36" y1="5"  x2="36" y2="13" stroke="#1D9E75" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="36" y1="59" x2="36" y2="67" stroke="#1D9E75" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="5"  y1="36" x2="13" y2="36" stroke="#1D9E75" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="59" y1="36" x2="67" y2="36" stroke="#1D9E75" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="36" cy="36" r="5.5" fill="#1D9E75"/>
  <circle cx="36" cy="36" r="2.5" fill="white"/>
</svg>"""

CONNECT_LOGO = """<svg width="72" height="72" viewBox="0 0 72 72" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="36" cy="36" r="30" stroke="#185FA5" stroke-width="1.5" stroke-dasharray="4 3" opacity="0.25"/>
  <circle cx="36" cy="36" r="8.5" fill="#185FA5"/>
  <circle cx="36" cy="36" r="4"   fill="white"/>
  <circle cx="36" cy="9"  r="5.5" stroke="#185FA5" stroke-width="2" fill="#deeef9"/>
  <circle cx="60" cy="23" r="5.5" stroke="#185FA5" stroke-width="2" fill="#deeef9"/>
  <circle cx="52" cy="57" r="5.5" stroke="#185FA5" stroke-width="2" fill="#deeef9"/>
  <circle cx="20" cy="57" r="5.5" stroke="#185FA5" stroke-width="2" fill="#deeef9"/>
  <circle cx="12" cy="23" r="5.5" stroke="#185FA5" stroke-width="2" fill="#deeef9"/>
  <line x1="36"   y1="14.5" x2="36"   y2="27.5" stroke="#185FA5" stroke-width="1.5"/>
  <line x1="55.5" y1="25.5" x2="44"   y2="31"   stroke="#185FA5" stroke-width="1.5"/>
  <line x1="48"   y1="52"   x2="42"   y2="43.5" stroke="#185FA5" stroke-width="1.5"/>
  <line x1="24"   y1="52"   x2="30"   y2="43.5" stroke="#185FA5" stroke-width="1.5"/>
  <line x1="17.5" y1="25.5" x2="29"   y2="31"   stroke="#185FA5" stroke-width="1.5"/>
  <path d="M40 9.5 Q54 9 57.5 21"   stroke="#185FA5" stroke-width="1" opacity="0.3" fill="none"/>
  <path d="M57 29 Q61 45 53.5 52.5" stroke="#185FA5" stroke-width="1" opacity="0.3" fill="none"/>
  <path d="M48 60 Q36 66 24 60"     stroke="#185FA5" stroke-width="1" opacity="0.3" fill="none"/>
  <path d="M18.5 52.5 Q11 45 15 29" stroke="#185FA5" stroke-width="1" opacity="0.3" fill="none"/>
  <path d="M14.5 21 Q18 7 32 9.5"   stroke="#185FA5" stroke-width="1" opacity="0.3" fill="none"/>
</svg>"""

GROW_LOGO = """<svg width="72" height="72" viewBox="0 0 72 72" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="36" cy="36" r="30" stroke="#534AB7" stroke-width="1.5" stroke-dasharray="5 4" opacity="0.2"/>
  <line x1="11" y1="54" x2="61" y2="54" stroke="#534AB7" stroke-width="1" opacity="0.15"/>
  <line x1="11" y1="44" x2="61" y2="44" stroke="#534AB7" stroke-width="1" opacity="0.12"/>
  <line x1="11" y1="34" x2="61" y2="34" stroke="#534AB7" stroke-width="1" opacity="0.10"/>
  <polygon points="11,54 22,41 33,47 45,28 61,13 61,54" fill="#534AB7" opacity="0.08"/>
  <polyline points="11,54 22,41 33,47 45,28 61,13"
            stroke="#534AB7" stroke-width="3"
            stroke-linejoin="round" stroke-linecap="round" fill="none"/>
  <circle cx="11" cy="54" r="3.5" fill="#534AB7"/>
  <circle cx="22" cy="41" r="3.5" fill="#534AB7" opacity="0.7"/>
  <circle cx="33" cy="47" r="3.5" fill="#534AB7" opacity="0.7"/>
  <circle cx="45" cy="28" r="4"   fill="#534AB7"/>
  <circle cx="61" cy="13" r="5"   fill="#534AB7"/>
  <polygon points="56,9 66,9 66,19" fill="#534AB7"/>
</svg>"""


# ─── Schedule Generation ──────────────────────────────────────────────────────

def pair_key(a, b):
    return (min(a, b), max(a, b))

def group_conflicts(group, met_pairs):
    for i in range(len(group)):
        for j in range(i + 1, len(group)):
            if pair_key(group[i], group[j]) in met_pairs:
                return True
    return False

def backtrack(remaining, groups, met_pairs):
    if len(remaining) == 0:
        return True
    if len(remaining) % 3 != 0:
        return False
    first = remaining[0]
    rest  = remaining[1:]
    for i in range(len(rest) - 1):
        for j in range(i + 1, len(rest)):
            g = [first, rest[i], rest[j]]
            if not group_conflicts(g, met_pairs):
                new_pairs = []
                for a in range(len(g)):
                    for b in range(a + 1, len(g)):
                        k = pair_key(g[a], g[b])
                        if k not in met_pairs:
                            met_pairs.add(k)
                            new_pairs.append(k)
                groups.append(g)
                new_remaining = [x for idx, x in enumerate(rest) if idx != i and idx != j]
                if backtrack(new_remaining, groups, met_pairs):
                    return True
                groups.pop()
                for k in new_pairs:
                    met_pairs.discard(k)
    return False

def generate_schedule():
    people    = list(range(1, 31))
    met_pairs = set()
    schedule  = []
    base = [
        [1,2,3],[4,5,6],[7,8,9],[10,11,12],[13,14,15],
        [16,17,18],[19,20,21],[22,23,24],[25,26,27],[28,29,30]
    ]
    schedule.append([list(g) for g in base])
    for group in base:
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                met_pairs.add(pair_key(group[i], group[j]))
    for _ in range(5):
        remaining = list(people)
        random.shuffle(remaining)
        groups  = []
        success = backtrack(remaining, groups, met_pairs)
        if not success or len(groups) != 10:
            shuffled = list(people)
            random.shuffle(shuffled)
            groups = [shuffled[i*3:(i+1)*3] for i in range(10)]
        schedule.append([list(g) for g in groups])
        for group in groups:
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    met_pairs.add(pair_key(group[i], group[j]))
    return schedule


# ─── Session state ────────────────────────────────────────────────────────────

if "schedule" not in st.session_state:
    with st.spinner("Generating optimised schedule…"):
        st.session_state.schedule = generate_schedule()

if "current_round" not in st.session_state:
    st.session_state.current_round = None

if "highlight" not in st.session_state:
    st.session_state.highlight = None

schedule = st.session_state.schedule

IMPACT_TABLES  = ["Table A", "Table B", "Table C"]
CONNECT_TABLES = ["Table A", "Table B", "Table C", "Table D"]
GROW_TABLES    = ["Table A", "Table B", "Table C"]


# ─── Helpers ─────────────────────────────────────────────────────────────────

def count_unique_meetings(up_to_round):
    meetings = {i: set() for i in range(1, 31)}
    for r in range(up_to_round + 1):
        for group in schedule[r]:
            for p in group:
                for q in group:
                    if p != q:
                        meetings[p].add(q)
    counts = [len(v) for v in meetings.values()]
    return min(counts), meetings

def render_chips(groups, tables, chip_class, highlight):
    html = ""
    for i, group in enumerate(groups):
        html += f'<div class="tbl-label">{tables[i]}</div>'
        html += '<div class="chips-row">'
        for num in group:
            hl = " chip-highlight" if highlight and num == highlight else ""
            html += f'<div class="chip {chip_class}{hl}">{num}</div>'
        html += '</div>'
    return html

# ── FIX: on_change callback makes highlight update immediately on input ──
def on_search_change():
    val = st.session_state.search_input
    st.session_state.highlight = int(val) if val else None


# ─── Page Header ─────────────────────────────────────────────────────────────

st.markdown("""
<div class="page-header">
  <div class="main-title">Leaders Network Circles</div>
  <div class="main-title-ar">دوائر التواصل القيادي</div>
  <div class="sub-line">Saudi Leadership Society · AUS Chapter · 30 Participants · 6 Rounds · 10 min each</div>
  <div class="org-badges">
    <span class="org-badge"><span class="org-dot" style="background:#1D9E75;"></span>Misk Foundation</span>
    <span class="org-badge"><span class="org-dot" style="background:#185FA5;"></span>Saudi Leadership Society</span>
    <span class="aus-badge">AUS Chapter</span>
    <span class="event-badge"><span class="pulse-dot"></span>اللقاء الأول · القطاع الصحي</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ─── Stats row ───────────────────────────────────────────────────────────────

r          = st.session_state.current_round
unique_min = 0
if r is not None:
    unique_min, _ = count_unique_meetings(r)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<div class="stat-card"><span class="stat-val">30</span><span class="stat-lbl">Participants</span></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="stat-card"><span class="stat-val">6</span><span class="stat-lbl">Total Rounds</span></div>', unsafe_allow_html=True)
with c3:
    rnd_display = (r + 1) if r is not None else "—"
    st.markdown(f'<div class="stat-card"><span class="stat-val">{rnd_display}</span><span class="stat-lbl">Current Round</span></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="stat-card"><span class="stat-val">{unique_min}</span><span class="stat-lbl">Min Unique Meetings</span></div>', unsafe_allow_html=True)

st.markdown("---")

# ─── Controls ────────────────────────────────────────────────────────────────

col_btns, col_search, col_regen = st.columns([5, 2, 1])

with col_btns:
    st.markdown('<div class="section-label">Select Round</div>', unsafe_allow_html=True)
    btn_cols = st.columns(6)
    for i in range(6):
        with btn_cols[i]:
            if st.button(f"Round {i+1}", key=f"round_{i}", use_container_width=True):
                st.session_state.current_round = i
                st.rerun()

with col_search:
    # KEY FIX: on_change triggers st.session_state.highlight update + automatic rerun
    st.number_input(
        "🔍 Find Participant (1–30)",
        min_value=1,
        max_value=30,
        value=None,
        placeholder="Enter number…",
        key="search_input",
        on_change=on_search_change,
    )

with col_regen:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("↺ Reshuffle", use_container_width=True):
        del st.session_state["schedule"]
        st.session_state.current_round = None
        st.session_state.highlight     = None
        st.rerun()

st.markdown("---")

# ─── Main circles display ────────────────────────────────────────────────────

if st.session_state.current_round is None:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-title">Select a Round to Begin</div>
        <div class="empty-sub">Click any round button above to reveal participant assignments</div>
    </div>
    """, unsafe_allow_html=True)
else:
    r          = st.session_state.current_round
    round_data = schedule[r]
    hl         = st.session_state.highlight

    impact_groups  = round_data[0:3]
    connect_groups = round_data[3:7]
    grow_groups    = round_data[7:10]

    col_i, col_c, col_g = st.columns(3)

    # ── Impact ──
    with col_i:
        chips = render_chips(impact_groups, IMPACT_TABLES, "chip-impact", hl)
        st.markdown(f"""
        <div class="circle-card">
          <div class="ch-impact">
            {IMPACT_LOGO}
            <span class="circle-name cn-impact">Impact Circle</span>
            <span class="circle-name-ar">دائرة الأثر</span>
            <span class="circle-meta">3 tables · 3 people each</span>
            <div class="cpbar"><div class="cpf-i" style="width:30%;"></div></div>
          </div>
          <div class="card-body">{chips}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Connect ──
    with col_c:
        chips = render_chips(connect_groups, CONNECT_TABLES, "chip-connect", hl)
        st.markdown(f"""
        <div class="circle-card">
          <div class="ch-connect">
            {CONNECT_LOGO}
            <span class="circle-name cn-connect">Connect Circle</span>
            <span class="circle-name-ar">دائرة التواصل</span>
            <span class="circle-meta">4 tables · 3 people each</span>
            <div class="cpbar"><div class="cpf-c" style="width:40%;"></div></div>
          </div>
          <div class="card-body">{chips}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Grow ──
    with col_g:
        chips = render_chips(grow_groups, GROW_TABLES, "chip-grow", hl)
        st.markdown(f"""
        <div class="circle-card">
          <div class="ch-grow">
            {GROW_LOGO}
            <span class="circle-name cn-grow">Grow Circle</span>
            <span class="circle-name-ar">دائرة النمو</span>
            <span class="circle-meta">3 tables · 3 people each</span>
            <div class="cpbar"><div class="cpf-g" style="width:30%;"></div></div>
          </div>
          <div class="card-body">{chips}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="info-box">
      <span><span class="info-dot" style="background:#1D9E75;"></span>Impact: 3 × 3</span>
      <span class="info-sep"></span>
      <span><span class="info-dot" style="background:#185FA5;"></span>Connect: 4 × 3</span>
      <span class="info-sep"></span>
      <span><span class="info-dot" style="background:#534AB7;"></span>Grow: 3 × 3</span>
      <span class="info-sep"></span>
      <span>Round {r+1} of 6 &nbsp;·&nbsp; 10 min per round</span>
    </div>
    """, unsafe_allow_html=True)

# ─── Full round summary table ─────────────────────────────────────────────────

if st.session_state.current_round is not None:
    st.markdown("---")
    with st.expander("📋 Full round summary table"):
        r          = st.session_state.current_round
        round_data = schedule[r]
        rows       = []
        circle_names = ["Impact"]*3 + ["Connect"]*4 + ["Grow"]*3
        all_tables   = IMPACT_TABLES + CONNECT_TABLES + GROW_TABLES
        for idx, group in enumerate(round_data):
            rows.append({
                "Circle": circle_names[idx],
                "Table":  all_tables[idx],
                "P1": group[0], "P2": group[1], "P3": group[2],
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ─── Progress tracker ────────────────────────────────────────────────────────

st.markdown("---")
st.markdown('<div class="section-title">Unique Meetings Tracker</div>', unsafe_allow_html=True)
st.markdown('<div style="font-size:0.76rem;color:#6b6b8a;margin-bottom:6px;">Per participant — cumulative up to current round</div>', unsafe_allow_html=True)

if st.session_state.current_round is not None:
    _, meetings = count_unique_meetings(st.session_state.current_round)
else:
    meetings = {i: set() for i in range(1, 31)}

cells = ""
for i in range(1, 31):
    count = len(meetings[i])
    cls   = "p0"
    if   count >= 12: cls = "p12"
    elif count >= 8:  cls = "p8"
    elif count >= 4:  cls = "p4"
    elif count >= 1:  cls = "p1"
    cells += (
        f'<div class="prog-cell">'
        f'<span class="prog-num {cls}">{count}</span>'
        f'<span class="prog-id">#{i}</span>'
        f'</div>'
    )

st.markdown(f'<div class="prog-grid">{cells}</div>', unsafe_allow_html=True)

st.markdown("""
<div class="legend-row">
  <div class="leg"><div class="leg-dot" style="background:#cccccc;"></div>0 meetings</div>
  <div class="leg"><div class="leg-dot" style="background:#534AB7;"></div>1–3</div>
  <div class="leg"><div class="leg-dot" style="background:#185FA5;"></div>4–7</div>
  <div class="leg"><div class="leg-dot" style="background:#1D9E75;"></div>8–11</div>
  <div class="leg"><div class="leg-dot" style="background:#B8700F;"></div>12 complete</div>
</div>
""", unsafe_allow_html=True)

# ─── All rounds overview ──────────────────────────────────────────────────────

st.markdown("---")
with st.expander("📅 All 6 rounds overview"):
    tabs = st.tabs([f"Round {i+1}" for i in range(6)])
    for r_idx, tab in enumerate(tabs):
        with tab:
            round_data   = schedule[r_idx]
            circle_names = ["Impact"]*3 + ["Connect"]*4 + ["Grow"]*3
            all_tables   = IMPACT_TABLES + CONNECT_TABLES + GROW_TABLES
            rows = []
            for idx, group in enumerate(round_data):
                rows.append({
                    "Circle": circle_names[idx],
                    "Table":  all_tables[idx],
                    "P1": group[0], "P2": group[1], "P3": group[2],
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
