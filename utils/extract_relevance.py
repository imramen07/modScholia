def extract_relevant_sentences(docs, query, max_sentences = 5):
    STOPWORDS = {
        "what", "is", "the", "a", "an", "of", "in", "on", "for", "to",
        "and", "or", "by", "with", "how"
    }

    query_words = set(
        word for word in query.lower().split()
        if word not in STOPWORDS
    )

    selected = []

    for doc in docs:
        sentences = doc.page_content.split(".")

        for s in sentences:
            s = s.strip()
            if len(s) < 20:
                continue

            sentence_words = set(s.lower().split())
            common_words = query_words.intersection(sentence_words)

            if len(common_words) >= 2:
                selected.append((
                    s,
                    doc.metadata.get("page", 0) + 1,
                    doc.metadata.get("source", "Unknown")
                ))
            
            if len(selected) >= max_sentences:
                break
        if len(selected) >= max_sentences:
            break
    
    context = ""
    pages_used = set()

    for sent, page, source in selected:
        context += f"[{source} - Page {page}] {sent}.\n"
        pages_used.add((source, page))
    
    return context, sorted(pages_used, key = lambda x: (x[0], x[1]))