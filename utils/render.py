# todo - fastapi
import streamlit as st

def initandrender_chat():
    
    for msg in st.session_state.get("messages", []):
        with st.chat_message(msg["role"]):
            st.write(msg["content"])