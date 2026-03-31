import streamlit as st
import random
import pandas as pd
import time

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Leaders Network Circles | دوائر التواصل القيادي",
    page_icon="🔵",
    layout="wide",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0d0d2b; color: #ffffff; }

    /* Hide default Streamlit header */
    #MainMenu, header, footer { visibility: hidden; }

    /* Title area */
    .main-title {
        text-align: center;
        font-size: 2rem;
        font-weight: 700;
        color: #00e5ff;
        margin-bottom: 0.2rem;
        letter-spacing: 1px;
    }
    .sub-title {
        text-align: center;
        font-size: 1rem;
        color: #aaaacc;
        margin-bottom: 1.5rem;
    }

    /* Stat cards */
    .stat-card {
        background: linear-gradient(135deg, #1a1a4e, #12124a);
        border: 1px solid #3333aa;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }
    .stat-val { font-size: 2rem; font-weight: 700; color: #00e5ff; }
    .stat-lbl { font-size: 0.75rem; color: #aaaacc; margin-top: 2px; }

    /* Circle cards */
    .circle-card {
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 10px;
    }
    .impact-card  { background: linear-gradient(135deg, #0a2e1a, #0f4a28); border: 1px solid #1d9e75; }
    .connect-card { background: linear-gradient(135deg, #0a1a38, #0e2e60); border: 1px solid #185fa5; }
    .grow-card    { background: linear-gradient(135deg, #1a1040, #2a1a6e); border: 1px solid #7f77dd; }

    .circle-title {
        font-size: 1.1rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 12px;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .impact-title  { color: #00e5a0; }
    .connect-title { color: #00b4ff; }
    .grow-title    { color: #b39dff; }

    /* Table label */
    .table-label {
        font-size: 0.7rem;
        color: #aaaacc;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 6px;
        margin-top: 10px;
    }

    /* Participant chips */
    .chips-row { display: flex; gap: 8px; flex-wrap: wrap; padding-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.08); }
    .chips-row-last { border-bottom: none; }

    .chip {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 42px;
        height: 42px;
        border-radius: 50%;
        font-size: 14px;
        font-weight: 700;
        animation: popIn 0.4s ease both;
    }
    @keyframes popIn {
        0%   { transform: scale(0.3); opacity: 0; }
        60%  { transform: scale(1.15); }
        100% { transform: scale(1); opacity: 1; }
    }
    .chip-impact  { background: #0f4a28; color: #00e5a0; border: 2px solid #1d9e75; }
    .chip-connect { background: #0e2e60; color: #00b4ff; border: 2px solid #185fa5; }
    .chip-grow    { background: #2a1a6e; color: #b39dff; border: 2px solid #7f77dd; }
    .chip-highlight { box-shadow: 0 0 0 3px #ff4081, 0 0 12px #ff4081; }

    /* Round buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1a1a6e, #12124a) !important;
        color: #aaaacc !important;
        border: 1px solid #3333aa !important;
        border-radius: 20px !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #2a2a9e, #1a1a6e) !important;
        color: #00e5ff !important;
        border-color: #00e5ff !important;
    }

    /* Progress bar */
    .prog-grid { display: grid; grid-template-columns: repeat(10, 1fr); gap: 5px; margin-top: 10px; }
    .prog-cell {
        background: #1a1a4e;
        border: 1px solid #3333aa;
        border-radius: 6px;
        padding: 5px 2px;
        text-align: center;
        font-size: 11px;
    }
    .prog-num { font-size: 13px; font-weight: 700; }
    .prog-0  { color: #666688; }
    .prog-2  { color: #7f77dd; }
    .prog-4  { color: #185fa5; }
    .prog-8  { color: #00b4ff; }
    .prog-12 { color: #00e5a0; }

    /* Divider */
    hr { border-color: #2a2a6e; }

    /* Info box */
    .info-box {
        background: linear-gradient(135deg, #1a1a4e, #0d0d2b);
        border: 1px solid #3333aa;
        border-radius: 10px;
        padding: 12px 16px;
        text-align: center;
        color: #aaaacc;
        font-size: 0.85rem;
        margin-top: 12px;
    }

    /* Search input */
    .stNumberInput input {
        background: #1a1a4e !important;
        border: 1px solid #3333aa !important;
        border-radius: 20px !important;
        color: #ffffff !important;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# ─── Schedule Generation ─────────────────────────────────────────────────────

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
    rest = remaining[1:]

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
    people = list(range(1, 31))
    met_pairs = set()
    schedule = []

    # Round 1: base grouping
    base = [
        [1,2,3],[4,5,6],[7,8,9],[10,11,12],[13,14,15],
        [16,17,18],[19,20,21],[22,23,24],[25,26,27],[28,29,30]
    ]
    schedule.append([list(g) for g in base])
    for group in base:
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                met_pairs.add(pair_key(group[i], group[j]))

    # Rounds 2–6: backtracking
    for _ in range(5):
        remaining = list(people)
        random.shuffle(remaining)
        groups = []
        success = backtrack(remaining, groups, met_pairs)
        if not success or len(groups) != 10:
            # fallback shuffle
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
    with st.spinner("Generating optimized schedule..."):
        st.session_state.schedule = generate_schedule()

if "current_round" not in st.session_state:
    st.session_state.current_round = None

if "highlight" not in st.session_state:
    st.session_state.highlight = None

schedule = st.session_state.schedule

IMPACT_TABLES  = ["Table A", "Table B", "Table C"]
CONNECT_TABLES = ["Table A", "Table B", "Table C", "Table D"]
GROW_TABLES    = ["Table A", "Table B", "Table C"]


# ─── Helper: count unique meetings ───────────────────────────────────────────

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


# ─── Helper: render chips HTML ────────────────────────────────────────────────

def render_chips(groups, tables, chip_class, highlight):
    html = ""
    for i, group in enumerate(groups):
        is_last = (i == len(groups) - 1)
        html += f'<div class="table-label">{tables[i]}</div>'
        row_class = "chips-row-last" if is_last else ""
        html += f'<div class="chips-row {row_class}">'
        for num in group:
            hl = " chip-highlight" if highlight and num == highlight else ""
            html += f'<div class="chip {chip_class}{hl}">{num}</div>'
        html += '</div>'
    return html


# ─── Title ────────────────────────────────────────────────────────────────────

st.markdown('<div class="main-title">🔵 دوائر التواصل القيادي | Leaders Network Circles</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Saudi Leadership Society — AUS Chapter &nbsp;·&nbsp; 30 Participants · 6 Rounds · 10 min each</div>', unsafe_allow_html=True)

st.markdown("---")

# ─── Stats row ───────────────────────────────────────────────────────────────

r = st.session_state.current_round
unique_min = 0
if r is not None:
    unique_min, _ = count_unique_meetings(r)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<div class="stat-card"><div class="stat-val">30</div><div class="stat-lbl">Participants</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="stat-card"><div class="stat-val">6</div><div class="stat-lbl">Total Rounds</div></div>', unsafe_allow_html=True)
with c3:
    rnd_display = (r + 1) if r is not None else "—"
    st.markdown(f'<div class="stat-card"><div class="stat-val">{rnd_display}</div><div class="stat-lbl">Current Round</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="stat-card"><div class="stat-val">{unique_min}</div><div class="stat-lbl">Min Unique Meetings / Person</div></div>', unsafe_allow_html=True)

st.markdown("---")

# ─── Controls ────────────────────────────────────────────────────────────────

col_btns, col_search, col_regen = st.columns([5, 2, 1])

with col_btns:
    btn_cols = st.columns(6)
    for i in range(6):
        with btn_cols[i]:
            if st.button(f"Round {i+1}", key=f"round_{i}", use_container_width=True):
                st.session_state.current_round = i
                with st.spinner(f"Loading Round {i+1}..."):
                    time.sleep(0.3)
                st.rerun()

with col_search:
    highlight_num = st.number_input("🔍 Find participant #", min_value=1, max_value=30, value=None, placeholder="1–30", key="search")
    st.session_state.highlight = int(highlight_num) if highlight_num else None

with col_regen:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Reshuffle", use_container_width=True):
        del st.session_state["schedule"]
        st.session_state.current_round = None
        st.rerun()

st.markdown("---")

# ─── Main circles display ────────────────────────────────────────────────────

if st.session_state.current_round is None:
    st.markdown("""
    <div style="text-align:center; padding: 60px 0; color: #aaaacc; font-size: 1.1rem;">
        👆 Click a round button above to reveal the participant assignments
    </div>
    """, unsafe_allow_html=True)
else:
    r = st.session_state.current_round
    round_data = schedule[r]
    hl = st.session_state.highlight

    impact_groups  = round_data[0:3]
    connect_groups = round_data[3:7]
    grow_groups    = round_data[7:10]

    col_i, col_c, col_g = st.columns(3)

    # ── Impact ──
    with col_i:
        chips_html = render_chips(impact_groups, IMPACT_TABLES, "chip-impact", hl)
        st.markdown(f"""
        <div class="circle-card impact-card">
            <div class="circle-title impact-title">⬡ Impact Circle</div>
            {chips_html}
        </div>
        """, unsafe_allow_html=True)

    # ── Connect ──
    with col_c:
        chips_html = render_chips(connect_groups, CONNECT_TABLES, "chip-connect", hl)
        st.markdown(f"""
        <div class="circle-card connect-card">
            <div class="circle-title connect-title">⬡ Connect Circle</div>
            {chips_html}
        </div>
        """, unsafe_allow_html=True)

    # ── Grow ──
    with col_g:
        chips_html = render_chips(grow_groups, GROW_TABLES, "chip-grow", hl)
        st.markdown(f"""
        <div class="circle-card grow-card">
            <div class="circle-title grow-title">⬡ Grow Circle</div>
            {chips_html}
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="info-box">
        Round {r+1} of 6 &nbsp;·&nbsp; Impact: 3 tables × 3 people &nbsp;·&nbsp;
        Connect: 4 tables × 3 people &nbsp;·&nbsp; Grow: 3 tables × 3 people
    </div>
    """, unsafe_allow_html=True)

# ─── Full round summary table ─────────────────────────────────────────────────

if st.session_state.current_round is not None:
    st.markdown("---")
    with st.expander("📋 Full round summary table (printable)"):
        r = st.session_state.current_round
        round_data = schedule[r]

        rows = []
        circle_names = (
            ["Impact"] * 3 +
            ["Connect"] * 4 +
            ["Grow"] * 3
        )
        all_tables = IMPACT_TABLES + CONNECT_TABLES + GROW_TABLES

        for idx, group in enumerate(round_data):
            rows.append({
                "Circle": circle_names[idx],
                "Table": all_tables[idx],
                "P1": group[0],
                "P2": group[1],
                "P3": group[2],
            })

        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

# ─── Progress tracker ────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("**Unique meetings tracker** (per participant, up to current round)")

if st.session_state.current_round is not None:
    _, meetings = count_unique_meetings(st.session_state.current_round)
else:
    meetings = {i: set() for i in range(1, 31)}

cells = ""
for i in range(1, 31):
    count = len(meetings[i])
    if count == 0:
        cls = "prog-0"
    elif count < 4:
        cls = "prog-2"
    elif count < 8:
        cls = "prog-4"
    elif count < 12:
        cls = "prog-8"
    else:
        cls = "prog-12"
    cells += f'<div class="prog-cell"><div class="prog-num {cls}">{count}</div><div style="color:#666688;font-size:10px;">#{i}</div></div>'

st.markdown(f'<div class="prog-grid">{cells}</div>', unsafe_allow_html=True)

st.markdown("""
<div style="display:flex;gap:20px;margin-top:10px;font-size:12px;color:#aaaacc;flex-wrap:wrap;">
  <span>🟣 1–3 meetings</span>
  <span>🔵 4–7 meetings</span>
  <span>💙 8–11 meetings</span>
  <span>🟢 12 meetings (complete)</span>
</div>
""", unsafe_allow_html=True)

# ─── All rounds overview ──────────────────────────────────────────────────────

st.markdown("---")
with st.expander("📅 All 6 rounds overview"):
    tab_labels = [f"Round {i+1}" for i in range(6)]
    tabs = st.tabs(tab_labels)
    for r_idx, tab in enumerate(tabs):
        with tab:
            round_data = schedule[r_idx]
            circle_names = ["Impact"]*3 + ["Connect"]*4 + ["Grow"]*3
            all_tables   = IMPACT_TABLES + CONNECT_TABLES + GROW_TABLES
            rows = []
            for idx, group in enumerate(round_data):
                rows.append({
                    "Circle": circle_names[idx],
                    "Table": all_tables[idx],
                    "P1": group[0], "P2": group[1], "P3": group[2],
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
