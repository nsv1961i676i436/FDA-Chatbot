from fastapi import FastAPI, HTTPException, Request
from app.services.pdf_qa_local import answer_question

app = FastAPI()

@app.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    question = data.get("question")
    context = data.get("context")

    if not question or not context:
        raise HTTPException(status_code=400, detail="Missing question or context.")

    try:
        answer = answer_question(question, context)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to answer: {e}")
