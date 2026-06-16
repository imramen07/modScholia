import tempfile
import os
from langchain_community.document_loaders import PyPDFLoader
from utils.hashing import hash_bytes

def pdf_loader(name, data):
    # validate header first
    if not data.startswith(b'%PDF'):
        raise ValueError(f"File {name} is not valid PDF")

    #proceed hashing
    file_hash = hash_bytes(data)
    with tempfile.NamedTemporaryFile(delete = False, suffix = ".pdf") as tmp:
        tmp.write(data)
        tmp_path = tmp.name

    try:
        loader = PyPDFLoader(tmp_path)
        pages = loader.load()

    finally:
        # error prone
        os.remove(tmp_path)

    # add - page number counter
    for i, p in enumerate(pages, start = 1):
        p.metadata["source"] = name
        p.metadata["file_hash"] = file_hash
        p.metadata["page"] = i

    return pages