from config.settings import TOP_K, FETCH_K

def retrieve_docs(db, query):
    return db.max_marginal_relevance_search(
        query, k = TOP_K, fetch_k = FETCH_K
    )