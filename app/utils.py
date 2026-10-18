import os
import json
import pandas as pd
import streamlit as st

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(APP_ROOT,"dashboard_data.csv"))
    df["value_group"] = pd.qcut(df["current_value"], 5, labels=["<0.4M", "0.4-0.9M", "0.9-2.5M", "2.5-8M", ">8M"])
    df["pct_in_group"] = df.groupby("value_group", observed=True)["residual"].rank(pct=True)
    return df

@st.cache_data
def load_metrics():
    with open(os.path.join(APP_ROOT, "metrics.json")) as f:
        return json.load(f)
