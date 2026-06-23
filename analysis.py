def analyze_data(df):
    summary = df.describe(include='all')
    nulls = df.isnull().sum()
    return summary, nulls