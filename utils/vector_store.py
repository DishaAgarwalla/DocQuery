import faiss
import numpy as np
import pickle
import os

def clean_doc_name(doc_name):
    """Remove path prefix from document name"""
    if doc_name:
        return os.path.basename(doc_name)
    return "Unknown"

def create_vector_store(embeddings):
    """Create FAISS vector store from embeddings"""
    if len(embeddings) == 0:
        raise ValueError("No embeddings provided")
    
    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    
    embeddings_array = np.array(embeddings).astype("float32")
    index.add(embeddings_array)
    
    print(f"Vector store created. Dimension: {dimension}, Vectors: {index.ntotal}")
    
    return index

def search_vector_store(index, query_embedding, k=5):
    """Search for top K similar vectors"""
    if index.ntotal == 0:
        raise ValueError("Vector store is empty")
    
    query_embedding = np.array([query_embedding]).astype("float32")
    distances, indices = index.search(query_embedding, min(k, index.ntotal))
    
    return indices, distances

def save_vector_store(index, chunks, metadata, filepath="utils/vector_store/"):
    """Save FAISS index, chunks, and metadata to disk"""
    os.makedirs(filepath, exist_ok=True)
    
    # Clean metadata document names
    if metadata:
        for item in metadata:
            if 'document' in item:
                item['document'] = clean_doc_name(item['document'])
    
    # Save FAISS index
    faiss.write_index(index, os.path.join(filepath, "index.faiss"))
    
    # Save chunks
    with open(os.path.join(filepath, "chunks.pkl"), "wb") as f:
        pickle.dump(chunks, f)
    
    # Save metadata
    with open(os.path.join(filepath, "metadata.pkl"), "wb") as f:
        pickle.dump(metadata, f)
    
    print(f"Vector store saved to {filepath}")

def load_vector_store(filepath="utils/vector_store/"):
    """Load FAISS index, chunks, and metadata from disk"""
    index_path = os.path.join(filepath, "index.faiss")
    chunks_path = os.path.join(filepath, "chunks.pkl")
    metadata_path = os.path.join(filepath, "metadata.pkl")
    
    if not os.path.exists(index_path) or not os.path.exists(chunks_path):
        return None, None, None
    
    index = faiss.read_index(index_path)
    
    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)
    
    metadata = None
    if os.path.exists(metadata_path):
        with open(metadata_path, "rb") as f:
            metadata = pickle.load(f)
            # Clean document names in loaded metadata
            for item in metadata:
                if 'document' in item:
                    item['document'] = clean_doc_name(item['document'])
    
    print(f"Vector store loaded. Vectors: {index.ntotal}")
    
    return index, chunks, metadata