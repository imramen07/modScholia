def deduplicate_docs(docs):
    seen = set()
    unique_docs = []

    for doc in docs:
        text = doc.page_content.strip()
        if text not in seen:
            seen.add(text)
            unique_docs.append(doc)
    return unique_docs