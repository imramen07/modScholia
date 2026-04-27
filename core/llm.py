import streamlit as st
from langchain_ollama import OllamaLLM
from config.settings import LLM_MODEL

@st.cache_resource
def load_llm():
    return OllamaLLM(
        model = LLM_MODEL,
        num_ctx = 4096,
        temperature = 0.0
    )