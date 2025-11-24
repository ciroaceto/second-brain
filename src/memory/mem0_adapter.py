from mem0 import Memory
from mem0.llms.anthropic import AnthropicLLM
from src.config import MEM0_DIR, ANTHROPIC_API_KEY, MODEL
from src.observability.otel_setup import trace_function

# Monkey-patch Mem0's Anthropic integration to fix Claude Sonnet 4.5 parameter conflict
# Claude Sonnet 4.5 doesn't allow both temperature and top_p to be set
original_get_common_params = AnthropicLLM._get_common_params

def _patched_get_common_params(self, **kwargs):
    """Override to only use temperature, not top_p (Claude Sonnet 4.5 requirement)"""
    params = {
        "temperature": self.config.temperature,
        "max_tokens": self.config.max_tokens,
        # Remove top_p to avoid conflict with Claude Sonnet 4.5
    }
    params.update(kwargs)
    return params

AnthropicLLM._get_common_params = _patched_get_common_params

# Note: Anthropic doesn't provide embedding models, only LLMs (Claude)
# Using HuggingFace for embeddings (local, free, no API key needed)
memory = Memory.from_config({
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "mem0",
            "path": str(MEM0_DIR),
        }
    },
    "llm": {
        "provider": "anthropic",
        "config": {
            "model": MODEL,
            "api_key": ANTHROPIC_API_KEY,
        }
    },
    "version": "v1.1",
    "embedder": {
        "provider": "huggingface",
        "config": {
            # Fast, lightweight model for embeddings
            "model": "sentence-transformers/all-MiniLM-L6-v2",
        }
    }
})

@trace_function
def add_memory(user_id: str, messages: list[dict]):
    """Add conversation to memory."""
    for msg in messages:
        memory.add(msg.get("content", ""), user_id=user_id)

@trace_function
def search_memory(user_id: str, query: str, limit: int = 5) -> list[dict]:
    """Search memory for relevant context."""
    results = memory.search(query, user_id=user_id, limit=limit)
    # Mem0 returns dict with 'results' key containing list of memories
    if isinstance(results, dict) and 'results' in results:
        return results['results']
    return results if isinstance(results, list) else []

@trace_function
def get_all_memories(user_id: str) -> list[dict]:
    """Get all memories for a user."""
    results = memory.get_all(user_id=user_id)
    # Mem0 returns dict with 'results' key containing list of memories
    if isinstance(results, dict) and 'results' in results:
        return results['results']
    return results if isinstance(results, list) else []

