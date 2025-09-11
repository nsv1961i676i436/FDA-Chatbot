# question answering logic, using openAI
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def answer_question(question: str, context: dict) -> str:
    scored_sections = []
    for heading, content in context.items():
        score = float(util.cos_sim(
            model.encode(question, convert_to_tensor=True),
            model.encode(content, convert_to_tensor=True)
        ))
        scored_sections.append((score, heading, content))

    # Pick top section
    top = max(scored_sections, key=lambda x: x[0])
    return f"From section '{top[1]}': {top[2][:300]}..."  # basic extract, could enhance
