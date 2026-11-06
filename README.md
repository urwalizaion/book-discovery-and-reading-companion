# 📚 Book Discovery Companion

A Python Streamlit app that helps you discover books via Open Library + AI summaries via Gemini.

## ✨ Features
- 🔍 Search books using Open Library API
- 🤖 AI-powered summaries using Google Gemini (supports new AQ. keys)
- 📖 Personal reading list (reading_list.json)
- 💾 Streamlit secrets for secure API keys

## 🚀 Setup
1. Clone repo: `git clone https://github.com/urwalization/book-discovery-companion.git`
2. Install: `pip install -r requirements.txt`
3. Add API key to `.streamlit/secrets.toml`:
4. Run: `streamlit run app.py`

## 🔧 Fix for AQ. Keys (Nov 2026)
Google now issues `AQ.` keys. This app uses new SDK:
```python
from google import genai
client = genai.Client(api_key=api_key)

