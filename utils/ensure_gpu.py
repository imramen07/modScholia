import config
import cuda
import streamlit as st

def ensure_gpu(db):

    if config.device == "cuda" and not st.session_state.get("gpu_loaded", False):
        db = cuda.use_gpu_once(db)
        st.session_state.gpu_loaded = True
    
    return db