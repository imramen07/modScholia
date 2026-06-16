def build_chat_context(messages, limit = 3, maxchar = 2000):
    history = ""
    for msg in messages[-limit:]:
        role = msg["role"]
        content = msg["content"]
        history += f"{role.upper()}: {content}\n"
    # add - token limit, truncate after maxchar
    # watchout for context loss
    # todo - dynamic maxchar alteration
    if len(history) > maxchar:
        history = history[:maxchar] + "...(truncated)"
    return history