import streamlit as st
import json
import os
import requests
from google import genai
from search import search_books, BookSearchError, BookNotFound
from reading_list import load_list, save_list, add_book, move_book, delete_book

try:
    from ai_helper import get_summary
    AI_OLD = True
except:
    AI_OLD = False
    get_summary = None

try:
    from styles import apply_styles
    apply_styles()
except:
    pass

st.set_page_config(page_title="Book Discovery Companion", page_icon="📚")

api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

st.title("📚 Book Discovery and reading Companion")

reading_data = load_list()

query = st.text_input("Search books (Open Library)", placeholder="e.g. Atomic Habits")

if query:
    try:
        books = search_books(query)
        for doc in books[:10]:
            title = doc.get("title", "No title")
            author = doc.get("author", "")
            year = doc.get("year", "")
            
            with st.expander(f"{title} - {author} ({year})"):
                if doc.get("cover_url"):
                    st.image(doc["cover_url"], width=120)
                
                if st.button(f"✨ AI Summary: {title}", key=f"ai_{title}_{year}"):
                    if not client and AI_OLD:
                        summary = get_summary(title, author)
                        st.markdown(summary)
                    elif not client:
                        st.error("Add GEMINI_API_KEY in Streamlit Secrets")
                    else:
                        with st.spinner("Gemini thinking..."):
                            r = client.models.generate_content(
                                model="gemini-2.0-flash", 
                                contents=f"Summarize book '{title}' by {author}. Give: 1) Short summary 2) Reading level 3) 3 discussion questions"
                            )
                            st.markdown(r.text)
                
                c1, c2, c3 = st.columns(3)
                if c1.button("Want", key=f"w_{title}_{year}"):
                    add_book(doc, "want_to_read")
                    st.success(f"Added {title} to Want to Read!")
                if c2.button("Reading", key=f"r_{title}_{year}"):
                    add_book(doc, "reading")
                    st.success(f"Added {title} to Reading!")
                if c3.button("Done", key=f"d_{title}_{year}"):
                    add_book(doc, "finished")
                    st.success(f"Added {title} to Finished!")

    except BookNotFound as e:
        st.warning(str(e))
    except BookSearchError as e:
        st.error(str(e))

st.divider()
st.subheader("My Reading List")

tabs = st.tabs(["Want to Read", "Reading", "Finished"])
status_map = {"Want to Read": "want_to_read", "Reading": "reading", "Finished": "finished"}

for i, tab_name in enumerate(["Want to Read", "Reading", "Finished"]):
    with tabs[i]:
        status_key = status_map[tab_name]
        books = reading_data.get(status_key, [])
        if not books:
            st.write("No books yet")
        for b in books:
            col1, col2 = st.columns([3, 1])
            col1.write(f"**{b.get('title')}** - {b.get('author','')}")
            if col2.button("Delete", key=f"del_{status_key}_{b.get('title')}"):
                delete_book(b.get('title'), status_key)
                st.rerun()
