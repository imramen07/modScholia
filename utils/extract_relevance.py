import re

# splitting moved in function
#def split_sentences(text):
    #return re.split(r'(?<=[.!?])\s+', text)

def extract_relevant_sentences(docs, query, max_sen_per_doc = 3):
    
    # breaks flow of sentences. need fix
    #STOPWORDS = {
        #"what", "is", "the", "a", "an", "of", "in", "on", "for", "to",
        #"and", "or", "by", "with", "how", "define"
    #}

    #query_words = set(
        #w for w in query.lower().split()
        #if w not in STOPWORDS
    #)

    query_words = set(query.lower().split())
    context = []
    source = []

    for doc in docs:
        source_n = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", 0)
        sentences = re.split(r'(?<=[.!?])\s+', doc.page_content)
        relevant_sen = []

        for s in sentences:
            s_low = s.lower()
            if any(word in s_low for word in query_words):
                relevant_sen.append(s.strip())
                # handle overflow here
                if len(relevant_sen) >= max_sen_per_doc:
                    break
        if relevant_sen:
            context.append(f"[{source} - Page {page}]\n" + "\n".join(relevant_sen))
            source_n.append((source, page))

    if not context:
        # trigger fallback to doc 1 init 500 char
        f_doc = docs[0]
        context.append(f_doc.page_content[:500])
        source_n.append((f_doc.metadata.get("source", "Unknown"),
                         f_doc.metadata.get("page", 0)))
        
        return "\n\n".join(context), source_n