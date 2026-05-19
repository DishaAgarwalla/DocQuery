from sentence_transformers import SentenceTransformer

print("Loading embedding model...")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

print("Embedding model loaded.")

def create_embeddings(chunks):
    """Create embeddings for text chunks"""
    if not chunks:
        return []
    
    # Clean chunks before embedding (remove page markers)
    cleaned_chunks = []
    for chunk in chunks:
        import re
        cleaned = re.sub(r'\[PAGE_\d+_OF_[^\]]+\]\n?', '', chunk)
        cleaned_chunks.append(cleaned)
    
    embeddings = model.encode(
        cleaned_chunks,
        show_progress_bar=True,
        convert_to_numpy=True
    )
    
    return embeddings