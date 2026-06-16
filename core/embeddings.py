import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from config.settings import EMBEDDING_MODEL

@st.cache_resource
def init_and_load_embeddings(device):
    # removed device check from here
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name = EMBEDDING_MODEL,
            # for safety, keep trust_remote_code false
            model_kwargs = {"device": device,
                            "trust_remote_code": False},
            encode_kwargs = {"normalize_embeddings": True}
        )
        # test a testing string to spot failures
        _ = embeddings.embed_query("test me")
        return embeddings
    
    except Exception as e:
        # here fallback to cpu if cuda out of mem
        # handles large chunking memory failures and syystem crashes
        if device == "cuda" and "CUDA out of memory" in str(e):
            st.warning("CUDA out of memory, Fallback to CPU")
            return init_and_load_embeddings("cpu")
        # if cpu fails too
        raise RuntimeError(f"Failed to load embedding model: {e}")