import os
import sys

# Add utils to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.pdf_loader import load_pdfs
from utils.text_splitter import split_text
from utils.embeddings import create_embeddings, model
from utils.vector_store import create_vector_store, search_vector_store, save_vector_store, load_vector_store
from utils.qa_model import get_answer

def main():
    print("\n" + "="*60)
    print("📚 DOCQUERY - Document Question Answering System")
    print("="*60 + "\n")
    
    # Check if vector store exists
    index, chunks = load_vector_store()
    
    if index is None:
        print("First time setup: Processing PDF files...")
        
        # STEP 1 — Load PDFs
        data_folder = "data"
        
        if not os.path.exists(data_folder):
            print(f"Error: '{data_folder}' folder not found!")
            print(f"Please create a '{data_folder}' folder and add PDF files.")
            return
        
        pdf_files = []
        for file in os.listdir(data_folder):
            if file.endswith(".pdf"):
                pdf_files.append(os.path.join(data_folder, file))
        
        if not pdf_files:
            print(f"Error: No PDF files found in '{data_folder}' folder!")
            return
        
        print(f"\n📄 PDF Files Found: {len(pdf_files)}")
        for f in pdf_files:
            print(f"   - {os.path.basename(f)}")
        
        # STEP 2 — Load Text
        print("\n📖 Extracting text from PDFs...")
        text = load_pdfs(pdf_files)
        
        if not text:
            print("Error: No text extracted from PDFs!")
            return
        
        print(f"✅ Total text length: {len(text)} characters")
        
        # STEP 3 — Split Text
        print("\n✂️ Splitting text into chunks...")
        chunks = split_text(text)
        
        if not chunks:
            print("Error: Text splitting failed!")
            return
        
        # STEP 4 — Create Embeddings
        print("\n🔢 Creating embeddings...")
        embeddings = create_embeddings(chunks)
        
        # STEP 5 — Create Vector Store
        print("\n🗄️ Creating FAISS vector store...")
        index = create_vector_store(embeddings)
        
        # Save for future use
        save_vector_store(index, chunks)
        print("\n✅ Vector store saved for future use!")
    
    else:
        print("✅ Loaded existing vector store!")
    
    print("\n" + "="*60)
    print("💬 Ready to answer your questions!")
    print("Type 'quit' or 'exit' to stop")
    print("="*60 + "\n")
    
    # Interactive Q&A loop
    while True:
        query = input("❓ Your question: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if not query:
            print("Please enter a valid question.\n")
            continue
        
        print("\n🔍 Searching for relevant information...")
        
        # Generate query embedding
        query_embedding = model.encode(query)
        
        # Search vector store
        results, distances = search_vector_store(index, query_embedding, k=5)
        
        # Build context
        top_indexes = results[0]
        context_chunks = []
        
        for idx in top_indexes:
            chunk = chunks[idx]
            # Clean text
            chunk = chunk.replace("\n", " ")
            chunk = chunk.replace("•", " ")
            chunk = " ".join(chunk.split())
            context_chunks.append(chunk)
        
        best_context = " ".join(context_chunks)
        
        # Generate answer
        print("🤖 Generating answer...\n")
        answer = get_answer(query, best_context)
        
        print(f"📝 Answer: {answer}\n")
        print("-"*60 + "\n")

if __name__ == "__main__":
    main()