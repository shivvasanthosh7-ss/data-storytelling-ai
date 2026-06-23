from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_insights(df):
    data_sample = df.head(20).to_string()

    prompt = f"""
    Analyze this dataset and give insights:

    {data_sample}

    Give:
    - Summary
    - Patterns
    - Recommendations
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# 🔥 NEW FUNCTION (CHAT)
def chat_with_data(df, question):
    data_sample = df.head(20).to_string()

    prompt = f"""
    Dataset:
    {data_sample}

    User question:
    {question}

    Answer clearly based on data.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content