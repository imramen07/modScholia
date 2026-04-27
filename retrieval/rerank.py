

def rerank_docs(reranker, query, docs):
    if not docs:
        return []
    pairs = [(query, doc.page_content) for doc in docs]

    if all(len(doc.page_content) < 200 for doc in docs):
        scores = [1.0] * len(docs)
    else:
        scores = reranker.predict(pairs)

    reranked = sorted(
        zip(docs, scores),
        key = lambda x : x[1],
        reverse = True
    )
    if not scores:
        return docs[:3]
    
    elif max(scores < 0.2):
        return docs[:3]
    
    threshold = max(0.2, max(scores) * 0.5)

    top_docs = [doc for doc, score in reranked if score >= threshold][:3]

    if not top_docs:
        return [doc for doc, _ in reranked[:2]]

    return top_docs
    