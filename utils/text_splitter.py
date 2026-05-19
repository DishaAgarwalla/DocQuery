import re
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(text):
    """Split text into meaningful chunks - avoid table of contents"""
    
    # Remove table of contents patterns
    lines = text.split('\n')
    filtered_lines = []
    
    for line in lines:
        # Skip lines that look like table of contents
        if re.match(r'^\s*\.{2,}\s+\d+$', line):  # ...... 22
            continue
        if re.match(r'^\s*\d+\.\s+\w+.*\.{2,}\d+$', line):  # 1. Title......22
            continue
        if re.match(r'^\s*\w+\s+\.{2,}\s+\d+$', line):  # Chapter......22
            continue
        filtered_lines.append(line)
    
    cleaned_text = '\n'.join(filtered_lines)
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=150,
        separators=[
            "\n\n",  # Paragraphs
            "\n",    # Lines  
            ". ",    # Sentences
            "? ",    # Questions
            "! ",    # Exclamations
            "; ",    # Semicolons
            ", ",    # Commas
            " ",     # Words
            ""       # Characters
        ],
        length_function=len
    )
    
    chunks = splitter.split_text(cleaned_text)
    
    # Filter out chunks that are likely table of contents
    valid_chunks = []
    for chunk in chunks:
        # Skip chunks that are mostly page numbers or dots
        if len(chunk) > 0:
            dot_ratio = chunk.count('.') / len(chunk)
            digit_ratio = sum(c.isdigit() for c in chunk) / len(chunk)
            
            if dot_ratio < 0.3 and digit_ratio < 0.3:
                valid_chunks.append(chunk)
        else:
            valid_chunks.append(chunk)
    
    print(f"\n✅ Text Splitting Completed.")
    print(f"Total Chunks: {len(valid_chunks)} (filtered from {len(chunks)})")
    
    return valid_chunks