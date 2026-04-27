def build_chat_context(messages, limit = 3):
    history = ""
    for msg in messages[-limit:]:
        role = msg["role"]
        content = msg["content"]
        history += f"{role.upper()}: {content}\n"
    return history