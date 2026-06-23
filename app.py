import streamlit as st
import pandas as pd
from analysis import analyze_data
from visualization import plot_data
from insights import generate_insights, chat_with_data

# 🔥 MUST BE FIRST
st.set_page_config(page_title="Data Story AI", layout="wide")

# Header
st.markdown("## 📊 Smart Data Analysis & AI Insights")
st.markdown("---")

# Sidebar
st.sidebar.title("⚙️ Options")
show_data = st.sidebar.checkbox("Show Data Preview", True)
show_graphs = st.sidebar.checkbox("Show Visualizations", True)
show_insights = st.sidebar.checkbox("Show Insights", True)
show_chat = st.sidebar.checkbox("Enable AI Chat", True)

# Title
st.title("📊 Data Storytelling AI")
st.caption("Upload CSV or PDF and get insights")

# Upload
uploaded_file = st.file_uploader("Upload CSV or PDF", type=["csv", "pdf"])

if uploaded_file is not None:

    # ================= CSV =================
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

        if show_data:
            st.subheader("📁 Dataset Preview")
            st.write(df.head())

        # Analysis
        summary, nulls = analyze_data(df)

        if show_data:
            st.subheader("📊 Summary Statistics")
            st.write(summary)

            st.subheader("❌ Missing Values")
            st.write(nulls)

        # Visualization
        if show_graphs:
            st.subheader("📈 Visualizations")
            plot_data(df)

        # Insights
        if show_insights:
            if st.button("Generate Insights"):
                st.subheader("🧠 Insights")
                result = generate_insights(df)
                st.write(result)

        # Chat
        if show_chat:
            st.subheader("💬 Chat with your Data")
            question = st.text_input("Ask something about your data:")

            if st.button("Ask AI"):
                if question:
                    answer = chat_with_data(df, question)
                    st.success(answer)
                else:
                    st.warning("Enter a question")

        # Download report
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

    # ================= PDF =================
    elif uploaded_file.name.endswith(".pdf"):

        import PyPDF2

        st.subheader("📄 PDF Analysis")

        # Read PDF
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""

        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted

        # Show preview
        st.subheader("📜 Extracted Text (Preview)")
        st.text_area("PDF Content", text[:2000], height=300)

        # AI Insights for PDF
        if st.button("Generate Insights from PDF"):

            from openai import OpenAI
            import os

            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": f"Analyze this document and give summary + insights:\n\n{text[:2000]}"
                    }
                ]
            )

            st.subheader("🧠 PDF Insights")
            st.write(response.choices[0].message.content)

        # Download PDF
        st.download_button(
            label="Download PDF",
            data=uploaded_file,
            file_name=uploaded_file.name,
            mime="application/pdf"
        )