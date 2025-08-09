import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Run History", layout="wide")
st.title("Run History")

p = Path("data/runs.csv")
if p.exists():
    df = pd.read_csv(p)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No runs yet. Go run the agent on the Home page.")
