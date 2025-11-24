def semantic_chunk(text: str, max_chunk_size: int = 1000) -> list[str]:
    """Simple semantic chunking - split on sentences, respect max size."""
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = []
    current_size = 0
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        size = len(sentence)
        if current_size + size > max_chunk_size and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_size = size
        else:
            current_chunk.append(sentence)
            current_size += size
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

