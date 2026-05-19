import streamlit as st
import os
import sys
import shutil
import re
import time

# Add utils to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.pdf_loader import load_pdfs, clean_text_chunk
from utils.text_splitter import split_text
from utils.embeddings import create_embeddings, model
from utils.vector_store import create_vector_store, search_vector_store, save_vector_store, load_vector_store
from utils.qa_model import get_answer, extract_page_from_chunk
from utils.citation_formatter import format_answer_with_citation, create_export_text
from utils.dark_mode import get_theme_toggle
from utils.copy_handler import create_copy_button
from utils.question_suggestions import generate_suggestions, get_context_based_suggestions
from utils.document_comparison import compare_answers, format_comparison_result

# Page configuration
st.set_page_config(
    page_title="DocQuery - Document QA System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply theme
current_theme = get_theme_toggle()

# Custom CSS based on theme
if current_theme == "dark":
    st.markdown("""
    <style>
        .answer-box {
            background-color: #1e2a1e;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #00ff88;
            margin: 0.5rem 0;
            color: #e0e0e0;
            animation: fadeIn 0.5s ease-in;
        }
        .answer-box strong { color: #00ff88; }
        .source-card {
            background-color: #1a1a2e;
            padding: 0.8rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
            border-left: 3px solid #00ff88;
            color: #c0c0c0;
            animation: slideIn 0.3s ease-out;
        }
        .source-card strong { color: #00ff88; }
        .main-header {
            text-align: center;
            padding: 1rem;
            background: linear-gradient(90deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 0.5rem;
            color: white;
            margin-bottom: 2rem;
        }
        .stTextInput input {
            background-color: #2a2a2a;
            color: white;
            border: 1px solid #444;
        }
        .stButton button {
            background-color: #2a2a3e;
            color: white;
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            background-color: #3a3a4e;
            border-color: #00ff88;
            transform: scale(1.02);
        }
        .stMetric {
            background-color: #1a1a2e;
            padding: 0.5rem;
            border-radius: 0.5rem;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        .answer-box {
            background-color: #d4edda;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #28a745;
            margin: 0.5rem 0;
            animation: fadeIn 0.5s ease-in;
        }
        .source-card {
            background-color: #f8f9fa;
            padding: 0.8rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
            border-left: 3px solid #007bff;
            animation: slideIn 0.3s ease-out;
        }
        .main-header {
            text-align: center;
            padding: 1rem;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 0.5rem;
            color: white;
            margin-bottom: 2rem;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📄 DocQuery</h1>
    <p>Intelligent Document Question Answering System with Citations & Comparison</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processing_done" not in st.session_state:
    st.session_state.processing_done = False
if "chunk_metadata" not in st.session_state:
    st.session_state.chunk_metadata = {}
if "comparison_mode" not in st.session_state:
    st.session_state.comparison_mode = False
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None
if "processing_complete" not in st.session_state:
    st.session_state.processing_complete = False

# Sidebar
with st.sidebar:
    # Real-time Stats at the top
    st.header("📊 Live Stats")
    
    # Get current document count
    data_folder = "data"
    pdf_files = []
    if os.path.exists(data_folder):
        pdf_files = [f for f in os.listdir(data_folder) if f.endswith(".pdf")]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📄 Documents", len(pdf_files))
    with col2:
        # This will be updated after system loads
        st.metric("📊 Status", "Ready" if 'index' in dir() and index else "Loading")
    
    st.divider()
    
    # Collapsible System Information
    with st.expander("⚙️ System Information", expanded=False):
        st.markdown("""
        **Components:**
        - 📚 PDF Processing (PyPDF)
        - ✂️ Text Chunking (LangChain)
        - 🔢 Embeddings (all-MiniLM-L6-v2)
        - 🗄️ Vector Store (FAISS)
        - 🤖 LLM (FLAN-T5-small)
        
        **Settings:**
        - Chunk Size: 700
        - Overlap: 150
        - Top K Results: 5
        """)
    
    st.divider()
    
    # Comparison Mode Toggle
    st.subheader("🔍 Comparison Mode")
    if st.button("📊 Compare Two Documents", use_container_width=True):
        st.session_state.comparison_mode = not st.session_state.comparison_mode
        st.rerun()
    
    if st.session_state.comparison_mode:
        st.info("Comparison Mode ACTIVE - Ask questions comparing two documents")
    
    st.divider()
    
    # File upload section with progress animation
    st.subheader("📁 Upload PDFs")
    uploaded_files = st.file_uploader(
        "Add PDF documents", 
        type=['pdf'], 
        accept_multiple_files=True,
        help="Upload any PDF file with selectable text"
    )
    
    if uploaded_files:
        if st.button("🔄 Process New Documents", type="primary"):
            with st.spinner("📚 Processing uploaded documents... Please wait..."):
                # Animated progress placeholder
                progress_text = st.empty()
                progress_bar = st.progress(0)
                
                # Clear data folder
                if os.path.exists("data"):
                    for old_file in os.listdir("data"):
                        if old_file.endswith(".pdf"):
                            os.remove(os.path.join("data", old_file))
                else:
                    os.makedirs("data", exist_ok=True)
                
                progress_bar.progress(20)
                progress_text.text("📁 Saving uploaded files...")
                time.sleep(0.3)
                
                # Save uploaded files
                saved_files = []
                for i, uploaded_file in enumerate(uploaded_files):
                    file_path = os.path.join("data", uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    saved_files.append(uploaded_file.name)
                    progress = 20 + (i + 1) * 10
                    progress_bar.progress(min(progress, 50))
                
                progress_text.text("🗑️ Clearing old data...")
                time.sleep(0.3)
                progress_bar.progress(60)
                
                # Delete old vector store
                vector_store_path = "utils/vector_store"
                if os.path.exists(vector_store_path):
                    shutil.rmtree(vector_store_path)
                
                progress_text.text("🔄 Refreshing system...")
                time.sleep(0.3)
                progress_bar.progress(80)
                
                # Clear cache
                st.cache_resource.clear()
                st.session_state.processing_done = True
                st.session_state.messages = []
                st.session_state.chunk_metadata = {}
                
                progress_text.text("✅ Complete!")
                progress_bar.progress(100)
                time.sleep(0.5)
                progress_text.empty()
                progress_bar.empty()
                
                st.success(f"✅ Added {len(saved_files)} document(s): {', '.join(saved_files)}")
                st.info("🔄 Refreshing... Please wait.")
                time.sleep(1)
                st.rerun()
    
    st.divider()
    
    # Clear buttons with animation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            with st.spinner("Clearing chat history..."):
                time.sleep(0.3)
                st.session_state.messages = []
                st.rerun()
    with col2:
        if st.button("🔄 Clear All Data", use_container_width=True):
            with st.spinner("Clearing all data..."):
                time.sleep(0.3)
                if os.path.exists("utils/vector_store"):
                    shutil.rmtree("utils/vector_store")
                if os.path.exists("data"):
                    for f in os.listdir("data"):
                        if f.endswith(".pdf"):
                            os.remove(os.path.join("data", f))
                st.cache_resource.clear()
                st.session_state.messages = []
                st.session_state.chunk_metadata = {}
                st.success("All data cleared!")
                time.sleep(0.5)
                st.rerun()

def check_pdf_quality(pdf_path):
    """Check if PDF has extractable text"""
    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf_path)
        text = ""
        for i, page in enumerate(reader.pages[:2]):
            text += page.extract_text() or ""
        if len(text.strip()) > 100:
            return True, f"✅ Good! Found {len(text)} characters"
        else:
            return False, f"⚠️ Only {len(text)} characters found. PDF may be scanned image."
    except Exception as e:
        return False, f"❌ Error reading PDF: {str(e)[:100]}"

@st.cache_resource
def load_system():
    index, chunks, metadata = load_vector_store()
    
    if index is None:
        data_folder = "data"
        
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
            return None, None, None
        
        pdf_files = []
        for file in os.listdir(data_folder):
            if file.endswith(".pdf"):
                pdf_files.append(os.path.join(data_folder, file))
        
        if not pdf_files:
            return None, None, None
        
        # Animated processing
        progress_text = st.empty()
        progress_bar = st.progress(0)
        
        progress_text.text("🔍 Checking PDF quality...")
        progress_bar.progress(10)
        
        for pdf_path in pdf_files:
            is_good, message = check_pdf_quality(pdf_path)
            if not is_good:
                st.warning(f"📄 {os.path.basename(pdf_path)}: {message}")
        
        progress_text.text("📖 Loading PDFs...")
        progress_bar.progress(30)
        
        text, pdf_metadata = load_pdfs(pdf_files)
        
        if len(text.strip()) < 100:
            st.error("❌ No readable text found in uploaded PDFs!")
            return None, None, None
        
        progress_text.text("✂️ Splitting text into chunks...")
        progress_bar.progress(50)
        
        chunks = split_text(text)
        
        if not chunks:
            st.error("❌ No text chunks created!")
            return None, None, None
        
        progress_text.text("📝 Creating metadata...")
        progress_bar.progress(60)
        
        chunk_metadata = []
        for i, chunk in enumerate(chunks):
            page_num, doc_name = extract_page_from_chunk(chunk)
            if page_num and doc_name:
                chunk_metadata.append({'chunk_id': i, 'page': page_num, 'document': doc_name})
            else:
                chunk_metadata.append({'chunk_id': i, 'page': 'N/A', 'document': os.path.basename(pdf_files[0]) if pdf_files else 'Unknown'})
        
        progress_text.text("🔢 Generating embeddings...")
        progress_bar.progress(75)
        
        embeddings = create_embeddings(chunks)
        
        if len(embeddings) == 0:
            st.error("❌ No embeddings created!")
            return None, None, None
        
        progress_text.text("🗄️ Creating vector store...")
        progress_bar.progress(90)
        
        index = create_vector_store(embeddings)
        save_vector_store(index, chunks, chunk_metadata)
        
        progress_text.text("✅ Complete!")
        progress_bar.progress(100)
        time.sleep(0.5)
        progress_text.empty()
        progress_bar.empty()
        
        st.success(f"✅ Processed {len(pdf_files)} PDF(s), created {len(chunks)} chunks")
        return index, chunks, chunk_metadata
    
    return index, chunks, metadata

# Initialize system
with st.spinner("🔄 Initializing DocQuery system..."):
    index, chunks, chunk_metadata = load_system()

# Main chat interface
if index is None or chunks is None:
    st.warning("⚠️ No PDF documents found or processed!")
    st.info("📤 Use the sidebar to upload PDF files and click 'Process New Documents'.")
    
    with st.expander("📖 How to use DocQuery"):
        st.markdown("""
        ### Steps to use:
        1. **Upload PDF files** using the sidebar uploader
        2. Click **"Process New Documents"** button
        3. Wait for processing to complete
        4. Start asking questions!
        
        **Features:**
        - 🌙 Dark mode toggle
        - 📋 Copy answers to clipboard
        - 📍 Page number citations
        - 📥 Export answers
        - 💡 Question suggestions
        - 📊 Compare two documents
        """)
else:
    # Update the metrics in sidebar (needs rerun to show)
    st.success(f"✅ System ready! {index.ntotal} document chunks loaded.")
    
    # Show current documents
    with st.expander("📚 Current Documents"):
        data_folder = "data"
        if os.path.exists(data_folder):
            pdfs = [f for f in os.listdir(data_folder) if f.endswith(".pdf")]
            for pdf in pdfs:
                st.text(f"📄 {pdf}")
    
    # Question Suggestions Section
    with st.expander("💡 Suggested Questions (click to expand)", expanded=False):
        if chunks and len(chunks) > 0:
            with st.spinner("Generating suggestions..."):
                suggestions = generate_suggestions(chunks, num_suggestions=4)
            st.markdown("**Try asking:**")
            cols = st.columns(2)
            for i, suggestion in enumerate(suggestions):
                with cols[i % 2]:
                    if st.button(f"💬 {suggestion}", key=f"sugg_{i}"):
                        st.session_state.pending_question = suggestion
                        st.rerun()
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Check for pending question (auto-submit for follow-ups)
    if st.session_state.pending_question:
        query = st.session_state.pending_question
        st.session_state.pending_question = None
    else:
        # Question input
        col1, col2 = st.columns([5, 1])
        with col1:
            query = st.text_input("Ask a question about your documents:", key="main_input", label_visibility="collapsed", placeholder="Type your question here...")
        with col2:
            submit_clicked = st.button("📤 Ask", type="primary", use_container_width=True)
        
        if not submit_clicked:
            query = None
    
    # Process the question
    if query:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
        
        # Generate response with animated spinner
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching documents and generating answer..."):
                try:
                    # Search for relevant chunks
                    query_embedding = model.encode(query)
                    results, distances = search_vector_store(index, query_embedding, k=5)
                    
                    # Build context and collect citations
                    top_indexes = results[0]
                    context_chunks = []
                    citations = []
                    sources = []
                    all_docs = []
                    
                    for idx in top_indexes:
                        if idx < len(chunks):
                            chunk = chunks[idx]
                            if chunk_metadata and idx < len(chunk_metadata):
                                meta = chunk_metadata[idx]
                                page = meta.get('page', 'N/A')
                                doc = meta.get('document', 'Unknown')
                                citations.append(f"📍 Page {page} | 📄 {doc}")
                                sources.append({'page': page, 'document': doc, 'preview': chunk[:200]})
                                all_docs.append(doc)
                            else:
                                page_num, doc_name = extract_page_from_chunk(chunk)
                                if page_num and doc_name:
                                    citations.append(f"📍 Page {page_num} | 📄 {doc_name}")
                                    sources.append({'page': page_num, 'document': doc_name, 'preview': chunk[:200]})
                                    all_docs.append(doc_name)
                                else:
                                    citations.append("📍 Source: Document")
                                    sources.append({'page': 'N/A', 'document': 'Unknown', 'preview': chunk[:200]})
                            
                            chunk = clean_text_chunk(chunk)
                            chunk = chunk.replace("\n", " ")
                            chunk = " ".join(chunk.split())
                            context_chunks.append(chunk)
                    
                    best_context = " ".join(context_chunks)
                    
                    # Check if in comparison mode
                    if st.session_state.comparison_mode and len(set(all_docs)) > 1:
                        docs_found = list(set(all_docs))
                        doc_answers = {}
                        for doc_name in docs_found[:2]:
                            doc_context = " ".join([chunks[i] for i in top_indexes if i < len(chunks) and chunk_metadata and chunk_metadata[i].get('document') == doc_name])
                            doc_context = clean_text_chunk(doc_context)
                            doc_answer = get_answer(query, doc_context)
                            doc_answers[doc_name] = doc_answer
                        
                        if len(doc_answers) >= 2:
                            doc_list = list(doc_answers.keys())
                            comparison = compare_answers(doc_answers[doc_list[0]], doc_answers[doc_list[1]])
                            answer = format_comparison_result(comparison, doc_list[0], doc_list[1])
                        else:
                            answer = get_answer(query, best_context)
                    else:
                        answer = get_answer(query, best_context)
                    
                    # Generate follow-up suggestions
                    follow_ups = get_context_based_suggestions(query, answer, chunks[:10])
                    
                    # Format answer with citations
                    unique_citations = list(dict.fromkeys(citations))
                    formatted_answer = format_answer_with_citation(answer, unique_citations[:3])
                    
                    # Display answer
                    st.markdown(f'<div class="answer-box"><strong>📝 Answer:</strong><br>{formatted_answer}</div>', unsafe_allow_html=True)
                    
                    # Display follow-up suggestions
                    if follow_ups:
                        st.markdown("**💡 Follow-up questions you might ask:**")
                        cols = st.columns(3)
                        for i, fu in enumerate(follow_ups[:3]):
                            with cols[i]:
                                if st.button(f"➡️ {fu}", key=f"followup_{i}_{hash(fu)}"):
                                    st.session_state.pending_question = fu
                                    st.rerun()
                    
                    # Add Copy Button
                    col1, col2 = st.columns([3, 1])
                    with col2:
                        create_copy_button(answer, unique_citations[:3])
                    
                    # Show sources
                    with st.expander("📚 View sources with page numbers (click to expand)"):
                        for i, source in enumerate(sources[:3], 1):
                            st.markdown(f"""
                            <div class="source-card">
                                <strong>Source {i}:</strong><br>
                                📍 <strong>Page:</strong> {source['page']}<br>
                                📄 <strong>Document:</strong> {source['document']}<br>
                                <strong>Preview:</strong><br>
                                <code>{source['preview'][:300]}...</code>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Export button
                    export_text = create_export_text(query, answer, sources[:3])
                    st.download_button(
                        label="📥 Export Q&A",
                        data=export_text,
                        file_name=f"docquery_qa_{int(time.time())}.txt",
                        mime="text/plain",
                        key=f"export_{hash(query)}"
                    )
                
                except Exception as e:
                    error_msg = f"❌ Error generating answer: {str(e)}"
                    st.error(error_msg)
                    answer = error_msg
        
        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": formatted_answer if 'formatted_answer' in locals() else answer})
        
        # Clear input and rerun to show the answer
        st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Powered by FAISS, Sentence Transformers, and FLAN-T5 | 📍 Answers include page citations | 🌙 Dark mode available | 💡 Question suggestions | 📊 Document comparison</p>",
    unsafe_allow_html=True
)