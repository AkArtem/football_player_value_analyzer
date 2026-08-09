import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

st.set_page_config(layout="wide")
@st.cache_data
def load_data():
    csv_path = os.path.join(os.path.dirname(__file__), 'dashboard_data.csv')
    return pd.read_csv(csv_path)

df = load_data()
st.sidebar.header("Filters")
pos = st.sidebar.multiselect("Position", options=sorted(df['position'].unique()), default=sorted(df['position'].unique()))
min_age, max_age = st.sidebar.slider("Age", float(df['age'].min()), float(df['age'].max()), (18.0, 35.0))
min_minutes = st.sidebar.number_input("Minimum minutes played", min_value=0, value=900, step=100)
min_value = st.sidebar.number_input("Minimum market value (€)", min_value=0, value=400000, step=100000, max_value=300000000)
max_value = st.sidebar.number_input("Maximum market value (€)", min_value=0, value=20000000, step=1000000, max_value=300000000)

mask = (df['position'].isin(pos)) & (df['current_value'].between(min_value, max_value)) & (df['age'].between(min_age, max_age)) & (df['total_minutes'] >= min_minutes)
df_f = df[mask].reset_index(drop=True)

st.title("Undervalued / Overvalued Players")
st.markdown(f"Showing **{len(df_f)}** players (filtered from {len(df)} total)")
N = st.sidebar.slider("Top N", 5, 50, 10)
col1, col2 = st.columns(2)
df_f["pred_eur"] = np.expm1(df_f["predicted_log_value"]).round(0).astype(int)
with col1:
    st.subheader(f"Most undervalued (top {N})")
    underv = df_f.sort_values('residual').head(N)[['name', 'position', 'age', 'current_value', 'residual', 'pred_eur']]
    st.dataframe(underv.style.format({"age": "{:,.1f}", "current_value": "{:,.0f}", "pred_eur": "€{:,.0f}"}), use_container_width=True)

with col2:
    st.subheader(f"Most overvalued (top {N})")
    over = df_f.sort_values('residual', ascending=False).head(N)[['name', 'position', 'age', 'current_value', 'residual', 'pred_eur']]
    st.dataframe(over.style.format({"age": "{:,.1f}", "current_value": "{:,.0f}", "pred_eur": "€{:,.0f}"}), use_container_width=True)

st.header("Residuals scatter")
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(df_f['predicted_log_value'], df_f['residual'], alpha=0.6, s=20)
ax.axhline(0, color='red', linestyle='--')
ax.set_xlabel("Predicted log(value)")
ax.set_ylabel("Residual")
st.pyplot(fig)

st.download_button("Download filtered table (CSV)", df_f.to_csv(index=False), file_name="players_filtered.csv", mime="text/csv")