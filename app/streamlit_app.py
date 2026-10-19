import streamlit as st

st.set_page_config(page_title="Football Player Value Analyzer", layout="wide")

pages = [
    st.Page("home.py", title="Home", default=True),
    st.Page("pages/1_Rankings.py", title="Rankings"),
    st.Page("pages/2_Player_Search.py", title="Player Search"),
    st.Page("pages/3_EDA.py", title="EDA"),
]
st.navigation(pages).run()
