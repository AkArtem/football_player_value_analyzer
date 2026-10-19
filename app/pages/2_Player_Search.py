import streamlit as st
import numpy as np
from utils import load_data, verdict, ELITE_VALUE

st.set_page_config(layout="wide")
df = load_data()


st.title("Player Search")
search_name = st.text_input("Search by player name:", value="", placeholder="Type a player name", help="Enter a player's name to search for them in the dataset")

if search_name:
    results = df[df['name'].str.contains(search_name, case=False, na=False)]
    results = results.sort_values('current_value', ascending=False)
    for index, row in results.iterrows():
        if row['current_value'] > ELITE_VALUE:
            st.warning("This player is in the elite-value range. The model is less reliable above €40M, so treat this estimate as directional.")
        st.subheader(row['name'])
        col1, col2, col3 = st.columns(3)
        col1.metric("Actual Value", f"€{row['current_value']:,.0f}")
        col2.metric("Predicted Value", f"€{np.expm1(row['predicted_log_value']):,.0f}")
        col3.metric("Residual", f"{row['residual']:.2f}")
        
        st.write(f"**{verdict(row['residual'])}** · {row['pct_in_group']:.0%} percentile in price group {row['value_group']} · stability (std) {row['residual_std']:.2f}")
        st.write(f"Position: {row['position']}, Age: {row['age']:.1f}, Minutes last 12 months: {row['recent_minutes']:.0f}, Career minutes in dataset: {row['total_minutes']}")
        if row['residual_std'] > 0.15:
            st.caption("The prediction for this player changes a lot between CV splits, so treat it with caution.")
        st.markdown("---")