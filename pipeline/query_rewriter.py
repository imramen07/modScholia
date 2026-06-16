import re
from pipeline.intent import detect_intent

# slightly enhances query, use this afterwards
def better_query(query: str) -> str:
    
    return re.sub(r"\s+", " ", query).strip().lower()

def rewrite_query(query):
    
    q = better_query(query)
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
    final = list(dict.fromkeys(expansions))
    return q, final