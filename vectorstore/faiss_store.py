from langchain_community.vectorstores import FAISS
import os

def create_index(chunks, embeddings, index_dir):
    
    # init db, mkdirs and save db
    db = FAISS.from_documents(chunks, embeddings)
    os.makedirs(index_dir, exist_ok = True)
    db.save_local(index_dir)

    return db

def load_index(embeddings, index_dir):
    
    # handle no dir first
    if not os.path.exists(index_dir):
        return None
    
    # then use it
    try:
        db = FAISS.load_local(
            index_dir,
            embeddings,
            # secure
            allow_dangerous_deserialization = False
        )
        # validate exist index
        if not hasattr(db, "index") or db.index is None:
            raise ValueError("Corrupted FAISS index")

        return db
    
    except Exception as e:
        print(f"Error loading index: {e}")
        return None