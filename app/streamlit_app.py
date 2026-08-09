import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Football Player Value Analyzer", layout="wide")

@st.cache_data
def load_data():
    csv_path = os.path.join(os.path.dirname(__file__), 'dashboard_data.csv')
    return pd.read_csv(csv_path)

df = load_data()
st.title("Football Player Value Analyzer")
st.markdown("Identifying over/undervalued players via residual analysis of market value vs performance stats")

st.sidebar.header("Filters")

min_value = st.sidebar.number_input("Minimum market value (€)", min_value=0, value=400000, step=100000, max_value=220000000)
max_value = st.sidebar.number_input("Maximum market value (€)", min_value=0, value=20000000, step=1000000, max_value=300000000)

positions = sorted(df["position"].dropna().unique().tolist())
selected_positions = st.sidebar.multiselect("Position", positions, default=positions)

min_age, max_age =st.sidebar.slider("Age range", float(df["age"].min()), float(df["age"].max()),(18.0, 35.0))

min_minutes = st.sidebar.number_input("Minimum minutes played", min_value=0, value=900, step=100)

filtered = df[df["current_value"].between(min_value, max_value) & df["position"].isin(selected_positions) & df["age"].between(min_age, max_age) & (df["total_minutes"] >= min_minutes)].copy()
st.info("This model works best in the broad mid-market. Extreme elite values are less reliable because brand, hype, contract situation, and league context are not fully captured in this dataset.")

if len(filtered) == 0:
    st.warning("No players match selected filters")
    st.stop()
    
if filtered["current_value"].max() > 20000000:
    st.warning("Some selected players are in the high-value range, where predictions are less stable and reliable")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Players analyzed", len(filtered))
col2.metric("Avg market value", f"€{filtered['current_value'].mean():,.0f}")
most_undervalued = filtered.loc[filtered['residual'].idxmin()]
col3.metric("Most undervalued", most_undervalued['name'], f"residual: {most_undervalued['residual']:.2f}")
col4.metric("Model R^2", "0.61")

st.markdown("---")
st.subheader("Model comparison")
results_table = pd.DataFrame({
    'Model': ['Mean baseline', 'Minutes-only', 'Linear Regression with recent stats', 'Tuned Random Forest with recent stats'],
    'RMSE': [1.72, 1.67, 1.22, 1.07],
    'R^2': [-0.00, 0.07, 0.50, 0.61]})
st.table(results_table)
st.markdown("This tool is best suited for identifying value inefficiencies in the broad mid-market (€400K–€20M). Predictions for elite, globally-recognized players tend to be less reliable, since their value is driven by brand and marketing factors not captured in performance stats. See Known Limitations for details.")
st.subheader("Notable players in this dataset")
featured_names = ["Erling Haaland", "Jude Bellingham", "Harry Kane", "Federico Valverde"]
cols = st.columns(len(featured_names))
for col, name in zip(cols, featured_names):
    player_rows = df[df['name'] == name]
    with col:
        if not player_rows.empty:
            player = player_rows.iloc[0]
            st.metric(name, f"€{player['current_value']:,.0f}", f"{player['position']}, age {player['age']:.0f}")
        else:
            st.info(f"{name} not found in dataset")