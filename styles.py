import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Title color */
    h1 {
        color: #2c3e50;
        text-align: center;
        font-family: 'Georgia', serif;
    }
    
    /* Book cards */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        padding: 10px;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 20px;
        border: none;
        background-color: #4a4a8c;
        color: white;
    }
    .stButton > button:hover {
        background-color: #6c6cb0;
        color: white;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #2c3e50;
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
