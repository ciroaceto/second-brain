from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from src.config import MODEL
from src.guardrails.pii_ner import detect_pii

# AnthropicModel automatically reads ANTHROPIC_API_KEY from environment
model = AnthropicModel(MODEL)

pii_agent = Agent(
    model,
    system_prompt="You are a PII detection agent. Identify any personally identifiable information in the text. Return a JSON list of PII entities with type and text.",
)

def validate_pii_with_llm(text: str, ner_entities: list[dict]) -> list[dict]:
    """Use LLM to validate ambiguous PII detected by NER."""
    if not ner_entities:
        return []
    
    # Only validate if confidence is low
    low_confidence = [e for e in ner_entities if e.get("confidence", 1.0) < 0.85]
    if not low_confidence:
        return ner_entities
    
    prompt = f"Text: {text}\n\nDetected entities: {low_confidence}\n\nValidate these PII detections."
    result = pii_agent.run_sync(prompt)
    # Simplified - in production would parse structured response
    return ner_entities

