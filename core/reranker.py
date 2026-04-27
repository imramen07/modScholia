import streamlit as st
from sentence_transformers import CrossEncoder
from config.settings import RERANK_MODEL

@st.cache_resource
def load_reranker(device):
    return CrossEncoder(
        RERANK_MODEL,
        device = device
    )