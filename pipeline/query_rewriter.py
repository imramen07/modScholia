import re
from pipeline.intent import detect_intent

def clean_query(query: str) -> str:
    
    return re.sub(r"\s+", " ", query).strip().lower()

def rewrite_query(query: str):
    
    q = clean_query(query)
    intent = detect_intent(q)

    expansions = []

    #intent based
    if intent == "definition":
        expansions.append(f"{q} definition meaning explanation concept")

    elif intent == "summary":
        expansions.append(f"{q} summary overview key points")

    elif intent == "explain":
        expansions.append(f"{q} detailed explanation working principle how it works")

    else:
        expansions.append(q)

    #general
    if len(q.split()) <= 3:
        expansions.append(f"{q} explanation details information")

    #remove dupes
    seen = set()
    final_queries = []
    for e in expansions:
        if e not in seen:
            seen.add(e)
            final_queries.append(e)

    return q, final_queries