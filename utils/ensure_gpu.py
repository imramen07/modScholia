from config.settings import device
from utils.cuda import use_gpu_once
import streamlit as st

def ensure_gpu(db):

    if device == "cuda" and not st.session_state.get("gpu_loaded", False):
        db = use_gpu_once(db)
        st.session_state.gpu_loaded = True
    
    return db