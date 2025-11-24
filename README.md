# Second Brain

Multi-agent second brain system with RAG, memory, and PII guardrails.

## Setup

1. Install [uv](https://github.com/astral-sh/uv):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Install dependencies:
```bash
uv sync
uv run python -m spacy download en_core_web_lg
```

3. Set environment variable:
```bash
export ANTHROPIC_API_KEY=your_key
```

## Development

Run commands with `uv run`:
```bash
uv run python main.py ingest file.pdf
uv run python main.py query "question"
```

Or activate the virtual environment:
```bash
source .venv/bin/activate  # uv creates .venv automatically
python main.py ingest file.pdf
```

## Observability Setup

Set up Jaeger for trace visualization:

```bash
./setup_observability.sh
```

This will:
- Start Jaeger container with Docker
- Expose Jaeger UI at http://localhost:16686
- Configure OTLP endpoints for trace collection

## Usage

```bash
# Ingest a document (PDF or text)
uv run python main.py ingest path/to/file.pdf
uv run python main.py ingest path/to/file.txt

# Query
uv run python main.py query "What is in my documents?"

# Interactive chat
uv run python main.py chat

# View memory
uv run python main.py memory

# Run evaluations
uv run python main.py eval

# View metrics
uv run python main.py metrics
```

Or if virtual environment is activated:
```bash
python main.py ingest path/to/file.pdf
python main.py query "What is in my documents?"
```
