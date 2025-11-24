import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
VECTOR_DB_DIR = DATA_DIR / "vector_db"
MEM0_DIR = DATA_DIR / "mem0_data"
DOCUMENTS_DIR = DATA_DIR / "documents"

# API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError(
        "ANTHROPIC_API_KEY environment variable is not set. "
        "Please set it using: export ANTHROPIC_API_KEY='your-api-key'"
    )

MODEL = "claude-sonnet-4-5"

# Create directories
for d in [DATA_DIR, VECTOR_DB_DIR, MEM0_DIR, DOCUMENTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

