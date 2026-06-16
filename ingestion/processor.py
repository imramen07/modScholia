import streamlit as st
from ingestion.loader import pdf_loader
from ingestion.splitter import split_docs

def process_files(file_data):
    all_pages = []
    # add - loading bar
    loadingbar = st.progress(0, text = "Loading PDFs...")

    # iterate index (i) for loadingbar
    for i, (name, data) in enumerate(file_data):
        pages = pdf_loader(name, data)
        all_pages.extend(pages)
        loadingbar.progress((i+1)/len(file_data))
    loadingbar.empty()

    # set spinner for chunk splitting
    with st.spinner("Splitting into chunks..."):
        chunks = split_docs(all_pages)
    return all_pages, chunks