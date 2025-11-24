import os
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI


def get_chat_model():
    groq_key = os.getenv("GROQ_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")

    if groq_key:
        return ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=groq_key,
            temperature=0.6,
        )

    if openai_key:
        return ChatOpenAI(
            model="gpt-4o-mini",
            api_key=openai_key,
            temperature=0.6,
        )

    if google_key:
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            api_key=google_key,
            temperature=0.6,
        )

    raise Exception("No API keys found. Please add API keys.")
