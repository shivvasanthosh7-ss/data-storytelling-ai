import streamlit as st
import pandas as pd
from analysis import analyze_data
from visualization import plot_data
from insights import generate_insights

st.set_page_config(page_title="Data Story AI", layout="wide")

st.markdown("##  Smart Data Analysis & AI Insights")
st.markdown("---")


st.sidebar.title(" Options")
show_data = st.sidebar.checkbox("Show Data Preview", True)
show_graphs = st.sidebar.checkbox("Show Visualizations", True)
show_insights = st.sidebar.checkbox("Show Insights", True)


st.title(" Data Storytelling AI")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)


    if show_data:
        st.subheader(" Dataset Preview")
        st.write(df.head())

    
    summary, nulls = analyze_data(df)

    if show_data:
        st.subheader("Summary Statistics")
        st.write(summary)

        st.subheader(" Missing Values")
        st.write(nulls)


    if show_graphs:
        st.subheader(" Visualizations")
        plot_data(df)

    
    if show_insights:
        if st.button("Generate Insights"):
            st.subheader(" Insights")
            result = generate_insights(df)
            st.write(result)

    
    if st.button("Download Report"):
        report = f"""
DATA REPORT

Rows: {df.shape[0]}
Columns: {df.shape[1]}

Missing Values:
{df.isnull().sum()}

Summary:
{df.describe()}
"""

        st.download_button(
            label="Download TXT",
            data=report,
            file_name="report.txt",
            mime="text/plain"
        )