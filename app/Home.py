import time
import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path
import csv

RUNS_PATH = Path("data/runs.csv")

def log_run(row: dict):
    RUNS_PATH.parent.mkdir(parents=True, exist_ok=True)
    write_header = not RUNS_PATH.exists()
    with RUNS_PATH.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=row.keys())
        if write_header:
            w.writeheader()
        w.writerow(row)


st.set_page_config(page_title="My Agent Dashboard", layout="wide")
st.title("Agent Control Room")

# --- Controls
col1, col2, col3 = st.columns([2,1,1])
with col1:
    query = st.text_input("Task prompt", "Summarize the latest report about X")
with col2:
    max_steps = st.number_input("Max steps", 1, 20, 5)
with col3:
    run_btn = st.button("Run Agent")

# --- Status area
status = st.empty()
log_box = st.container()
result_box = st.container()

# --- Fake metrics (replace with real later)
df = pd.DataFrame({
    "timestamp": pd.date_range("2025-08-01", periods=10, freq="D"),
    "runs": [3,5,2,7,4,6,9,8,11,10],
    "failures": [0,1,0,1,0,1,2,0,1,0],
    "cost_usd": [0.02,0.05,0.01,0.06,0.03,0.07,0.11,0.09,0.14,0.12]
})
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Runs", int(df["runs"].sum()))
m2.metric("Failure Rate", f'{100*df["failures"].sum()/df["runs"].sum():.1f}%')
m3.metric("Avg Cost/Run", f'${df["cost_usd"].mean():.03f}')
m4.metric("Last Run Cost", f'${df["cost_usd"].iloc[-1]:.03f}')

# --- Charts
left, right = st.columns(2)
with left:
    st.subheader("Runs over time")
    st.plotly_chart(px.line(df, x="timestamp", y="runs"))
with right:
    st.subheader("Cost over time")
    st.plotly_chart(px.line(df, x="timestamp", y="cost_usd"))

# --- Agent run simulation (replace with real backend)
if run_btn:
    status.info("Agent queued…")
    logs = []
    for step in range(1, max_steps+1):
        time.sleep(0.4)
        log = f"Step {step}: calling tool / reading resource / reasoning…"
        logs.append(log)
        with log_box:
            st.write(log)
    status.success("Agent finished ✅")
    with result_box:
        st.subheader("Result")
        st.write({
            "prompt": query,
            "answer": "This is where your agent’s answer will show up.",
            "tokens_used": 1234,
            "cost_usd": 0.012,
            "duration_s": round(0.4*max_steps, 1)
        })
    row = {
    "timestamp": pd.Timestamp.now().isoformat(),
    "prompt": query,
    "steps": int(max_steps),
    "tokens_used": 1234,
    "cost_usd": 0.012,
    "status": "success"
    }
    log_run(row)
