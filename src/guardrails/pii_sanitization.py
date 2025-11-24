from src.guardrails.pii_ner import detect_pii, sanitize
from src.guardrails.pii_agent import validate_pii_with_llm
from src.observability.otel_setup import trace_function

@trace_function
def process_text(text: str, use_llm: bool = False) -> tuple[str, list[dict]]:
    """Process text through guardrails - returns sanitized text and detected entities."""
    entities = detect_pii(text)
    
    if use_llm and entities:
        entities = validate_pii_with_llm(text, entities)
    
    sanitized = sanitize(text, entities)
    return sanitized, entities

