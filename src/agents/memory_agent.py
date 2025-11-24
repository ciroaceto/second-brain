from src.memory.mem0_adapter import add_memory, search_memory, get_all_memories
from src.observability.otel_setup import trace_function

@trace_function
def store_conversation(user_id: str, messages: list[dict]):
    """Store conversation in memory."""
    add_memory(user_id, messages)

@trace_function
def get_context(user_id: str, query: str) -> str:
    """Get relevant context from memory."""
    memories = search_memory(user_id, query)
    if not memories:
        return ""
    
    # Handle both string and dict responses from Mem0
    context_items = []
    for m in memories:
        if isinstance(m, dict):
            context_items.append(m.get("memory", "") or m.get("text", "") or str(m))
        elif isinstance(m, str):
            context_items.append(m)
        else:
            context_items.append(str(m))
    
    return "\n".join(context_items)

@trace_function
def get_preferences(user_id: str) -> dict:
    """Get user preferences from memory."""
    all_memories = get_all_memories(user_id)
    if not all_memories:
        return {"preferences": []}
    
    # Handle both string and dict responses from Mem0
    preferences = []
    for m in all_memories[:5]:
        if isinstance(m, dict):
            preferences.append(m.get("memory", "") or m.get("text", "") or str(m))
        elif isinstance(m, str):
            preferences.append(m)
        else:
            preferences.append(str(m))
    
    return {"preferences": preferences}

