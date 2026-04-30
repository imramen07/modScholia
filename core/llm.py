import streamlit as st
from langchain_ollama import OllamaLLM
from config.settings import LLM_MODEL

@st.cache_resource
def load_llm():
    
    try:
        llm = OllamaLLM(
            model = LLM_MODEL,
            num_ctx = 4096,
            temperature = 0.0,
            top_p = 0.9,
            streaming = True
        )
        return llm
    
    except Exception as e:
        raise RuntimeError(f"LLM failed to load: {e}")