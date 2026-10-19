import streamlit as st
import pandas as pd
import numpy as np
from utils import load_data, load_metrics, fmt_eur, DATA_NOTE, DEFAULT_MIN_VALUE, DEFAULT_MAX_VALUE, DEFAULT_RECENT_MINUTES, ELITE_VALUE

df = load_data()
m = load_metrics()

st.title("Football Player Value Analyzer")
st.markdown("Which players are cheap or expensive **compared with what their stats suggest?** "
            "A Gradient Boosting model predicts each player's Transfermarkt value from playing time, age, league level and recent form. "
            "The gap between the real and the predicted value (the *residual*) shows who the market rates higher or lower than the stats do. "
            "A big gap is not proof of a bad price: injuries, contracts, hype and leagues outside the dataset are not in the model.")

st.sidebar.header("Filters")

min_value = st.sidebar.number_input("Minimum market value (€)", min_value=0, value=DEFAULT_MIN_VALUE, step=500000, max_value=300000000)
max_value = st.sidebar.number_input("Maximum market value (€)", min_value=0, value=DEFAULT_MAX_VALUE, step=1000000, max_value=300000000)

positions = sorted(df["position"].dropna().unique().tolist())
selected_positions = st.sidebar.multiselect("Position", positions, default=positions)

min_age, max_age =st.sidebar.slider("Age range", float(df["age"].min()), float(df["age"].max()),(18.0, 35.0))

min_minutes = st.sidebar.number_input("Minimum minutes (last 12 months)", min_value=0, value=DEFAULT_RECENT_MINUTES, step=100)

filtered = df[df["current_value"].between(min_value, max_value) & df["position"].isin(selected_positions) & df["age"].between(min_age, max_age) & (df["recent_minutes"] >= min_minutes)].copy()
st.info("The model works best in the broad mid-market (about €1M–€40M). Elite values are less reliable because brand, hype, contracts and injuries are not in the data.")

if len(filtered) == 0:
    st.warning("No players match selected filters")
    st.stop()
    
if filtered["current_value"].max() > ELITE_VALUE:
    st.warning("Some selected players are in the high-value range, where predictions are less stable and reliable")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Players analyzed", len(filtered))
col2.metric("Avg market value", fmt_eur(filtered['current_value'].mean()))
most_undervalued = filtered.loc[filtered['residual'].idxmin()]
col3.metric("Biggest gap below estimate", most_undervalued['name'])
col3.caption(f"residual {most_undervalued['residual']:.2f}")
col4.metric("Model R² (5-fold CV)", f"{m['cv_r2']:.3f}")

st.markdown("---")
st.subheader("Model comparison")
models = pd.DataFrame(m["models"]).rename(columns={"R^2": "R²", "RMSE": "RMSE (log)"})
st.dataframe(models.style.format({"RMSE (log)": "{:.3f}", "R²": "{:.3f}"}), hide_index=True, width='stretch')
st.caption(f"Final model: tuned Gradient Boosting. Hold-out R² = {m['holdout_r2']:.3f}. {DATA_NOTE}")

st.markdown("**How to read a residual:** residual = log(real value) − log(predicted value). "
            "−0.7 means the market price is about half of the stats-based estimate, +0.7 means about double. "
            "Use the **Rankings** page for top lists and **Player Search** for a single player.")
st.subheader("Notable players in this dataset")
featured_names = ["Erling Haaland", "Jude Bellingham", "Harry Kane", "Federico Valverde"]
cols = st.columns(len(featured_names))
for col, name in zip(cols, featured_names):
    player_rows = df[df['name'] == name]
    with col:
        if not player_rows.empty:
            player = player_rows.iloc[0]
            st.metric(name, fmt_eur(player['current_value']))
            st.caption(f"{player['position']}, age {player['age']:.0f} · estimate {fmt_eur(np.expm1(player['predicted_log_value']))}")
        else:
            st.info(f"{name} not found in dataset")