import spacy
import re

try:
    nlp = spacy.load("en_core_web_lg")
except OSError:
    nlp = None

PII_PATTERNS = {
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
    "credit_card": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
}

def detect_pii(text: str) -> list[dict]:
    """Detect PII using spaCy NER and regex."""
    entities = []
    
    # Regex patterns
    for pii_type, pattern in PII_PATTERNS.items():
        for match in re.finditer(pattern, text):
            entities.append({
                "type": pii_type,
                "text": match.group(),
                "start": match.start(),
                "end": match.end(),
                "confidence": 0.9
            })
    
    # spaCy NER
    if nlp:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "ORG", "GPE", "DATE"]:
                entities.append({
                    "type": ent.label_.lower(),
                    "text": ent.text,
                    "start": ent.start_char,
                    "end": ent.end_char,
                    "confidence": 0.85
                })
    
    return entities

def sanitize(text: str, entities: list[dict] = None) -> str:
    """Remove/replace PII."""
    if entities is None:
        entities = detect_pii(text)
    
    result = text
    for entity in sorted(entities, key=lambda x: x["start"], reverse=True):
        result = result[:entity["start"]] + f"[{entity['type'].upper()}]" + result[entity["end"]:]
    
    return result

