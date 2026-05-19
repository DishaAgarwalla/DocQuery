"""
Formats answers with proper citations and source references
"""

def format_answer_with_citation(answer, citations):
    """
    Format answer with citations
    
    Args:
        answer: The generated answer text
        citations: List of citation strings
    
    Returns:
        Formatted answer with citations
    """
    if not citations:
        return answer
    
    # Remove duplicate citations
    unique_citations = []
    for c in citations:
        if c not in unique_citations:
            unique_citations.append(c)
    
    # Add citations at the end
    citation_text = "\n\n" + "\n".join(unique_citations)
    
    return answer + citation_text


def format_multiple_sources(sources):
    """
    Format multiple sources for display
    
    Args:
        sources: List of dicts with 'page', 'document', 'preview'
    
    Returns:
        Formatted sources list
    """
    formatted = []
    for i, source in enumerate(sources, 1):
        page = source.get('page', 'N/A')
        doc = source.get('document', 'Unknown')
        preview = source.get('preview', '')
        
        citation = f"**Source {i}:** 📍 Page {page} | 📄 {doc}"
        if preview:
            citation += f"\n*Preview:* {preview[:200]}..."
        formatted.append(citation)
    
    return formatted


def create_export_text(question, answer, sources):
    """
    Create exportable text with all citations
    
    Args:
        question: The user's question
        answer: The generated answer
        sources: List of source dictionaries
    
    Returns:
        String formatted for export
    """
    export = []
    export.append("=" * 60)
    export.append(f"QUESTION: {question}")
    export.append("=" * 60)
    export.append(f"\nANSWER:\n{answer}\n")
    export.append("-" * 60)
    export.append("SOURCES:")
    
    for source in sources:
        page = source.get('page', 'N/A')
        doc = source.get('document', 'Unknown')
        export.append(f"  📍 Page {page} - {doc}")
    
    export.append("=" * 60)
    
    return "\n".join(export)


def get_sources_summary(sources):
    """
    Get a quick summary of sources
    
    Args:
        sources: List of source dictionaries
    
    Returns:
        String like "Found on pages 7, 12, 31"
    """
    pages = []
    documents = set()
    
    for source in sources:
        page = source.get('page', 'N/A')
        doc = source.get('document', 'Unknown')
        if page != 'N/A':
            pages.append(str(page))
        documents.add(doc)
    
    if len(pages) == 0:
        return f"Found in {len(documents)} document(s)"
    elif len(documents) == 1:
        return f"Found on page(s) {', '.join(pages)} from {list(documents)[0]}"
    else:
        return f"Found in {len(documents)} documents across {len(pages)} pages"