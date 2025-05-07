# memory_core module

from datetime import datetime

# In-memory structure for now (could extend to file or DB)
memory = []

def log(type: str, context: str, content: str) -> dict:
    entry = {
        "type": type,
        "context": context,
        "content": content,
        "timestamp": datetime.utcnow().isoformat()
    }
    memory.append(entry)
    return {"message": "Logged successfully", "entry": entry}

def retrieve(filter_type: str = None, context: str = None) -> list:
    return [m for m in memory if (not filter_type or m['type'] == filter_type) and (not context or m['context'] == context)]

def clear(context: str = None) -> str:
    global memory
    if context:
        memory = [m for m in memory if m['context'] != context]
        return f"Cleared memory for context: {context}"
    memory = []
    return "Cleared all memory"

def run(payload: dict) -> dict:
    action = payload.get("action")
    if action == "log":
        return log(payload["type"], payload["context"], payload["content"])
    elif action == "retrieve":
        return {"results": retrieve(payload.get("type"), payload.get("context"))}
    elif action == "clear":
        return {"message": clear(payload.get("context"))}
    return {"error": "Unknown action"}