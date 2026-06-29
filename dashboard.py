"""
HCIL Service Performance Intelligence Dashboard — Dealer Composite Ranking Engine
Honda Car India Limited ·
Run: python -m streamlit run dashboard_final.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="HCIL Service Performance Intelligence Dashboard — Dealer Rankings",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── COLOUR PALETTE ─────────────────────────────────────────────
# Professional base
NAVY   = "#1A1A2E"
WHITE  = "#FFFFFF"
BG     = "#F5F6FA"
CARD   = "#FFFFFF"
BORDER = "#DDE3EE"
TEXT1  = "#1A1A2E"
TEXT2  = "#4A5568"
TEXT3  = "#8896A8"

# VIBGYOR accents — used only for data encoding
VIOLET = "#6A0DAD"
INDIGO = "#3949AB"
BLUE   = "#1565C0"
GREEN  = "#2E7D32"
YELLOW = "#F9A825"
ORANGE = "#E65100"
RED    = "#C62828"

ZONE_COLORS = {
    "North": INDIGO,
    "South": GREEN,
    "West":  ORANGE,
    "East":  VIOLET,
}

st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    background: {BG};
  }}

  /* TOP BAR */
  .topbar {{
    background: {NAVY};
    margin: -1rem -1rem 0 -1rem;
    padding: 0 2.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 64px;
    border-bottom: 3px solid {BLUE};
  }}
  .tb-left    {{ display:flex; align-items:center; gap:16px; }}
  .tb-logo    {{ background:{BLUE}; color:white; font-size:12px; font-weight:700;
                 padding:7px 13px; letter-spacing:1.5px; border-radius:3px; }}
  .tb-title   {{ color:white; font-size:16px; font-weight:600; }}
  .tb-divider {{ color:#3A4A6A; font-size:20px; }}
  .tb-sub     {{ color:#6B84B0; font-size:12px; font-weight:400; }}
  .tb-right   {{ color:#5A7090; font-size:11px; letter-spacing:.8px; }}

  /* SECTION LABELS */
  .sec-label {{
    font-size:11px; font-weight:700; color:{TEXT3};
    text-transform:uppercase; letter-spacing:1.5px;
    margin: 2.5rem 0 1.2rem;
    padding-bottom: 8px;
    border-bottom: 1px solid {BORDER};
  }}

  /* KPI SUMMARY CARDS */
  .kpi-row {{
    display:grid;
    grid-template-columns: repeat(5,1fr);
    gap:16px;
    margin: 1.2rem 0 2rem;
  }}
  .kpi-card {{
    background:{CARD};
    border:1px solid {BORDER};
    padding: 24px 22px;
    border-radius: 6px;
    border-top: 3px solid {BLUE};
  }}
  .kpi-card.alert   {{ border-top-color:{RED}; }}
  .kpi-card.neutral {{ border-top-color:{BORDER}; }}
  .kpi-label {{
    font-size:10px; font-weight:700; color:{TEXT3};
    text-transform:uppercase; letter-spacing:1px;
    margin-bottom:12px;
  }}
  .kpi-val  {{ font-size:28px; font-weight:700; color:{TEXT1}; line-height:1; }}
  .kpi-note {{ font-size:11px; color:{TEXT3}; margin-top:8px; }}

  /* MAIN TABLE */
  .dtable {{ width:100%; border-collapse:collapse; }}
  .dtable thead tr {{
    background:{NAVY}; color:white;
    font-size:10px; font-weight:700;
    text-transform:uppercase; letter-spacing:1px;
  }}
  .dtable thead th {{ padding:14px 18px; text-align:left; white-space:nowrap; }}
  .dtable tbody tr {{
    border-bottom:1px solid {BORDER}; background:{CARD};
  }}
  .dtable tbody tr:hover {{ background:#EEF2FB; }}
  .dtable tbody td {{
    padding:15px 18px; font-size:12px;
    color:{TEXT1}; vertical-align:middle;
  }}
  .dtable tbody tr.row-top    {{ background:#F0F7F1; }}
  .dtable tbody tr.row-bottom {{ background:#FDF2F2; }}

  /* RANK BADGE */
  .rank-badge {{
    display:inline-flex; align-items:center; justify-content:center;
    width:30px; height:30px; border-radius:50%;
    font-size:11px; font-weight:700;
  }}
  .rb-gold {{ background:{YELLOW}; color:#5A3A00; }}
  .rb-top  {{ background:{BLUE}; color:white; }}
  .rb-mid  {{ background:{BORDER}; color:{TEXT2}; }}
  .rb-bot  {{ background:#FDECEA; color:{RED}; }}

  /* SCORE BAR */
  .score-wrap  {{ display:flex; align-items:center; gap:12px; }}
  .score-track {{ flex:1; height:8px; background:{BORDER}; border-radius:4px; overflow:hidden; }}
  .score-fill  {{ height:8px; border-radius:4px; }}
  .score-num   {{ font-size:13px; font-weight:600; color:{TEXT1}; width:38px; text-align:right; }}

  /* MINI BAR */
  .mini-wrap  {{ display:flex; align-items:center; gap:8px; }}
  .mini-track {{ width:56px; height:5px; background:{BORDER}; border-radius:3px; overflow:hidden; }}
  .mini-fill  {{ height:5px; border-radius:3px; }}
  .mini-val   {{ font-size:11px; color:{TEXT2}; min-width:42px; }}

  /* ZONE PILL */
  .zone-pill {{
    display:inline-block; font-size:10px; font-weight:700;
    padding:4px 11px; border-radius:20px; letter-spacing:.4px;
  }}
  .z-north {{ background:#E8EDF8; color:{INDIGO}; }}
  .z-south {{ background:#E8F5E9; color:{GREEN}; }}
  .z-west  {{ background:#FBE9E7; color:{ORANGE}; }}
  .z-east  {{ background:#F3E5F5; color:{VIOLET}; }}

  /* INTERVENTION CARDS */
  .int-card {{
    background:{CARD}; border:1px solid {BORDER};
    border-top:3px solid {RED}; border-radius:6px;
    padding:20px 16px;
  }}

  /* ACTION BOARD CARDS */
  .action-card {{
    background:{CARD}; border:1px solid {BORDER};
    border-left:5px solid {RED};
    border-radius:0 6px 6px 0;
    padding:22px 24px; margin-bottom:14px;
  }}
  .action-card.moderate {{ border-left-color:{YELLOW}; }}
  .action-card.watch    {{ border-left-color:{GREEN}; }}

  .priority-pill {{
    display:inline-block; font-size:9px; font-weight:700;
    padding:3px 11px; border-radius:20px;
    text-transform:uppercase; letter-spacing:.7px;
    margin-bottom:12px;
  }}
  .pp-critical {{ background:#FDECEA; color:{RED}; }}
  .pp-moderate {{ background:#FFF8E1; color:#7A5000; }}
  .pp-watch    {{ background:#E8F5E9; color:{GREEN}; }}

  .action-suggestion {{
    display:flex; align-items:flex-start; gap:14px;
    background:{BG}; border:1px solid {BORDER};
    border-radius:5px; padding:12px 16px; margin-top:12px;
  }}
  .action-label {{
    font-size:9px; font-weight:700; color:{BLUE};
    text-transform:uppercase; letter-spacing:.9px;
    white-space:nowrap; padding-top:2px;
  }}
  .action-text {{ font-size:12px; color:{TEXT2}; line-height:1.65; }}

  /* AI SUMMARY */
  .ai-summary {{
    background:{NAVY}; border-radius:8px;
    padding:26px 32px; margin: 2.5rem 0 1.5rem;
    border-left:5px solid {BLUE};
  }}
  .ai-tag {{
    font-size:9px; font-weight:700; color:{BLUE};
    text-transform:uppercase; letter-spacing:1.4px;
    margin-bottom:12px;
  }}
  .ai-text {{
    font-size:13px; color:#C8D4E8; line-height:1.85;
  }}
  .ai-text b {{ color:white; }}

  /* FOOTER */
  .footer {{
    background:{NAVY}; color:#4A6090; font-size:10px;
    text-align:center; padding:16px;
    margin: 2rem -1rem -1rem; letter-spacing:.5px;
  }}

  /* MISC */
  #MainMenu, footer, header {{ visibility:hidden; }}
  .block-container {{ padding:0 1.5rem 1rem; }}

  /* TABS */
  .stTabs [data-baseweb="tab-list"] {{
    gap:4px; border-bottom:2px solid {BORDER}; padding-bottom:0;
    margin-top:1.2rem;
  }}
  .stTabs [data-baseweb="tab"] {{
    font-size:12px; font-weight:600; color:{TEXT2};
    padding:12px 22px; border-radius:4px 4px 0 0;
    border:1px solid transparent; border-bottom:none;
    letter-spacing:.3px;
  }}
  .stTabs [aria-selected="true"] {{
    background:{CARD}; color:{BLUE};
    border-color:{BORDER}; border-bottom-color:{CARD};
  }}
</style>

<div class="topbar">
  <div class="tb-left">
    <div class="tb-logo">HCIL</div>
    <div class="tb-title">Service Performance Intelligence Dashboard</div>
    <div class="tb-divider">|</div>
    <div class="tb-sub">Dealer Composite Ranking Engine</div>
  </div>
  <div class="tb-right">FY 2024–25 &nbsp;·&nbsp; IT / SYSTEMS &nbsp;·&nbsp; </div>
</div>
""", unsafe_allow_html=True)

