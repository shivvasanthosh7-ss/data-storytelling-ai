import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import PyPDF2
import io

# 🔥 MUST BE FIRST
st.set_page_config(page_title="Data Story AI", layout="wide")

# Sidebar
st.sidebar.title("⚙️ Options")
show_data = st.sidebar.checkbox("Show Data Preview", True)
show_graphs = st.sidebar.checkbox("Show Visualizations", True)
show_insights = st.sidebar.checkbox("Show Insights", True)

# Title
st.title("📊 Data Storytelling AI")
st.markdown("## 📊 Smart Data Analysis & AI Insights")
st.markdown("---")

# Upload (CSV + PDF)
uploaded_file = st.file_uploader("Upload CSV or PDF", type=["csv", "pdf"])

# ================= CSV PART =================
if uploaded_file is not None and uploaded_file.name.endswith(".csv"):
    df = pd.read_csv(uploaded_file)

    if show_data:
        st.subheader("📁 Dataset Preview")
        st.write(df.head())

    # Summary
    st.subheader("📊 Summary Statistics")
    st.write(df.describe())

    # Missing values
    st.subheader("❌ Missing Values")
    st.write(df.isnull().sum())

    # Visualization
    if show_graphs:
        st.subheader("📈 Visualizations")
        numeric_cols = df.select_dtypes(include=['int64','float64']).columns

        for col in numeric_cols:
            fig, ax = plt.subplots()
            sns.histplot(df[col], kde=True, ax=ax)
            ax.set_title(f"{col} Distribution")
            st.pyplot(fig)

        # Correlation
        if len(numeric_cols) > 1:
            fig, ax = plt.subplots()
            sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)

    # FREE INSIGHTS
    if show_insights and st.button("Generate Insights"):
        st.subheader("🧠 Insights (FREE AI)")

        st.write(f"✔ Dataset has {df.shape[0]} rows and {df.shape[1]} columns")
        st.write(f"✔ Missing values: {df.isnull().sum().sum()}")

        means = df.mean(numeric_only=True)
        st.write("📊 Average Values:")
        st.write(means)

        st.write("🏆 Key Observations:")
        for col in means.index:
            st.write(f"• {col} average is {means[col]:.2f}")

        st.write("🚀 Recommendations:")
        st.write("• Clean missing data if present")
        st.write("• Focus on high-value features")
        st.write("• Use correlation heatmap for relationships")

# ================= PDF PART =================
elif uploaded_file is not None and uploaded_file.name.endswith(".pdf"):
    st.subheader("📄 PDF Preview & Insights")

    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"

    st.text_area("Extracted Text", text[:2000], height=300)

    if st.button("Generate Insights from PDF"):
        st.subheader("🧠 PDF Insights (FREE)")

        word_count = len(text.split())
        st.write(f"✔ Total words: {word_count}")

        st.write("📌 Key Insights:")
        st.write("• This document contains textual information")
        st.write("• Useful for summaries and keyword extraction")
        st.write("• Can be further processed using NLP")

# ================= DOWNLOAD =================
if uploaded_file is not None:
    if st.button("Download Report"):
        report = f"""
        DATA REPORT

        File: {uploaded_file.name}

        """

        st.download_button(
            label="Download TXT",
            data=report,
            file_name="report.txt",
            mime="text/plain"
        )