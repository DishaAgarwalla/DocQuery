"""
Multi-document comparison functionality
"""

import re
from difflib import SequenceMatcher
from collections import defaultdict

def find_similar_content(text1, text2, threshold=0.6):
    """Find similar sentences between two documents"""
    
    # Split into sentences
    sentences1 = re.split(r'[.!?]+', text1)
    sentences2 = re.split(r'[.!?]+', text2)
    
    # Clean sentences
    sentences1 = [s.strip().lower() for s in sentences1 if len(s.strip()) > 20]
    sentences2 = [s.strip().lower() for s in sentences2 if len(s.strip()) > 20]
    
    similar_pairs = []
    
    for s1 in sentences1[:50]:  # Limit for performance
        for s2 in sentences2[:50]:
            similarity = SequenceMatcher(None, s1, s2).ratio()
            if similarity > threshold:
                similar_pairs.append({
                    'doc1_sentence': s1,
                    'doc2_sentence': s2,
                    'similarity': round(similarity, 2)
                })
    
    return similar_pairs[:5]  # Return top 5


def extract_unique_concepts(chunks, doc_names):
    """Extract unique concepts per document"""
    
    doc_concepts = defaultdict(set)
    all_concepts = set()
    
    # Common technical terms to look for
    tech_terms = {
        'algorithm', 'function', 'class', 'variable', 'data structure',
        'machine learning', 'deep learning', 'neural network', 'regression',
        'classification', 'clustering', 'database', 'query', 'sql',
        'python', 'java', 'c++', 'javascript', 'html', 'css',
        'framework', 'library', 'api', 'endpoint', 'server', 'client'
    }
    
    for i, chunks_list in enumerate(chunks):
        if i < len(doc_names):
            all_text = " ".join(chunks_list).lower()
            doc_name = doc_names[i]
            
            for term in tech_terms:
                if term in all_text:
                    doc_concepts[doc_name].add(term)
                    all_concepts.add(term)
    
    # Find unique concepts per document
    unique_concepts = {}
    for doc in doc_concepts:
        unique = doc_concepts[doc] - (all_concepts - doc_concepts[doc])
        unique_concepts[doc] = list(unique)[:5]
    
    return unique_concepts


def compare_answers(answer1, answer2):
    """Compare two answers from different documents"""
    
    if not answer1 or not answer2:
        return None
    
    similarity = SequenceMatcher(None, answer1.lower(), answer2.lower()).ratio()
    
    comparison = {
        'similarity': round(similarity, 2),
        'consistency': 'consistent' if similarity > 0.6 else 'different',
        'answer1': answer1,
        'answer2': answer2
    }
    
    if similarity < 0.4:
        comparison['verdict'] = "The documents provide conflicting information"
    elif similarity < 0.7:
        comparison['verdict'] = "The documents have somewhat different explanations"
    else:
        comparison['verdict'] = "The documents are consistent on this topic"
    
    return comparison


def format_comparison_result(comparison, doc_name1, doc_name2):
    """Format comparison result for display"""
    
    if not comparison:
        return "Unable to compare documents"
    
    output = []
    output.append(f"📊 **Comparison between '{doc_name1}' and '{doc_name2}'**")
    output.append("")
    output.append(f"📄 **{doc_name1} says:** {comparison['answer1']}")
    output.append("")
    output.append(f"📄 **{doc_name2} says:** {comparison['answer2']}")
    output.append("")
    output.append(f"⚖️ **Similarity:** {comparison['similarity'] * 100}%")
    output.append(f"🎯 **Verdict:** {comparison['verdict']}")
    
    return "\n".join(output)


def suggest_comparison_questions(doc_names):
    """Suggest questions suitable for document comparison"""
    
    if len(doc_names) < 2:
        return []
    
    questions = [
        f"What are the differences in approach between {doc_names[0]} and {doc_names[1]}?",
        f"Compare the definitions of key concepts in both documents",
        f"What does {doc_names[0]} say that {doc_names[1]} doesn't cover?",
        f"Which document provides more detailed information?",
        f"How do these documents explain the same concepts differently?"
    ]
    
    return questions[:4]


def extract_document_summary(chunks, doc_name, max_sentences=3):
    """Extract a quick summary of a document for comparison context"""
    
    if not chunks:
        return f"No content available for {doc_name}"
    
    # Combine first few chunks
    text = " ".join(chunks[:5])
    
    # Find key sentences (ones with important keywords)
    sentences = re.split(r'[.!?]+', text)
    important_keywords = ['important', 'key', 'main', 'primary', 'essential', 'critical']
    
    important_sentences = []
    for sent in sentences:
        sent_lower = sent.lower()
        if any(keyword in sent_lower for keyword in important_keywords):
            important_sentences.append(sent.strip())
            if len(important_sentences) >= max_sentences:
                break
    
    if not important_sentences:
        important_sentences = [sentences[0].strip()] if sentences else ["No summary available"]
    
    return " ".join(important_sentences[:max_sentences])