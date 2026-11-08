import google.generativeai as genai
import os

# Set your API key in Streamlit secrets
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_summary(title, author):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Write a short 3-sentence summary for the book '{title}' by {author}."
    response = model.generate_content(prompt)
    return response.text

def get_reading_level(title):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"What is the reading level (Beginner, Intermediate, Advanced) for book '{title}'? Explain why in one sentence."
    response = model.generate_content(prompt)
    return response.text

def get_questions(title):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Generate 3 discussion questions for the book '{title}'."
    response = model.generate_content(prompt)
    return response.text