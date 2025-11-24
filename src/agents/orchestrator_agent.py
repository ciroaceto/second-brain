from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from src.config import MODEL
from src.agents.research_agent import research
from src.agents.memory_agent import get_context, store_conversation, get_preferences
from src.guardrails.pii_sanitization import process_text
from src.observability.otel_setup import trace_function

# AnthropicModel automatically reads ANTHROPIC_API_KEY from environment
model = AnthropicModel(MODEL)

orchestrator = Agent(
    model,
    system_prompt="You coordinate agents to answer user queries. Use research agent for knowledge queries, memory agent for context.",
)

@trace_function
def process_query(query: str, user_id: str = "default") -> str:
    """Process user query through orchestrator."""
    # Sanitize input
    sanitized_query, _ = process_text(query)
    
    # Get memory context
    memory_context = get_context(user_id, sanitized_query)
    preferences = get_preferences(user_id)
    
    # Research
    research_result = research(sanitized_query)
    
    # Combine and respond
    prompt = f"""User query: {sanitized_query}

Memory context: {memory_context}
User preferences: {preferences}
Research result: {research_result}

Provide a comprehensive answer:"""
    
    result = orchestrator.run_sync(prompt)
    # Extract output from AgentRunResult
    if hasattr(result, 'output'):
        response_text = result.output
    elif hasattr(result, 'data'):
        response_text = str(result.data)
    else:
        response_text = str(result)
    
    # Store conversation
    store_conversation(user_id, [
        {"role": "user", "content": sanitized_query},
        {"role": "assistant", "content": response_text}
    ])
    
    # Sanitize output
    final_response, _ = process_text(response_text)
    return final_response

