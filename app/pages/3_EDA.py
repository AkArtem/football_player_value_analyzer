import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("dashboard_data.csv")
df = load_data()

st.title("Exploratory Data Analysis")
st.subheader("Market value distribution")
col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(6,4))
    ax.hist(df['current_value'], bins=67)
    ax.set_title("Raw distribution")
    ax.set_xlabel("Current value")
    st.pyplot(fig)
with col2:
    fig, ax = plt.subplots(figsize=(6,4))
    ax.hist(df['log_value'], bins=67)
    ax.set_title("Log distribution")
    ax.set_xlabel("log(Current value)")
    st.pyplot(fig)
st.markdown("Raw value is very right-skewed since the main part of players have low transfer value(a few very expensive players). \n"
            "While log-transform makes it closer to normal distribution. Which is the reason why model use log(value)")
st.markdown("---")

st.subheader("Age vs market value")
col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(10,5))
    ax.scatter(df["age"], df["current_value"], alpha=0.6, s=7)
    ax.set_title("Scatter plot of age vs market value")
    ax.set_xlabel("Age")
    ax.set_ylabel("Current value")
    st.pyplot(fig)
with col2:
    fig, ax = plt.subplots(figsize=(10,5))
    ax.scatter(df["age"], df["log_value"], alpha=0.6, s=7)
    ax.set_title("Scatter plot of age vs log market value")
    ax.set_xlabel("Age")
    ax.set_ylabel("Log(Current value)")
    st.pyplot(fig)
st.markdown("Raw market value is very close to 0 for most players, and only a few players have very high market value. "
    "log(Value) follows an arch shape, rises until the 25-27 age group, then declines. Which is why age_squared is used as a feature alongside age.")
st.markdown("---")

