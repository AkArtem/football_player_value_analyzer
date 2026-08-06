import streamlit as st
import pandas as pd
import numpy as np
@st.cache_data
def load_data():
    return pd.read_csv('../dashboard_data.csv')

df = load_data()
st.title("Player Search")
search_name = st.text_input("Search by player name:")

if search_name:
    results = df[df['name'].str.contains(search_name, case=False, na=False)]
    results = results.sort_values('current_value', ascending=False)
    for index, row in results.iterrows():
        st.subheader(row['name'])
        col1, col2, col3 = st.columns(3)
        col1.metric("Actual Value", f"€{row['current_value']:,.0f}")
        col2.metric("Predicted Value", f"€{np.exp(np.log(row['current_value']) - row['residual']):,.0f}, €{row['predicted_log_value']:.0f} (log scale)")
        col3.metric("Residual", f"{row['residual']:.2f}")
        
        st.write(f"Position: {row['position']}, Age: {row['age']:.1f}, Total Minutes: {row['total_minutes']}")