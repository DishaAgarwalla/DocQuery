from pypdf import PdfReader
import os

def load_pdfs(file_paths):
    """Load and extract text from PDF and TXT files with page numbers"""
    all_text = ""
    all_metadata = []
    
    for file_path in file_paths:
        try:
            if file_path.endswith('.pdf'):
                doc_name = os.path.basename(file_path)
                print(f"📖 Loading PDF: {doc_name}")
                pdf = PdfReader(file_path)
                
                for page_num, page in enumerate(pdf.pages, 1):
                    content = page.extract_text()
                    if content:
                        page_marker = f"\n[PAGE_{page_num}_OF_{doc_name}]\n"
                        all_text += page_marker + content + "\n"
                        all_metadata.append({
                            'page': page_num,
                            'document': doc_name,
                            'position': len(all_text)
                        })
                    else:
                        print(f"  ⚠️ No text on page {page_num}")
            
            elif file_path.endswith('.txt'):
                doc_name = os.path.basename(file_path)
                print(f"📝 Loading TXT: {doc_name}")
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    all_text += content + "\n"
                    all_metadata.append({
                        'page': 1,
                        'document': doc_name,
                        'position': len(all_text)
                    })
        
        except Exception as e:
            print(f"❌ Error loading {file_path}: {e}")
            continue
    
    return all_text, all_metadata

def extract_page_from_text(text):
    """Extract page number from text chunk if present"""
    import re
    match = re.search(r'\[PAGE_(\d+)_OF_([^\]]+)\]', text)
    if match:
        return int(match.group(1)), match.group(2)
    return None, None

def clean_text_chunk(chunk):
    """Remove page markers from text chunk for clean display"""
    import re
    return re.sub(r'\[PAGE_\d+_OF_[^\]]+\]\n?', '', chunk)