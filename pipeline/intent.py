def detect_intent(query):
    q = query.lower()
    if "summarize" in q:
        return "summary"
    elif "explain" in q:
        return "explain"
    elif "define" in q or "what is" in q:
        return "definition"
    return "general"