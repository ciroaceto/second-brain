import chromadb
from chromadb.config import Settings
from src.config import VECTOR_DB_DIR
from src.rag.chunking import semantic_chunk
from src.observability.otel_setup import trace_function

client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR), settings=Settings(anonymized_telemetry=False))
collection = client.get_or_create_collection("documents")

@trace_function
def add_document(text: str, metadata: dict = None):
    """Add document to vector store."""
    chunks = semantic_chunk(text)
    ids = []
    documents = []
    metadatas = []
    
    for i, chunk in enumerate(chunks):
        chunk_id = f"{metadata.get('doc_id', 'doc')}_{i}"
        ids.append(chunk_id)
        documents.append(chunk)
        metadatas.append({**(metadata or {}), "chunk_id": i})
    
    collection.add(ids=ids, documents=documents, metadatas=metadatas)

@trace_function
def search(query: str, n_results: int = 5) -> list[dict]:
    """Search for similar documents."""
    results = collection.query(query_texts=[query], n_results=n_results)
    
    return [
        {"text": doc, "metadata": meta}
        for doc, meta in zip(results["documents"][0], results["metadatas"][0])
    ]

