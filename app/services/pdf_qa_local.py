# app/services/pdf_qa_local.py

from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def answer_question(question: str, context_dict: dict) -> str:  # ✅ renamed
    scored = []
    question_embedding = model.encode(question, convert_to_tensor=True)

    for section_title, section_text in context_dict.items():
        section_embedding = model.encode(section_text, convert_to_tensor=True)
        score = util.cos_sim(question_embedding, section_embedding).item()
        scored.append((score, section_title, section_text))

    if not scored:
        return "No relevant information found in the document."

    top_score, top_section, top_text = max(scored, key=lambda x: x[0])
    snippet = top_text[:500] + "..." if len(top_text) > 500 else top_text
    return f"From section '{top_section}':\n{snippet}"
