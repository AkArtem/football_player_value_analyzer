import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from utils import load_data, DEFAULT_MIN_VALUE, DEFAULT_MAX_VALUE, DEFAULT_RECENT_MINUTES

st.set_page_config(layout="wide")
df = load_data()

stable_only = st.sidebar.checkbox("Hide unstable predictions (residual_std > 0.15)", value=True)
st.sidebar.header("Filters")
pos = st.sidebar.multiselect("Position", options=sorted(df['position'].unique()), default=sorted(df['position'].unique()))
min_age, max_age = st.sidebar.slider("Age", float(df['age'].min()), float(df['age'].max()), (18.0, 35.0))
min_minutes = st.sidebar.number_input("Minimum minutes (last 12 months)", min_value=0, value=DEFAULT_RECENT_MINUTES, step=100)
min_value = st.sidebar.number_input("Minimum market value (€)", min_value=0, value=DEFAULT_MIN_VALUE, step=500000, max_value=300000000)
max_value = st.sidebar.number_input("Maximum market value (€)", min_value=0, value=DEFAULT_MAX_VALUE, step=1000000, max_value=300000000)

mask = (
    df['position'].isin(pos)
    & df['current_value'].between(min_value, max_value)
    & df['age'].between(min_age, max_age)
    & (df['recent_minutes'] >= min_minutes)
)
if stable_only:
    mask = mask & (df['residual_std'] <= 0.15)
df_f = df[mask].reset_index(drop=True)

st.title("Undervalued / Overvalued Players")
st.markdown(f"Showing **{len(df_f)}** players (filtered from {len(df)} total). "
            "*Predicted* = what the stats suggest, *Pct in price group* = rank among players of similar price (0% = most undervalued).")
N = st.sidebar.slider("Top N", 5, 50, 10)
cols = {'name': 'Player', 'position': 'Position', 'age': 'Age', 'current_value': 'Market value',
        'pred_eur': 'Predicted', 'residual': 'Residual', 'residual_std': 'Stability (std)',
        'pct_in_group': 'Pct in price group'}
fmt = {'Age': '{:.1f}', 'Market value': '€{:,.0f}', 'Predicted': '€{:,.0f}',
       'Residual': '{:.2f}', 'Stability (std)': '{:.2f}', 'Pct in price group': '{:.0%}'}
col1, col2 = st.columns(2)
df_f["pred_eur"] = np.expm1(df_f["predicted_log_value"]).round(0).astype(int)
with col1:
    st.subheader(f"Most undervalued (top {N})")
    underv = df_f.sort_values('residual').head(N)[['name', 'position', 'age', 'current_value', 'residual', 'pred_eur', 'residual_std', 'pct_in_group']]
    st.dataframe(underv.rename(columns=cols).style.format(fmt), width='stretch', hide_index=True)

with col2:
    st.subheader(f"Most overvalued (top {N})")
    over = df_f.sort_values('residual', ascending=False).head(N)[['name', 'position', 'age', 'current_value', 'residual', 'pred_eur', 'residual_std', 'pct_in_group']]
    st.dataframe(over.rename(columns=cols).style.format(fmt), width='stretch', hide_index=True)

st.caption("Big positive residuals usually mean the market knows something that is not in the data: "
           "a recent transfer from a league that the dataset does not cover (so career minutes look low), a comeback from injury, or youth potential.")

st.header("Residuals scatter")
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(df_f['predicted_log_value'], df_f['residual'], alpha=0.6, s=20)
ax.axhline(0, color='red', linestyle='--')
ax.set_xlabel("Predicted log(value)")
ax.set_ylabel("Residual")
st.pyplot(fig)

st.download_button("Download filtered table (CSV)", df_f.to_csv(index=False), file_name="players_filtered.csv", mime="text/csv")