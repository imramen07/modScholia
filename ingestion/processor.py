from ingestion.loader import load_pdf
from ingestion.splitter import split_docs

def process_files(file_data):
    all_pages = []
    for name, data in file_data:
        pages = load_pdf(name, data)
        all_pages.extend(pages)

    chunks = split_docs(all_pages)
    return all_pages, chunks