

def rerank_docs(reranker, query, docs, top_k = 3):
    
    if not docs:
        return []
    
    pairs = [(query, doc.page_content) for doc in docs]

    try:
        scores = reranker.predict(pairs)
    
    except Exception:
        return docs[:top_k]
    
    scores = list(scores)

    reranked = sorted(
        zip(docs, scores),
        key = lambda x : x[1],
        reverse = True
    )

    docs_sorted = [doc for doc, _ in reranked]
    score_sorted = [score for _, score in reranked]

    max_score = max(score_sorted)
    min_score = min(score_sorted)

    threshold = max(
        min_score,
        max_score * 0.6
    )

    top_docs = [
        doc for doc, score in reranked
        if score >= threshold
    ]
    
    if not top_docs:
        top_docs = docs_sorted[:top_k]
    
    return top_docs[:top_k]