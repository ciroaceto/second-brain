from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from src.config import MODEL
from src.rag.vector_store import search
from src.observability.otel_setup import trace_function

# AnthropicModel automatically reads ANTHROPIC_API_KEY from environment
model = AnthropicModel(MODEL)

research_agent = Agent(
    model,
    system_prompt="You are a research agent. Answer questions using the provided context. Cite sources.",
)

@trace_function
def research(query: str, n_results: int = 5) -> str:
    """Research query using RAG."""
    results = search(query, n_results)
    if not results:
        return "No relevant documents found."
    context = "\n\n".join([f"[{i+1}] {r['text']}" for i, r in enumerate(results)])
    
    prompt = f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer with citations:"
    result = research_agent.run_sync(prompt)
    # Extract output from AgentRunResult
    if hasattr(result, 'output'):
        return result.output
    elif hasattr(result, 'data'):
        return str(result.data)
    else:
        return str(result)

