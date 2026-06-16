import streamlit as st
from sentence_transformers import CrossEncoder
from config.settings import RERANK_MODEL

@st.cache_resource
def load_reranker(device):
    # add - try-except
    try:
        model = CrossEncoder(
            RERANK_MODEL,
            device = device,
            trust_remote_code = False
        )
        return model
    except Exception as e:
        st.warning(f"Reranker not available: {e}")
        return None