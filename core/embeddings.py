import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from config.settings import EMBEDDING_MODEL

@st.cache_resource
def load_embeddings(device):

    if device not in ["cuda", "cpu"]:
        device = "cpu"

    try:
        embeddings = HuggingFaceEmbeddings(
            model_name = EMBEDDING_MODEL,
            model_kwargs = {"device": device},
            encode_kwargs = {"normalize_embeddings": True}
        )
        return embeddings
    
    except Exception as e:
        raise RuntimeError(f"Failed to load embedding model: {e}")