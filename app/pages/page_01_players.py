import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
@st.cache_data
def load_data():
    return pd.read_csv('../dashboard_data.csv')

df = load_data()
st.sidebar.header("Filters")
pos = st.sidebar.multiselect("Position", options=sorted(df['position'].unique()), default=sorted(df['position'].unique()))
min_age, max_age = st.sidebar.slider("Age", float(df['age'].min()), float(df['age'].max()), (18.0, 35.0))
min_minutes = st.sidebar.number_input("Minimum minutes played", min_value=0, value=900, step=100)

mask = (df['position'].isin(pos)) & (df['age'].between(min_age, max_age)) & (df['total_minutes'] >= min_minutes)
df_f = df[mask].reset_index(drop=True)
st.set_page_config(layout="wide")
st.title("Undervalued / Overvalued Players")
st.markdown(f"Showing **{len(df_f)}** players (filtered from {len(df)} total)")
N = st.sidebar.slider("Top N", 5, 50, 10)
col1, col2 = st.columns(2)
df_f["pred_eur"] = np.exp(np.log(df_f["current_value"]) - df_f["residual"]).round(0).astype(int)
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
top_100 = df.nlargest(100, 'current_value')
print(f"Mean residual for top 100 by value: {top_100['residual'].mean():.3f}")
print(f"% with positive residual (underpredicted): {(top_100['residual'] > 0).mean() * 100:.1f}%")

print(top_100[['name', 'current_value', 'residual']].sort_values('residual', ascending=False).head(15))

