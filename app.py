import streamlit as st
import requests
import json
import os
import google.generativeai as genai

st.set_page_config(page_title="Book Discovery Companion", page_icon="📚")

# Gemini setup from Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None

# Persistence
FILE = "reading_list.json"
if os.path.exists(FILE):
    with open(FILE) as f:
        reading_list = json.load(f)
else:
    reading_list = {"Want to Read": [], "Reading": [], "Finished": []}

st.title("📚 Book Discovery Companion")

query = st.text_input("Search books (Open Library)", placeholder="e.g. Atomic Habits")

if query:
    res = requests.get(f"https://openlibrary.org/search.json?q={query}&limit=10").json()
    for doc in res.get("docs", [])[:10]:
        title = doc.get("title", "No title")
        author = ", ".join(doc.get("author_name", [])[:2])
        year = doc.get("first_publish_year", "")
        
        with st.expander(f"{title} - {author} ({year})"):
            st.write(f"**Author:** {author}")
            
            if st.button(f"✨ AI Summary for {title}", key=title):
                if not model:
                    st.error("Add GEMINI_API_KEY in Streamlit Secrets")
                else:
                    with st.spinner("Gemini thinking..."):
                        prompt = f"Summarize book '{title}' by {author}. Give: 1) Short summary 2) Reading level 3) 3 discussion questions"
                        r = model.generate_content(prompt)
                        st.markdown(r.text)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Want to Read", key=f"want_{title}"):
                    reading_list["Want to Read"].append(title)
                    with open(FILE, "w") as f: json.dump(reading_list, f)
                    st.success("Added!")
            with col2:
                if st.button("Reading", key=f"read_{title}"):
                    reading_list["Reading"].append(title)
                    with open(FILE, "w") as f: json.dump(reading_list, f)
                    st.success("Added!")
            with col3:
                if st.button("Finished", key=f"fin_{title}"):
                    reading_list["Finished"].append(title)
                    with open(FILE, "w") as f: json.dump(reading_list, f)
                    st.success("Added!")

st.divider()
st.subheader("My Reading List")
st.json(reading_list)
