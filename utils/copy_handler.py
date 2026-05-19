"""
Copy answer to clipboard handler for DocQuery
"""

import streamlit as st
import pyperclip

def create_copy_button(answer, citations=None):
    """
    Create a copy button for the answer
    
    Args:
        answer: The answer text to copy
        citations: Optional citations to include
    
    Returns:
        Copy button component
    """
    
    # Prepare text to copy
    text_to_copy = answer
    
    if citations:
        text_to_copy += "\n\n" + "\n".join(citations)
    
    # Create unique key for button
    import hashlib
    key = hashlib.md5(text_to_copy.encode()).hexdigest()[:10]
    
    # Copy button
    if st.button("📋 Copy Answer", key=f"copy_btn_{key}", use_container_width=True):
        try:
            pyperclip.copy(text_to_copy)
            st.success("✅ Copied to clipboard!")
        except:
            # Fallback using JavaScript
            st.markdown(f"""
            <script>
            function copyToClipboard() {{
                const text = `{text_to_copy.replace('`', '\\`')}`;
                navigator.clipboard.writeText(text);
                alert('Copied to clipboard!');
            }}
            </script>
            <button onclick="copyToClipboard()" style="padding: 0.5rem; border-radius: 0.5rem; background-color: #28a745; color: white; border: none; cursor: pointer;">
            📋 Copy Answer
            </button>
            """, unsafe_allow_html=True)
            st.success("✅ Copied to clipboard!")
    
    return text_to_copy


def copy_with_format(answer, sources, include_sources=True):
    """
    Copy answer with optional sources
    
    Args:
        answer: The answer text
        sources: List of source dictionaries
        include_sources: Whether to include sources
    
    Returns:
        Formatted text for copying
    """
    
    formatted = []
    formatted.append("=" * 60)
    formatted.append("DOCQUERY ANSWER")
    formatted.append("=" * 60)
    formatted.append(f"\n{answer}\n")
    
    if include_sources and sources:
        formatted.append("-" * 40)
        formatted.append("SOURCES:")
        for i, source in enumerate(sources, 1):
            page = source.get('page', 'N/A')
            doc = source.get('document', 'Unknown')
            formatted.append(f"  Source {i}: Page {page} - {doc}")
    
    formatted.append("\n" + "=" * 60)
    
    return "\n".join(formatted)


def create_export_button(question, answer, sources):
    """
    Create an export button for the entire Q&A
    
    Args:
        question: User's question
        answer: Generated answer
        sources: List of sources
    """
    
    export_text = copy_with_format(answer, sources, include_sources=True)
    export_text = f"Q: {question}\n\nA: {export_text}"
    
    st.download_button(
        label="📥 Export Q&A",
        data=export_text,
        file_name=f"docquery_qa.txt",
        mime="text/plain",
        use_container_width=True
    )


def create_quick_copy_button(answer):
    """
    Simple one-click copy button
    
    Args:
        answer: The answer text
    """
    
    if st.button("📋 Quick Copy", use_container_width=True):
        try:
            pyperclip.copy(answer)
            st.toast("✅ Copied!", icon="✅")
        except:
            st.markdown(f"""
            <button onclick="navigator.clipboard.writeText(`{answer.replace('`', '\\`')}`); alert('Copied!')" 
            style="padding:0.5rem; background:#28a745; color:white; border:none; border-radius:0.5rem; cursor:pointer;">
            📋 Click to Copy
            </button>
            """, unsafe_allow_html=True)