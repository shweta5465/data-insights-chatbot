from groq import Groq
from data_handler import load_data, get_summary, get_stats
import os
from dotenv import load_dotenv

# API key loaded from .env file
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

df = load_data()
summary = get_summary(df)
stats = get_stats(df)

def ask_chatbot(user_question, chat_history):

    system_prompt = f"""
    You are a smart data analyst assistant.

    You have access to a sales dataset with this information:
    - Total rows: {summary['total_rows']}
    - Columns: {summary['columns']}
    - Sample data:
    {summary['sample']}

    - Statistical summary:
    {stats}

    Your job:
    1. Answer the user question based on this data
    2. Give clear simple insights
    3. Suggest what chart would best show the answer
    4. Be friendly and helpful
    """

    messages = [{"role": "system", "content": system_prompt}]

    for msg in chat_history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    messages.append({
        "role": "user",
        "content": user_question
    })

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        max_tokens=500
    )

    return response.choices[0].message.content