from langchain_community.vectorstores import FAISS
import os

def create_index(chunks, embeddings, index_dir):
    
    db = FAISS.from_documents(chunks, embeddings)
    os.makedirs(index_dir, exist_ok = True)
    db.save_local(index_dir)

    return db

def load_index(embeddings, index_dir):
    
    if not os.path.exists(index_dir):
        return None
    
    try:
        db = FAISS.load_local(
            index_dir,
            embeddings,
            allow_dangerous_deserialization = False
        )

        if not hasattr(db, "index") or db.index is None:
            raise ValueError("Corrupted FAISS index")

        return db
    
    except Exception:
        return None