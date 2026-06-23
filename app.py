import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import PyPDF2

# 🔥 MUST BE FIRST
st.set_page_config(page_title="Data Story AI Pro", layout="wide")

# ========== SESSION ==========
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ========== SIDEBAR ==========
st.sidebar.title("🚀 Data Story AI")
page = st.sidebar.radio("Navigate", [
    "🏠 Home",
    "📊 CSV Dashboard",
    "💬 Chat with Data",
    "📄 PDF Resume Analyzer"
])

# ========== HOME ==========
if page == "🏠 Home":
    st.title("🚀 Data Storytelling AI PRO")
    st.markdown("""
    ### 💡 Features:
    - 📊 Data Analysis Dashboard  
    - 💬 Chat with your dataset  
    - 📄 Resume Analyzer  
    - 📈 Smart Visualizations  
    """)

# ========== CSV DASHBOARD ==========
elif page == "📊 CSV Dashboard":

    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:
        df = pd.read_csv(file)

        st.subheader("📊 KPI Dashboard")

        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Missing", df.isnull().sum().sum())

        st.subheader("📁 Data Preview")
        st.dataframe(df.head())

        st.subheader("📈 Visualizations")

        num_cols = df.select_dtypes(include=['int64','float64']).columns

        for col in num_cols:
            fig, ax = plt.subplots()
            sns.histplot(df[col], kde=True, ax=ax)
            ax.set_title(col)
            st.pyplot(fig)

        if len(num_cols) > 1:
            fig, ax = plt.subplots()
            sns.heatmap(df[num_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)

# ========== CHAT ==========
elif page == "💬 Chat with Data":

    file = st.file_uploader("Upload CSV for Chat", type=["csv"])

    if file:
        df = pd.read_csv(file)

        st.subheader("💬 Ask Questions")

        user_q = st.text_input("Ask (average steps, max sleep_hours, rows...)")

        if user_q:
            user_q = user_q.lower()
            answer = ""

            if "average" in user_q:
                col = user_q.split()[-1]
                if col in df.columns:
                    answer = f"Average {col} = {df[col].mean():.2f}"

            elif "max" in user_q:
                col = user_q.split()[-1]
                if col in df.columns:
                    answer = f"Max {col} = {df[col].max()}"

            elif "min" in user_q:
                col = user_q.split()[-1]
                if col in df.columns:
                    answer = f"Min {col} = {df[col].min()}"

            elif "rows" in user_q:
                answer = f"Total rows = {df.shape[0]}"

            else:
                answer = "Try: average steps, max sleep_hours"

            st.session_state.chat_history.append((user_q, answer))

        # Chat display
        for q, a in st.session_state.chat_history:
            st.markdown(f"**You:** {q}")
            st.markdown(f"**AI:** {a}")

# ========== PDF ANALYZER ==========
elif page == "📄 PDF Resume Analyzer":

    file = st.file_uploader("Upload PDF Resume", type=["pdf"])

    if file:
        pdf = PyPDF2.PdfReader(file)
        text = ""

        for page in pdf.pages:
            text += page.extract_text() or ""

        st.subheader("📄 Resume Preview")
        st.text_area("", text[:2000], height=300)

        if st.button("Analyze Resume"):
            st.subheader("🧠 Resume Insights")

            text_lower = text.lower()

            skills = [
                "python","sql","excel","power bi",
                "machine learning","data analysis",
                "pandas","numpy","statistics"
            ]

            found = [s for s in skills if s in text_lower]

            st.write("🎯 Skills Found:")
            for s in found:
                st.success(s)

            score = min(len(found) * 12, 100)

            st.write("📊 Resume Score")
            st.progress(score)
            st.write(f"{score}/100")

            if score < 50:
                st.warning("Add more technical skills")
            else:
                st.success("Strong resume!")

# ========== REPORT ==========
st.sidebar.markdown("---")
if st.sidebar.button("📥 Download App Report"):
    report = "Data Story AI Pro Report\n\nProject by Shivva Santhosh"
    st.sidebar.download_button("Download", report, file_name="report.txt")