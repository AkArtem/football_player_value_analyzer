import streamlit as st
import numpy as np
from utils import load_data, verdict, flags, fmt_eur, ELITE_VALUE

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
        col1.metric("Market value", fmt_eur(row['current_value']))
        col2.metric("Stats-based estimate", fmt_eur(np.expm1(row['predicted_log_value'])))
        col3.metric("Residual", f"{row['residual']:.2f}")
        
        st.write(f"**{verdict(row['residual'])}** · {row['pct_in_group']:.0%} percentile in price group {row['value_group']} · stability (std) {row['residual_std']:.2f}")
        st.write(f"Position: {row['position']}, Age: {row['age']:.1f}, Minutes last 12 months: {row['recent_minutes']:.0f}, Career minutes in dataset: {row['total_minutes']}")
        for note in flags(row):
            st.caption(f"{note}")
        st.markdown("---")