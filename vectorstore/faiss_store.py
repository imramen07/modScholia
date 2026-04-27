from langchain_community.vectorstores import FAISS
import os

def create_index(chunks, embeddings, index_dir):
    db = FAISS.from_documents(chunks, embeddings)
    os.makedirs(index_dir, exist_ok = True)
    db.save_local(index_dir)
    return db

def load_index(embeddings, index_dir):
    return FAISS.load_local(
        index_dir,
        embeddings,
        allow_dangerous_deserialization = True
    )