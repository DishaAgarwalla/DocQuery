"""
Handles tracking page numbers and metadata for each text chunk
"""

class MetadataHandler:
    """Stores and manages page number information for document chunks"""
    
    def __init__(self):
        self.chunk_metadata = []  # List of dicts: {'page': page_num, 'doc': doc_name}
    
    def add_metadata(self, page_num, doc_name, chunk_index):
        """Add metadata for a chunk"""
        self.chunk_metadata.append({
            'page': page_num,
            'document': doc_name,
            'chunk_index': chunk_index
        })
    
    def get_metadata(self, chunk_index):
        """Get metadata for a specific chunk"""
        if chunk_index < len(self.chunk_metadata):
            return self.chunk_metadata[chunk_index]
        return None
    
    def format_citation(self, chunk_index):
        """Format citation string for display"""
        meta = self.get_metadata(chunk_index)
        if meta:
            return f"📍 Page {meta['page']} | 📄 {meta['document']}"
        return "📍 Source: Document"
    
    def clear(self):
        """Clear all metadata"""
        self.chunk_metadata = []


# Global instance for use across the app
metadata_handler = MetadataHandler()