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
    df["note"] = df.apply(lambda row: "; ".join(flags(row)), axis=1)
    return df

@st.cache_data
def load_metrics():
    with open(os.path.join(APP_ROOT, "metrics.json")) as f:
        return json.load(f)

DEFAULT_MIN_VALUE = 2_000_000
DEFAULT_MAX_VALUE = 40_000_000
DEFAULT_RECENT_MINUTES = 900
ELITE_VALUE = 40_000_000
DATA_NOTE = "Valuations mostly from December 2025 (Transfermarkt data, downloaded July 2026)."


def fmt_eur(x):
    """€4.6M / €850K instead of €4,563,346 (the model is not precise to the euro)."""
    if x >= 1_000_000:
        return f"€{x / 1_000_000:.1f}M"
    return f"€{x / 1_000:.0f}K"


def verdict(residual):
    """Plain-language reading of a residual. It compares the market price with the stats-based estimate;
    a big gap can mean the market knows something the data doesn't."""
    if residual <= -0.7:
        return "Market value far below the stats-based estimate"
    if residual <= -0.3:
        return "Market value below the stats-based estimate"
    if residual < 0.3:
        return "Market value close to the stats-based estimate"
    if residual < 0.7:
        return "Market value above the stats-based estimate"
    return "Market value far above the stats-based estimate"


def flags(row):
    """Short reasons why the stats-based estimate for a player may be off."""
    notes = []
    if row["recent_minutes"] < 900:
        notes.append("few recent minutes (injury / new arrival?)")
    if row["league_tier_missing"] == 1:
        notes.append("main league not in dataset")
    elif row["league_tier"] == 1 and row["current_value"] >= 10_000_000:
        notes.append("high price in a smaller league")
    if row["age"] >= 21 and row["total_minutes"] < 700 * (row["age"] - 18):
        notes.append("few career minutes for age (uncovered leagues?)")
    if row["residual_std"] > 0.15:
        notes.append("unstable prediction")
    return notes
