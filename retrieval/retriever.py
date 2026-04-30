import re
from config.settings import TOP_K, FETCH_K

def clean_query(query: str):
    return re.sub(r"\s+", " ", query).strip().lower()

def retrieve_docs(db, query):
    
    query = clean_query(query)

    try:
        docs = db.max_marginal_relevance_search(
            query,
            k = TOP_K,
            fetch_k = FETCH_K
        )

        if not docs:
            docs = db.similarity_search(query, k = TOP_K)
        
        return docs
    
    except Exception:
        return []