from config.settings import THRESHOLD_RERANK

def rerank_docs(reranker, query, docs, top_k = 3):
    
    # better fallback , instead of empty response
    if not docs or reranker is None:
        return docs[:top_k]
    
    pairs = [(query, doc.page_content) for doc in docs]

    try:
        # add - batch size
        scores = reranker.predict(pairs, batsize = 32)
    
    except Exception:
        return docs[:top_k]
    
    scores = list(scores)

    reranked = sorted(
        zip(docs, scores),
        key = lambda x : x[1],
        reverse = True
    )

    docs_sort = [doc for doc, _ in reranked]
    maxScore = max(score_sort)
    score_sort = [score for _, score in reranked]
    minScore = min(score_sort)

    threshold = max(
        minScore,
        maxScore * THRESHOLD_RERANK
    )

    # use threshold to filter docs
    top_docs = [
        doc for doc, score in reranked
        if score >= threshold
    ]
    
    # fallback - empty topdocs
    # push all sorted docs
    if not top_docs:
        top_docs = docs_sort[:top_k]
    
    return top_docs[:top_k]