import re

def split_sentences(text):
    
    return re.split(r'(?<=[.!?])\s+', text)

def extract_relevant_sentences(docs, query, max_sentences = 5):
    STOPWORDS = {
        "what", "is", "the", "a", "an", "of", "in", "on", "for", "to",
        "and", "or", "by", "with", "how", "define"
    }

    query_words = set(
        w for w in query.lower().split()
        if w not in STOPWORDS
    )

    scored_sentences = []

    for doc in docs:
        sentences = split_sentences(doc.page_content)

        for s in sentences:
            s_clean = s.strip()
            if len(s_clean) < 25:
                continue

            words = set(s_clean.lower().split())

            overlap = len(query_words.intersection(words))

            if overlap == 0:
                continue

            score = overlap / (len(query_words) + 1)

            scored_sentences.append((
                score,
                s_clean,
                doc.metadata.get("page", 0) + 1,
                doc.metadata.get("source", "Unknown")
            ))
        
        scored_sentences.sort(
            reverse = True,
            key = lambda x: x[0]
        )

        selected = scored_sentences[:max_sentences]

        context = ""
        pages_used = set()

        for _, sent, page, source in selected:
            context += f"[{source} - Page {page}] {sent}\n"
            pages_used.add((source, page))
        
        return context.strip(), sorted(pages_used)