from langchain_community.vectorstores import faiss

def use_gpu_once(db):

    try:
        if hasattr(db, "gpu_moved") and db._gpu_moved:
            return db

        res = faiss.StandardGpuResources()
        db.index = faiss.index_cpu_to_gpu(res, 0, db.index)
    
        db._gpu_moved = True

    except Exception as e:
        print(f"GPU conversion failed: {e}")

    return db