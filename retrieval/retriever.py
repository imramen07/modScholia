from config.settings import TOP_K, FETCH_K
from pipeline.query_rewriter import better_query

def retrieve_docs(db, query):
    
    query = better_query(query)

    try:
        # prioritize mmr
        docs = db.max_marginal_relevance_search(
            query,
            k = TOP_K,
            fetch_k = FETCH_K
        )

        # sim search if mmr fails
        if not docs:
            docs = db.similarity_search(query, k = TOP_K)
        
        return docs
    
    except Exception:
        return []