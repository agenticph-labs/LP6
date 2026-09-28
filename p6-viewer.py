"""
p6-viewer.py — Minimal Streamlit viewer for the P6 Research-to-Decision study.

Provides non-technical stakeholders with access to:
- Executive summary and recommendation
- Key visualizations
- CSV data explorers
- Full decision report

Usage:  streamlit run p6-viewer.py
"""

import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Paths ──────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
REPORT_PATH = ROOT / "market-entry-report.md"
NOTEBOOK_PATH = ROOT / "market-entry-analysis.ipynb"

st.set_page_config(
    page_title="P6: PH Coffee Market Entry Study",
    page_icon="☕",
    layout="wide",
)

st.title("☕ Philippine Specialty Coffee Market Entry Study")
st.markdown("**Research-to-Decision Analysis** — *Should a company enter the PH specialty coffee market?*")

# ── Load report ────────────────────────────────────────────────────────────
if REPORT_PATH.exists():
    report_text = REPORT_PATH.read_text()
    with st.expander("📄 View Full Decision Report", expanded=False):
        st.markdown(report_text)

# ── Key finding banner ─────────────────────────────────────────────────────
st.subheader("🏆 Recommendation")
st.success(
    "**Conditional GO** — Weighted score 74.7/100. "
    "Enter via phased strategy: 3 pilot stores in Metro Manila CBDs "
    "(BGC, Makati, Ortigas), validate unit economics over 12 months, "
    "then scale regionally with a capital-light franchise model."
)

# ── Visualizations ─────────────────────────────────────────────────────────
st.subheader("📊 Analysis Visualizations")

viz_cols = st.columns(3)
viz_files = [
    ("market-sizing.png", "Market Sizing"),
    ("competitor-map.png", "Competitor Map"),
    ("customer-segments.png", "Customer Segments"),
    ("pricing-benchmark.png", "Pricing Benchmark"),
    ("mcda-scoring.png", "MCDA Scoring"),
    ("risk-heatmap.png", "Risk Heatmap"),
    ("macro-context.png", "Macro Context"),
    ("unit-economics.png", "Unit Economics"),
]

for i, (fname, label) in enumerate(viz_files):
    fpath = ROOT / fname
    if fpath.exists():
        col = viz_cols[i % 3]
        with col:
            st.image(str(fpath), caption=label, use_container_width=True)

# ── CSV data explorers ─────────────────────────────────────────────────────
st.subheader("📁 Data Explorer")

csv_files = sorted(DATA_DIR.glob("*.csv"))
if csv_files:
    selected = st.selectbox("Select dataset to explore", [f.name for f in csv_files])
    df = pd.read_csv(DATA_DIR / selected)
    st.dataframe(df, use_container_width=True)

    with st.expander("📊 Summary Statistics"):
        st.dataframe(df.describe(include="all"), use_container_width=True)

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if len(numeric_cols) >= 1:
        chart_col = st.selectbox("Column to chart", numeric_cols)
        fig = px.bar(df, x=df.columns[0], y=chart_col, title=f"{chart_col} by {df.columns[0]}")
        st.plotly_chart(fig, use_container_width=True)

# ── Methodology overview ───────────────────────────────────────────────────
with st.expander("🧠 Methodology Overview"):
    st.markdown("""
This study follows a structured **research-to-decision framework**:

1. **Research Question Framing** — PICO / PESTEL lens
2. **Data Collection** — Government stats (PSA, BSP), industry reports
3. **Market Sizing** — Top-down + bottom-up triangulation
4. **Competitor Analysis** — Porter's Five Forces + strategic group mapping
5. **Pricing Analysis** — Income elasticity + competitive benchmarking
6. **Customer Segments** — Urban professionals, Gen Z, B2B, tourists
7. **Risk Assessment** — Regulatory, supply chain, competitive, macroeconomic
8. **Recommendation** — Multi-criteria decision analysis (MCDA)
    """)

# ── Footer ─────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption(
    "Portfolio Project 6 — AgenticPH Labs | "
    "Managed by the Hermes Agent System · agenticph.com"
)
