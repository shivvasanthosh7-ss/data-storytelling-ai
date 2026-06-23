import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def plot_data(df):
    numeric = df.select_dtypes(include=['number'])

    # Histograms
    if not numeric.empty:
        for col in numeric.columns[:3]:
            fig, ax = plt.subplots()
            df[col].hist(ax=ax)
            ax.set_title(f"{col} Distribution")
            st.pyplot(fig)

    # 🔥 Heatmap
    if len(numeric.columns) > 1:
        st.subheader("📊 Correlation Heatmap")
        corr = numeric.corr()

        fig, ax = plt.subplots(figsize=(8,5))
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)