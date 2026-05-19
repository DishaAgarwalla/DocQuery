from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re
import torch

print("Loading FLAN-T5 QA model...")

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
model = model.to(device)

print("QA model loaded successfully!")

def get_answer(question, context, max_context_length=800):
    """Generate accurate answer using improved prompting"""
    
    if not context or len(context.strip()) < 50:
        return "I couldn't find enough information in the documents to answer this question."
    
    if not question or len(question.strip()) < 3:
        return "Please ask a valid question."
    
    if len(context) > max_context_length:
        context = context[:max_context_length]
    
    context_cleaned = re.sub(r'\[PAGE_\d+_OF_[^\]]+\]\n?', '', context)
    context_cleaned = context_cleaned.replace('\n', ' ')
    context_cleaned = re.sub(r'\s+', ' ', context_cleaned)
    context_cleaned = context_cleaned.strip()
    
    prompt = f"""Question: {question}
Context: {context_cleaned}
Answer in one short sentence:"""
    
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding=True
    )
    
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    outputs = model.generate(
        **inputs,
        max_new_tokens=60,
        min_new_tokens=5,
        do_sample=False,
        num_beams=4,
        early_stopping=True
    )
    
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    answer = answer.strip()
    
    question_lower = question.lower()
    answer_lower = answer.lower()
    
    if answer_lower.startswith(question_lower[:20]) or question_lower[:20] in answer_lower[:50]:
        sentences = re.split(r'[.!?]', answer)
        for sent in sentences:
            sent = sent.strip()
            if len(sent) > 10 and question_lower[:15] not in sent.lower():
                answer = sent
                break
    
    if not answer or len(answer) < 5:
        return "Based on the documents, " + context_cleaned[:100] + "..."
    
    if answer.lower() == question.lower():
        return "The information is in the documents. Please check the sources below."
    
    if answer:
        answer = answer[0].upper() + answer[1:]
    
    if answer and answer[-1] not in ['.', '!', '?']:
        answer += '.'
    
    return answer

def extract_page_from_chunk(chunk):
    """Extract page number and document name from a chunk"""
    match = re.search(r'\[PAGE_(\d+)_OF_([^\]]+)\]', chunk)
    if match:
        return int(match.group(1)), match.group(2)
    return None, None


def get_comparison_answer(question, context1, context2, doc_name1, doc_name2):
    """Generate comparative answer from two documents"""
    
    if not context1 or not context2:
        return "Insufficient context from one or both documents."
    
    prompt = f"""Compare the answers from two documents.

Document 1 ({doc_name1}) context: {context1[:500]}
Document 2 ({doc_name2}) context: {context2[:500]}

Question: {question}

Compare the answers and highlight similarities and differences:"""
    
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    outputs = model.generate(**inputs, max_new_tokens=150, do_sample=False, num_beams=4)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return answer.strip()