def generate_insights(df):
    rows, cols = df.shape
    missing = df.isnull().sum().sum()

    numeric = df.select_dtypes(include=['number'])

    return f"""
📊 Dataset has {rows} rows and {cols} columns.

❌ Missing values: {missing}

📈 Avg values:
{numeric.mean().to_string()}

📊 Max values:
{numeric.max().to_string()}

💡 Insight:
- Some features have high variation
- Trends can be identified using charts

🚀 Recommendation:
- Clean missing values
- Focus on high-value columns
"""