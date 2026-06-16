def deduplicate_docs(docs):
    seencont = set()
    unique = []

    for doc in docs:
        # add - use content, source and page as info"
        info = (doc.page_content, doc.metadata.get("source", ""), doc.metadata.get("page", 0))
        if info not in seencont:
            seencont.add(info)
            unique.append(doc)

        # use if source fails
        #text = doc.page_content.strip()
        #if text not in seencont:
            #seencont.add(text)
            #unique.append(doc)
    return unique