# ── DATA ───────────────────────────────────────────────────────
# ✅ FIXED (correct path)
@st.cache_data
def load():
    return pd.read_csv("dealer_performance.csv")

df = load()

# ── SIDEBAR ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='font-size:13px;font-weight:700;color:{TEXT1};
                margin-bottom:18px;padding-bottom:10px;border-bottom:1px solid {BORDER};'>
      Dashboard Filters
    </div>""", unsafe_allow_html=True)

    zone_sel    = st.multiselect("Zone", ["North","South","East","West"],
                                 default=["North","South","East","West"])
    score_range = st.slider("Minimum Composite Score", 70, 100, 75)
    show_n      = st.radio("Dealer View",
                           ["All dealers", "Top 10 only", "Bottom 10 only"], index=0)

    st.markdown(f"""
    <div style='margin-top:24px;padding:16px;background:{BG};
                border:1px solid {BORDER};border-radius:6px;'>
      <div style='font-size:10px;font-weight:700;color:{TEXT3};
                  text-transform:uppercase;letter-spacing:1px;margin-bottom:12px;'>
        Score Composition
      </div>
      <div style='font-size:12px;color:{TEXT2};line-height:2.2;'>
        SR Achievement &nbsp;&nbsp;&nbsp; <b style='color:{TEXT1};'>25%</b><br>
        PM Achievement &nbsp;&nbsp;&nbsp; <b style='color:{TEXT1};'>20%</b><br>
        RSA Achievement &nbsp;&nbsp; <b style='color:{TEXT1};'>20%</b><br>
        EW Penetration &nbsp;&nbsp;&nbsp;&nbsp; <b style='color:{TEXT1};'>20%</b><br>
        ATW Achievement &nbsp;&nbsp; <b style='color:{TEXT1};'>15%</b>
      </div>
    </div>""", unsafe_allow_html=True)

# ── FILTER ─────────────────────────────────────────────────────
fdf = df[df.zone.isin(zone_sel) & (df.composite_score >= score_range)].copy()
if show_n == "Top 10 only":      fdf = fdf.head(10)
elif show_n == "Bottom 10 only": fdf = fdf.tail(10)

# ── HELPERS ────────────────────────────────────────────────────
def zone_pill(z):
    cls = {"North":"z-north","South":"z-south","West":"z-west","East":"z-east"}.get(z,"z-north")
    return f'<span class="zone-pill {cls}">{z}</span>'

def rank_badge(r, total):
    if r == 1:          cls = "rb-gold"
    elif r <= 3:        cls = "rb-top"
    elif r > total - 3: cls = "rb-bot"
    else:               cls = "rb-mid"
    return f'<span class="rank-badge {cls}">{r}</span>'

def score_bar(val):
    pct   = min(val, 100)
    color = BLUE if pct >= 85 else (YELLOW if pct >= 78 else RED)
    return (f'<div class="score-wrap">'
            f'<div class="score-track">'
            f'<div class="score-fill" style="width:{pct:.0f}%;background:{color};"></div>'
            f'</div><div class="score-num">{val:.1f}</div></div>')

def mini_bar(val, maxval):
    pct   = min(val / maxval * 100, 100)
    color = GREEN if pct >= 85 else (YELLOW if pct >= 70 else RED)
    return (f'<div class="mini-wrap">'
            f'<div class="mini-track">'
            f'<div class="mini-fill" style="width:{pct:.0f}%;background:{color};"></div>'
            f'</div><div class="mini-val">{val:.0f}%</div></div>')

def get_weakest_key(row):
    scores = {
        "SR":  row.sr_achievement  / 110,
        "PM":  row.pm_achievement  / 110,
        "EW":  row.ew_penetration  / 70,
        "ATW": row.atw_achievement / 110,
    }
    return min(scores, key=scores.get)

def weakest_html(row):
    w = get_weakest_key(row)
    return f'<span style="color:{RED};font-weight:700;font-size:11px;">↓ {w}</span>'

KPI_META = {
    "SR":  ("sr_achievement",  110, "SR Achievement",  95.0),
    "PM":  ("pm_achievement",  110, "PM Achievement",  93.0),
    "EW":  ("ew_penetration",   70, "EW Penetration",  58.0),
    "ATW": ("atw_achievement", 110, "ATW Achievement", 88.0),
}

ACTIONS = {
    "SR":  "Schedule SR activation camp; review top rejection reasons with the service manager.",
    "PM":  "Enrol service advisors in PM upsell training; track PM conversion rate weekly.",
    "EW":  "Mandate EW pitch at vehicle delivery; integrate EW checklist into PDI sheet.",
    "ATW": "Audit ATW adoption on DMS; retrain service leads on ATW benefits and process.",
}

THRESHOLDS = {
    "SR":  {"critical": 85, "moderate": 92},
    "PM":  {"critical": 83, "moderate": 90},
    "EW":  {"critical": 50, "moderate": 56},
    "ATW": {"critical": 78, "moderate": 85},
}

def get_priority(kpi, val):
    t = THRESHOLDS[kpi]
    if val < t["critical"]:   return "Critical"
    elif val < t["moderate"]: return "Moderate"
    return "Watch"

# ── TABS ───────────────────────────────────────────────────────
tab1, tab2 = st.tabs([
    "  📊  Dealer Composite Ranking  ",
    "  🔴  KPI Action Board  ",
])

# ════════════════════════════════════════════════════════════════
# TAB 1 — DEALER COMPOSITE RANKING
# ════════════════════════════════════════════════════════════════
with tab1:

    top_d      = fdf.iloc[0] if len(fdf) else df.iloc[0]
    best_zone  = fdf.groupby("zone").composite_score.mean().idxmax() if len(fdf) else "—"
    need_int   = len(fdf[fdf.composite_score < 82])

    # ── SNAPSHOT KPI CARDS ──
    st.markdown('<div class="sec-label">All-India Snapshot — FY 2024-25</div>',
                unsafe_allow_html=True)
    st.markdown(f"""
    <div class="kpi-row">
      <div class="kpi-card">
        <div class="kpi-label">Dealers Ranked</div>
        <div class="kpi-val">{len(fdf)}</div>
        <div class="kpi-note">of {len(df)} total dealers</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Avg Composite Score</div>
        <div class="kpi-val">{fdf.composite_score.mean():.1f}</div>
        <div class="kpi-note">out of 100 points</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Top Performer</div>
        <div class="kpi-val" style="font-size:17px;padding-top:4px;">{top_d.dealer_name}</div>
        <div class="kpi-note">{top_d.city} &nbsp;·&nbsp; Score {top_d.composite_score}</div>
      </div>
      <div class="kpi-card alert">
        <div class="kpi-label">Needs Intervention</div>
        <div class="kpi-val" style="color:{RED};">{need_int}</div>
        <div class="kpi-note">composite score below 82</div>
      </div>
      <div class="kpi-card neutral">
        <div class="kpi-label">Best Zone</div>
        <div class="kpi-val" style="font-size:20px;padding-top:6px;">{best_zone}</div>
        <div class="kpi-note">highest avg composite score</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── RANKING TABLE ──
    st.markdown('<div class="sec-label">Dealer Composite Ranking</div>',
                unsafe_allow_html=True)
    total     = len(df)
    rows_html = ""
    for _, row in fdf.iterrows():
        r      = int(row["rank"])
        tr_cls = "row-top" if r <= 5 else ("row-bottom" if r > total - 5 else "")
        rows_html += f"""
        <tr class="{tr_cls}">
          <td style="width:48px;">{rank_badge(r, total)}</td>
          <td>
            <div style="font-size:13px;font-weight:600;line-height:1.3;">
              {row.dealer_name}
            </div>
            <div style="font-size:10px;color:{TEXT3};margin-top:3px;">
              {row.city} &nbsp;·&nbsp; {row.state} &nbsp;·&nbsp; {row.dealer_code}
            </div>
          </td>
          <td>{zone_pill(row.zone)}</td>
          <td style="min-width:180px;">{score_bar(row.composite_score)}</td>
          <td>{mini_bar(row.sr_achievement, 110)}</td>
          <td>{mini_bar(row.pm_achievement, 110)}</td>
          <td>{mini_bar(row.ew_penetration, 70)}</td>
          <td>{mini_bar(row.atw_achievement, 110)}</td>
          <td>{weakest_html(row)}</td>
        </tr>"""

    st.markdown(f"""
    <div style="overflow-x:auto;border:1px solid {BORDER};border-radius:6px;
                overflow:hidden;margin-bottom:8px;">
    <table class="dtable">
      <thead><tr>
        <th>#</th>
        <th>Dealer</th>
        <th>Zone</th>
        <th>Composite Score</th>
        <th>SR Ach %</th>
        <th>PM Ach %</th>
        <th>EW Pen %</th>
        <th>ATW Ach %</th>
        <th>Weakest KPI</th>
      </tr></thead>
      <tbody>{rows_html}</tbody>
    </table>
    </div>
    <div style="font-size:10px;color:{TEXT3};padding-left:2px;margin-bottom:1rem;">
      Green rows = Top 5 &nbsp;·&nbsp; Red-tinted rows = Bottom 5 &nbsp;·&nbsp;
      Composite Score = SR×25% + PM×20% + RSA×20% + EW×20% + ATW×15%
    </div>""", unsafe_allow_html=True)

    # ── CHARTS ──
    st.markdown('<div class="sec-label">Performance Distribution</div>',
                unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")

    with c1:
        zone_avg = (df.groupby("zone")["composite_score"]
                    .mean().sort_values(ascending=False).reset_index())
        fig1 = go.Figure()
        fig1.add_bar(
            x=zone_avg.zone,
            y=zone_avg.composite_score,
            marker_color=[ZONE_COLORS.get(z, BLUE) for z in zone_avg.zone],
            text=zone_avg.composite_score.round(1),
            textposition="outside",
            textfont=dict(size=12, color=TEXT1)
        )
        fig1.add_hline(
            y=df.composite_score.mean(), line_dash="dot",
            line_color=TEXT3, line_width=1.5,
            annotation_text=f"All-India Avg  {df.composite_score.mean():.1f}",
            annotation_font_size=10, annotation_font_color=TEXT3
        )
        fig1.update_layout(
            title=dict(text="Average Composite Score by Zone",
                       font=dict(size=13, color=TEXT1), x=0),
            height=310, plot_bgcolor=CARD, paper_bgcolor=CARD,
            yaxis=dict(gridcolor=BORDER, range=[75, 96],
                       tickfont=dict(size=10, color=TEXT3)),
            xaxis=dict(tickfont=dict(size=12, color=TEXT1), showgrid=False),
            showlegend=False,
            margin=dict(t=45, b=15, l=15, r=15)
        )
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        kpi_labels = ["SR Ach%", "PM Ach%", "EW Pen%", "ATW Ach%"]
        kpi_fields = ["sr_achievement", "pm_achievement", "ew_penetration", "atw_achievement"]
        benchmarks = [95.0, 93.0, 58.0, 88.0]
        fig2 = go.Figure()
        for zone in ["North", "South", "West", "East"]:
            zdf  = df[df.zone == zone]
            vals = [round(zdf[f].mean(), 1) for f in kpi_fields]
            fig2.add_trace(go.Bar(
                name=zone,
                x=kpi_labels,
                y=vals,
                marker_color=ZONE_COLORS[zone],
                text=[f"{v:.1f}%" for v in vals],
                textposition="outside",
                textfont=dict(size=9, color=TEXT1),
            ))
        # Benchmark line per KPI group
        for i, bench in enumerate(benchmarks):
            fig2.add_shape(
                type="line",
                x0=i - 0.45, x1=i + 0.45,
                y0=bench, y1=bench,
                line=dict(color=RED, width=1.5, dash="dot"),
            )
        fig2.update_layout(
            title=dict(text="Zone KPI Comparison — All KPIs",
                       font=dict(size=13, color=TEXT1), x=0),
            barmode="group",
            height=310, plot_bgcolor=CARD, paper_bgcolor=CARD,
            yaxis=dict(gridcolor=BORDER, range=[40, 115],
                       tickfont=dict(size=10, color=TEXT3),
                       title=dict(text="Achievement %", font=dict(size=10, color=TEXT3))),
            xaxis=dict(tickfont=dict(size=11, color=TEXT1), showgrid=False),
            showlegend=True,
            legend=dict(orientation="h", y=-0.22,
                        font=dict(size=10, color=TEXT2)),
            margin=dict(t=45, b=55, l=15, r=15),
            bargap=0.25,
            bargroupgap=0.05,
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown(
            f"<div style='font-size:10px;color:{TEXT3};margin-top:-12px;padding-left:2px;'>"
            f"<span style='color:{RED};font-weight:700;'>— — —</span>"
            f"&nbsp; Dotted red line = benchmark target per KPI</div>",
            unsafe_allow_html=True
        )

    # ── INTERVENTION CARDS ──
    st.markdown('<div class="sec-label">Dealers Requiring Immediate Intervention</div>',
                unsafe_allow_html=True)
    bottom5  = df.nsmallest(5, "composite_score").sort_values("composite_score")
    kpi_disp = {
        "sr_achievement":  "SR Achievement",
        "pm_achievement":  "PM Achievement",
        "ew_penetration":  "EW Penetration",
        "atw_achievement": "ATW Achievement",
    }
    cols = st.columns(5, gap="medium")
    for i, (_, row) in enumerate(bottom5.iterrows()):
        scores = {
            "sr_achievement":  row.sr_achievement  / 110,
            "pm_achievement":  row.pm_achievement  / 110,
            "ew_penetration":  row.ew_penetration  / 70,
            "atw_achievement": row.atw_achievement / 110,
        }
        wk = min(scores, key=scores.get)
        with cols[i]:
            st.markdown(f"""
            <div class="int-card">
              <div style="font-size:10px;font-weight:700;color:{RED};
                          text-transform:uppercase;letter-spacing:.8px;margin-bottom:10px;">
                Rank #{int(row["rank"])}
              </div>
              <div style="font-size:13px;font-weight:600;color:{TEXT1};
                          line-height:1.35;margin-bottom:4px;">{row.dealer_name}</div>
              <div style="font-size:10px;color:{TEXT3};margin-bottom:16px;">
                {row.city} &nbsp;·&nbsp; {row.zone}
              </div>
              <div style="font-size:10px;color:{TEXT2};margin-bottom:4px;">
                Composite Score
              </div>
              <div style="font-size:24px;font-weight:700;color:{RED};
                          margin-bottom:14px;">{row.composite_score:.1f}</div>
              <div style="font-size:10px;color:{TEXT3};margin-bottom:4px;">Weakest KPI</div>
              <div style="font-size:11px;font-weight:700;color:{RED};">
                {kpi_disp[wk]}<br>
                <span style="font-size:15px;">{row[wk]:.1f}%</span>
              </div>
            </div>""", unsafe_allow_html=True)

    # ── AI INSIGHT SUMMARY ──
    south_avg  = df[df.zone == "South"].composite_score.mean()
    east_avg   = df[df.zone == "East"].composite_score.mean()
    zone_gap   = south_avg - east_avg
    ew_below   = len(df[df.ew_penetration < 55])
    crit_count = len(df[df.composite_score < 82])
    top_dealer = df.iloc[0].dealer_name
    top_city   = df.iloc[0].city
    top_score  = df.iloc[0].composite_score

    st.markdown(f"""
    <div class="ai-summary">
      <div class="ai-tag">⬡ &nbsp; AI Insight Summary</div>
      <div class="ai-text">
        <b>{top_dealer} ({top_city})</b> leads the dealer network with a composite score of
        <b>{top_score:.1f}</b>, while <b>{crit_count} dealer(s)</b> fall below the 82-point
        intervention threshold — indicating concentrated service risk in the lower tier that
        warrants immediate field-support deployment.
        The <b>South–East performance gap of {zone_gap:.1f} points</b> is the most significant
        regional disparity in the network; a structured knowledge-transfer programme modelled
        on South zone practices could close this gap within two quarters.
        Additionally, <b>{ew_below} dealers</b> are operating below 55% EW penetration,
        representing measurable unrealised revenue that can be recovered through mandatory
        EW pitch protocols and targeted sales coaching at delivery.
      </div>
    </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# TAB 2 — KPI ACTION BOARD
# ════════════════════════════════════════════════════════════════
with tab2:

    st.markdown('<div class="sec-label">KPI Action Board — Lowest Performing KPI per Dealer</div>',
                unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:12px;color:{TEXT2};margin-bottom:1.8rem;line-height:1.75;
                max-width:860px;">
    </div>""", unsafe_allow_html=True)

    # ── FILTERS ──
    fc1, fc2, fc3 = st.columns([2, 2, 2], gap="medium")
    with fc1:
        ab_zone = st.multiselect("Zone", ["North","South","East","West"],
                                 default=["North","South","East","West"], key="ab_zone")
    with fc2:
        ab_kpi  = st.multiselect("Focus KPI", ["SR","PM","EW","ATW"],
                                 default=["SR","PM","EW","ATW"], key="ab_kpi")
    with fc3:
        ab_pri  = st.multiselect("Priority Level", ["Critical","Moderate","Watch"],
                                 default=["Critical","Moderate"], key="ab_pri")

    # ── BUILD ACTION TABLE ──
    action_rows = []
    for _, row in df.iterrows():
        wk_key  = get_weakest_key(row)
        field   = KPI_META[wk_key][0]
        bench   = KPI_META[wk_key][3]
        wk_val  = row[field]
        gap     = bench - wk_val
        pri     = get_priority(wk_key, wk_val)
        action_rows.append({
            "rank":        int(row["rank"]),
            "dealer_name": row.dealer_name,
            "city":        row.city,
            "zone":        row.zone,
            "dealer_code": row.dealer_code,
            "composite":   row.composite_score,
            "weakest_kpi": wk_key,
            "kpi_value":   wk_val,
            "benchmark":   bench,
            "gap":         gap,
            "priority":    pri,
            "action":      ACTIONS[wk_key],
        })

    adf       = pd.DataFrame(action_rows)
    pri_order = {"Critical": 0, "Moderate": 1, "Watch": 2}
    adf_f     = (adf[adf.zone.isin(ab_zone) &
                     adf.weakest_kpi.isin(ab_kpi) &
                     adf.priority.isin(ab_pri)]
                 .sort_values(["priority", "composite"],
                              key=lambda x: x.map(pri_order) if x.name == "priority" else x)
                 .reset_index(drop=True))

    n_crit = len(adf_f[adf_f.priority == "Critical"])
    n_mod  = len(adf_f[adf_f.priority == "Moderate"])
    n_wat  = len(adf_f[adf_f.priority == "Watch"])

    # ── SUMMARY CHIPS ──
    st.markdown(f"""
    <div style="display:flex;gap:16px;margin-bottom:2rem;flex-wrap:wrap;">
      <div style="background:#FDECEA;border:1px solid #F5C6C2;border-radius:6px;
                  padding:16px 26px;text-align:center;min-width:110px;">
        <div style="font-size:30px;font-weight:700;color:{RED};">{n_crit}</div>
        <div style="font-size:10px;color:{RED};font-weight:700;
                    text-transform:uppercase;letter-spacing:.7px;margin-top:4px;">Critical</div>
      </div>
      <div style="background:#FFF8E1;border:1px solid #F5DEB3;border-radius:6px;
                  padding:16px 26px;text-align:center;min-width:110px;">
        <div style="font-size:30px;font-weight:700;color:{YELLOW};">{n_mod}</div>
        <div style="font-size:10px;color:#7A5000;font-weight:700;
                    text-transform:uppercase;letter-spacing:.7px;margin-top:4px;">Moderate</div>
      </div>
      <div style="background:#E8F5E9;border:1px solid #B7DFBF;border-radius:6px;
                  padding:16px 26px;text-align:center;min-width:110px;">
        <div style="font-size:30px;font-weight:700;color:{GREEN};">{n_wat}</div>
        <div style="font-size:10px;color:{GREEN};font-weight:700;
                    text-transform:uppercase;letter-spacing:.7px;margin-top:4px;">Watch</div>
      </div>
      <div style="background:{CARD};border:1px solid {BORDER};border-radius:6px;
                  padding:16px 26px;text-align:center;min-width:110px;">
        <div style="font-size:30px;font-weight:700;color:{TEXT1};">{n_crit+n_mod+n_wat}</div>
        <div style="font-size:10px;color:{TEXT3};font-weight:700;
                    text-transform:uppercase;letter-spacing:.7px;margin-top:4px;">Total Shown</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── KPI FREQUENCY CHART ──
    kpi_freq = adf_f.weakest_kpi.value_counts().reindex(["SR","PM","EW","ATW"], fill_value=0)
    kpi_clrs = {"SR": RED, "PM": ORANGE, "EW": VIOLET, "ATW": BLUE}
    fig_kpi  = go.Figure()
    fig_kpi.add_bar(
        x=kpi_freq.index,
        y=kpi_freq.values,
        marker_color=[kpi_clrs.get(k, BLUE) for k in kpi_freq.index],
        text=kpi_freq.values,
        textposition="outside",
        textfont=dict(size=12, color=TEXT1)
    )
    fig_kpi.update_layout(
        title=dict(text="Most Common Weakest KPI Across Dealers",
                   font=dict(size=13, color=TEXT1), x=0),
        height=250, plot_bgcolor=CARD, paper_bgcolor=CARD,
        yaxis=dict(gridcolor=BORDER, tickfont=dict(size=10, color=TEXT3)),
        xaxis=dict(tickfont=dict(size=12, color=TEXT1), showgrid=False),
        showlegend=False,
        margin=dict(t=45, b=15, l=15, r=15)
    )
    st.plotly_chart(fig_kpi, use_container_width=True)

    # ── ACTION CARDS ──
    st.markdown('<div class="sec-label">Dealer Action Cards</div>', unsafe_allow_html=True)

    pri_colors = {"Critical": RED, "Moderate": YELLOW, "Watch": GREEN}
    pri_cls    = {"Critical": "pp-critical", "Moderate": "pp-moderate", "Watch": "pp-watch"}
    card_cls   = {
        "Critical": "action-card",
        "Moderate": "action-card moderate",
        "Watch":    "action-card watch",
    }

    if adf_f.empty:
        st.info("No dealers match the current filter combination. Adjust the filters above.")
    else:
        for _, row in adf_f.iterrows():
            gap_sign  = "▼" if row.gap > 0 else "▲"
            gap_color = RED if row.gap > 0 else GREEN
            st.markdown(f"""
            <div class="{card_cls[row.priority]}">
              <div style="display:flex;justify-content:space-between;
                          align-items:flex-start;gap:24px;">
                <div style="flex:1;">
                  <span class="priority-pill {pri_cls[row.priority]}">{row.priority}</span>
                  <div style="font-size:14px;font-weight:700;color:{TEXT1};margin-bottom:5px;">
                    {row.dealer_name}
                    <span style="font-size:11px;font-weight:400;color:{TEXT3};margin-left:12px;">
                      {row.city} &nbsp;·&nbsp; {row.dealer_code}
                    </span>
                  </div>
                  <div style="margin-top:5px;">
                    {zone_pill(row.zone)}
                    <span style="font-size:11px;color:{TEXT3};margin-left:12px;">
                      Composite Score:
                      <b style="color:{TEXT1};">{row.composite:.1f}</b>
                    </span>
                  </div>
                </div>
                <div style="text-align:right;min-width:160px;flex-shrink:0;">
                  <div style="font-size:10px;color:{TEXT3};margin-bottom:3px;">
                    Weakest KPI
                  </div>
                  <div style="font-size:26px;font-weight:700;
                              color:{pri_colors[row.priority]};line-height:1.1;">
                    {row.weakest_kpi}
                  </div>
                  <div style="font-size:11px;color:{TEXT2};margin-top:5px;">
                    Value: <b>{row.kpi_value:.1f}%</b>
                    &nbsp;&nbsp;
                    <span style="color:{gap_color};font-weight:600;">
                      {gap_sign} {abs(row.gap):.1f} pp vs benchmark ({row.benchmark}%)
                    </span>
                  </div>
                </div>
              </div>
              <div class="action-suggestion">
                <div class="action-label">Suggested Action</div>
                <div class="action-text">{row.action}</div>
              </div>
            </div>""", unsafe_allow_html=True)

    # ── DOWNLOAD ──
    st.markdown("<div style='margin-top:1.8rem;'></div>", unsafe_allow_html=True)
    csv_out = adf_f[[
        "rank","dealer_name","city","zone","weakest_kpi",
        "kpi_value","benchmark","gap","priority","action"
    ]].copy()
    csv_out.columns = [
        "Rank","Dealer","City","Zone","Weakest KPI",
        "KPI Value %","Benchmark %","Gap (pp)","Priority","Suggested Action"
    ]
    st.download_button(
        label="⬇  Export Action List as CSV",
        data=csv_out.to_csv(index=False),
        file_name="kpi_action_board.csv",
        mime="text/csv"
    )

    # ── AI INSIGHT SUMMARY (Tab 2) ──
    dom_kpi   = kpi_freq.idxmax() if kpi_freq.sum() > 0 else "—"
    dom_count = int(kpi_freq.max())
    st.markdown(f"""
    <div class="ai-summary">
      <div class="ai-tag">⬡ &nbsp; AI Insight Summary</div>
      <div class="ai-text">
        Of the <b>{len(adf_f)} dealers</b> in the current view, <b>{n_crit} are at Critical
        priority</b> — requiring immediate field intervention to prevent further KPI erosion.
        <b>{dom_kpi}</b> is the most frequently flagged weakest KPI across <b>{dom_count}
        dealer(s)</b>, indicating a <b>network-wide training gap</b> in that area rather than
        isolated outlet-level issues. Moderate and Watch tier dealers should be enrolled in
        preventive coaching programmes now to avoid sliding into the Critical band before the
        next review cycle.
      </div>
    </div>""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  HCIL Service Performance Intelligence Dashboard &nbsp;·&nbsp; Honda Car India Limited &nbsp;t·&nbsp; FY 2024–25
</div>""", unsafe_allow_html=True)
