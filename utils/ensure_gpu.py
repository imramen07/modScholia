# major changes
# removed streamlit alterations
# check cuda availability via torch instead

import torch
import faiss

def ensure_gpu(db):
    # no cuda
    if not torch.cuda.is_available():
        return db
    # has cuda
    #check index
    if hasattr(db, "index") and db.index is not None:
        if not isinstance(db.index, faiss.GpuIndex):
            try:
                res = faiss.StandardGpuResources()
                db.index = faiss.index_cpu_to_gpu(res, 0, db.index)
                #print(f"Done cpu to gpu")
            except Exception as e:
                print(f"GPU move failed: {e}")
    return db