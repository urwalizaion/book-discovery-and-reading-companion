import streamlit as st
from google import genai

def get_summary(title, author):
    api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else None
    if not api_key:
        return "Add GEMINI_API_KEY in Secrets"
    client = genai.Client(api_key=api_key)
    r = client.models.generate_content(model="gemini-2.0-flash", contents=f"Write a short 3-sentence summary for '{title}' by {author}.")
    return r.text

def get_reading_level(title):
    api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else None
    client = genai.Client(api_key=api_key)
    r = client.models.generate_content(model="gemini-2.0-flash", contents=f"Reading level for '{title}'? One sentence.")
    return r.text

def get_questions(title):
    api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else None
    client = genai.Client(api_key=api_key)
    r = client.models.generate_content(model="gemini-2.0-flash", contents=f"3 discussion questions for '{title}'.")
    return r.text
