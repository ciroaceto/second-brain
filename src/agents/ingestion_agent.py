from pathlib import Path
from src.rag.vector_store import add_document
from src.guardrails.pii_sanitization import process_text
from src.ingestion.parsers import parse_file
from src.observability.otel_setup import trace_function

@trace_function
def ingest_file(file_path: str, user_id: str = "default"):
    """Ingest a file (PDF or text) into the system."""
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Parse based on file type
    text = parse_file(file_path)
    
    # Sanitize PII before storage
    sanitized, entities = process_text(text, use_llm=False)
    
    metadata = {
        "doc_id": path.stem,
        "file_path": str(path),
        "file_type": path.suffix.lower(),
        "user_id": user_id,
        "pii_detected": len(entities) > 0,
    }
    
    add_document(sanitized, metadata)
    return {"status": "ingested", "pii_entities": len(entities), "file_type": metadata["file_type"]}

