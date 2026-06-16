def detect_intent(query):
    q = query.lower()
    if any(word in q for word in ["summarize", "summary", "sum up", "tldr", "tl;dr"]):
        return "summary"
    elif any(word in q for word in ["explain", "how does", "why is", "describe"]):
        return "explain"
    elif any(word in q for word in ["define", "what is", "meaning of"]):
        return "definition"
    return "general"