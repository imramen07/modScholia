import tempfile
import os
from langchain_community.document_loaders import PyPDFLoader
from utils.hashing import hash_bytes

def load_pdf(name, data):

    file_hash = hash_bytes(data)

    with tempfile.NamedTemporaryFile(delete = False, suffix = ".pdf") as tmp:
        tmp.write(data)
        tmp_path = tmp.name

    try:
        loader = PyPDFLoader(tmp_path)
        pages = loader.load()

    finally:
        os.remove(tmp_path)

    for p in pages:
        p.metadata["source"] = name
        p.metadata["file_hash"] = file_hash

    return pages