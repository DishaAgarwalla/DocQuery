"""
Generate suggested questions based on document content
"""

import re
import random
from collections import Counter

# Common question templates
QUESTION_TEMPLATES = [
    "What is {}?",
    "Explain {} in detail",
    "How does {} work?",
    "What are the benefits of {}?",
    "What is the difference between {}?",
    "Why is {} important?",
    "Can you describe {}?",
    "What are the types of {}?",
    "How to use {}?",
    "What is the purpose of {}?",
]

# Technical keywords to look for
TECHNICAL_KEYWORDS = [
    'algorithm', 'function', 'class', 'method', 'variable', 'data', 'structure',
    'list', 'dictionary', 'tuple', 'set', 'array', 'string', 'integer', 'float',
    'loop', 'condition', 'statement', 'syntax', 'error', 'exception',
    'database', 'query', 'table', 'row', 'column', 'index', 'key',
    'machine learning', 'artificial intelligence', 'neural network', 'model',
    'training', 'testing', 'prediction', 'classification', 'regression',
    'python', 'java', 'javascript', 'html', 'css', 'sql',
    'framework', 'library', 'package', 'module', 'import'
]

def extract_keywords(text, num_keywords=10):
    """Extract important keywords from text"""
    
    # Clean text
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    words = text.split()
    
    # Filter words (at least 4 chars, not common stop words)
    stop_words = {'the', 'and', 'for', 'are', 'with', 'from', 'this', 'that', 
                  'have', 'will', 'you', 'can', 'your', 'not', 'but', 'was', 
                  'all', 'they', 'has', 'been', 'more', 'than', 'into', 'such',
                  'when', 'how', 'what', 'where', 'who', 'which', 'why', 'would',
                  'could', 'should', 'these', 'those', 'their', 'there', 'about'}
    
    filtered_words = [w for w in words if len(w) > 3 and w not in stop_words]
    
    # Count frequency
    word_counts = Counter(filtered_words)
    
    # Get top keywords
    keywords = [word for word, count in word_counts.most_common(num_keywords)]
    
    return keywords


def extract_phrases(text, num_phrases=5):
    """Extract meaningful phrases from text"""
    
    # Look for capitalized terms or technical terms
    phrases = []
    
    # Find capitalized words/phrases (potential technical terms)
    capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
    phrases.extend(capitalized)
    
    # Find technical keywords
    for keyword in TECHNICAL_KEYWORDS:
        if keyword in text.lower():
            phrases.append(keyword.title())
    
    # Remove duplicates and limit
    unique_phrases = list(dict.fromkeys(phrases))
    
    return unique_phrases[:num_phrases]


def generate_suggestions(chunks, num_suggestions=3):
    """Generate question suggestions based on document chunks"""
    
    if not chunks:
        return ["What is this document about?", "Summarize the main points", "What are the key topics?"]
    
    # Combine all chunks
    all_text = " ".join(chunks[:10])  # Limit to first 10 chunks for speed
    
    # Extract keywords and phrases
    keywords = extract_keywords(all_text, 8)
    phrases = extract_phrases(all_text, 5)
    
    suggestions = []
    
    # Generate questions from keywords
    for keyword in keywords[:3]:
        template = random.choice(QUESTION_TEMPLATES)
        question = template.format(keyword.title())
        suggestions.append(question)
    
    # Generate questions from phrases
    for phrase in phrases[:2]:
        if phrase and len(phrase) > 3:
            suggestions.append(f"Explain {phrase}")
    
    # Add default questions if needed
    if len(suggestions) < num_suggestions:
        defaults = [
            "What is the main topic of this document?",
            "Summarize the key points",
            "What are the important concepts?",
            "Can you provide an overview?",
            "What should I know from this document?"
        ]
        suggestions.extend(defaults[:num_suggestions - len(suggestions)])
    
    # Remove duplicates and limit
    unique_suggestions = list(dict.fromkeys(suggestions))
    
    return unique_suggestions[:num_suggestions]


def get_context_based_suggestions(question, answer, chunks):
    """Generate follow-up questions based on current Q&A"""
    
    follow_ups = []
    
    # Extract key terms from answer
    answer_lower = answer.lower()
    
    # Common follow-up patterns
    if 'example' not in answer_lower:
        follow_ups.append("Can you give an example?")
    
    if 'difference' not in answer_lower and 'compare' not in answer_lower:
        follow_ups.append("How is this different from others?")
    
    if 'advantage' not in answer_lower and 'benefit' not in answer_lower:
        follow_ups.append("What are the advantages?")
    
    if 'disadvantage' not in answer_lower and 'drawback' not in answer_lower:
        follow_ups.append("What are the disadvantages?")
    
    # Add default follow-up
    if len(follow_ups) < 2:
        follow_ups.append("Tell me more about this")
        follow_ups.append("Why is this important?")
    
    return follow_ups[:3]


def format_suggestions_for_ui(suggestions):
    """Format suggestions for display in UI"""
    
    formatted = []
    for i, suggestion in enumerate(suggestions, 1):
        formatted.append(f"💡 {suggestion}")
    
    return formatted