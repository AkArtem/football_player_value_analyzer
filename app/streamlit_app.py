import streamlit as st
import pandas as pd

st.set_page_config(page_title="Football Player Value Analyzer", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv('dashboard_data.csv')

df = load_data()
st.title("Football Player Value Analyzer")
st.markdown("Identifying over/undervalued players via residual analysis of market value vs performance stats")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Players analyzed", len(df))
col2.metric("Avg market value", f"€{df['current_value'].mean():,.0f}")
most_undervalued = df.loc[df['residual'].idxmin()]
col3.metric("Most undervalued", most_undervalued['name'], f"residual: {most_undervalued['residual']:.2f}")
col4.metric("Model R^2", "0.576")

st.markdown("---")
st.subheader("Model comparison")
results_table = pd.DataFrame({
    'Model': ['Mean baseline', 'Minutes-only', 'Linear Regression', 'Random Forest (tuned)'],
    'RMSE': [1.72, 1.67, 1.41, 1.12],
    'R^2': [0.00, 0.07, 0.33, 0.58]})
st.table(results_table)
st.markdown("This tool is best suited for identifying value inefficiencies in the broad mid-market (€500K–€30M). Predictions for elite, globally-recognized players tend to be less reliable, since their value is driven by brand and marketing factors not captured in performance stats. See Known Limitations for details.")
st.subheader("Notable players in this dataset")
featured_names = ["Erling Haaland", "Jude Bellingham", "Harry Kane", "Federico Valverde"]
cols = st.columns(len(featured_names))
for col, name in zip(cols, featured_names):
    player = df[df['name'] == name].iloc[0]
    with col:
        st.metric(name, f"€{player['current_value']:,.0f}", f"{player['position']}, age {player['age']:.0f}")