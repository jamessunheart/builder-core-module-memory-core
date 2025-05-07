# memory_core with local snapshot endpoint

from datetime import datetime

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

def snapshot(_: str = None) -> dict:
    return {
        "count": len(memory),
        "types": sorted(set(m['type'] for m in memory)),
        "contexts": sorted(set(m['context'] for m in memory)),
        "sample": memory[0] if memory else {}
    }

def run(payload: dict) -> dict:
    action = payload.get("action")
    if action == "log":
        return log(payload["type"], payload["context"], payload["content"])
    elif action == "retrieve":
        return {"results": retrieve(payload.get("type"), payload.get("context"))}
    elif action == "clear":
        return {"message": clear(payload.get("context"))}
    elif action == "snapshot":
        return snapshot()
    return {"error": "Unknown action"}