import streamlit as st, requests, json, os
from google import genai

st.set_page_config(page_title="Book Discovery Companion", page_icon="📚")

# New SDK that works with AQ.. keys
api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else None
client = genai.Client(api_key=api_key) if api_key else None

FILE="reading_list.json"
reading_list=json.load(open(FILE)) if os.path.exists(FILE) else {"Want to Read":[],"Reading":[],"Finished":[]}

st.title("📚 Book Discovery Companion")
query=st.text_input("Search books (Open Library)", placeholder="e.g. Atomic Habits")

if query:
    res=requests.get(f"https://openlibrary.org/search.json?q={query}&limit=10").json()
    for doc in res.get("docs",[])[:10]:
        title=doc.get("title","No title")
        author=", ".join(doc.get("author_name",[])[:2])
        year=doc.get("first_publish_year","")
        with st.expander(f"{title} - {author} ({year})"):
            if st.button(f"✨ AI Summary: {title}", key=title):
                if not client:
                    st.error("Add GEMINI_API_KEY in Secrets")
                else:
                    with st.spinner("Gemini thinking..."):
                        r=client.models.generate_content(model="gemini-2.0-flash", contents=f"Summarize book '{title}' by {author}. Give: 1) Short summary 2) Reading level 3) 3 discussion questions")
                        st.markdown(r.text)
            c1,c2,c3=st.columns(3)
            if c1.button("Want", key=f"w{title}"):
                reading_list["Want to Read"].append(title)
                json.dump(reading_list, open(FILE,"w"))
                st.success("Added!")
            if c2.button("Reading", key=f"r{title}"):
                reading_list["Reading"].append(title)
                json.dump(reading_list, open(FILE,"w"))
                st.success("Added!")
            if c3.button("Done", key=f"d{title}"):
                reading_list["Finished"].append(title)
                json.dump(reading_list, open(FILE,"w"))
                st.success("Added!")

st.divider()
st.subheader("My Reading List")
st.json(reading_list)
