from langchain_community.vectorstores import faiss

def use_gpu(db):
    try:
        res = faiss.StandardGpuResources()
        db.index = faiss.index_cpu_to_gpu(res, 0, db.index)
    
    except Exception:
        pass

    return db

def use_cpu(db):
    try:
        db.index = faiss.index_gpu_to_cpu(db.index)

    except Exception:
        pass

    return db;