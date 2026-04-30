import streamlit as st

def render_chat():
    
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])