import streamlit as st
import pandas as pd
from analysis import analyze_data
from visualization import plot_data
from insights import generate_insights

# 🔥 Page settings (ADD THIS AT TOP)
st.set_page_config(page_title="Data Story AI", layout="wide")

# Title
st.title("📊 Data Storytelling AI")

# Upload file
file = st.file_uploader("Upload CSV", type=["csv"])

if file:
    df = pd.read_csv(file)

    # Preview
    st.subheader("📁 Dataset Preview")
    st.write(df.head())

    # Analysis
    summary, nulls = analyze_data(df)

    st.subheader("📊 Summary Statistics")
    st.write(summary)

    st.subheader("❌ Missing Values")
    st.write(nulls)

    # Visualization
    st.subheader("📈 Visualizations")
    plot_data(df)

    # Insights
    if st.button("Generate Insights"):
        st.subheader("🧠 Insights")
        result = generate_insights(df)
        st.write(result)