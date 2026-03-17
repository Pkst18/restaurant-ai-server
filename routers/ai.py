from fastapi import APIRouter
from app.services.rag import ask_with_rag
from app.services.summarize import summarize_reviews
from app.services.insights import get_insights

router = APIRouter()

@router.post("/{restaurant_id}/ask")
def ask(restaurant_id: int, body: dict):
    question = body.get("question")
    if not question:
        return {"error": "กรุณาส่ง question มาด้วย"}
    answer = ask_with_rag(restaurant_id, question)
    return {"question": question, "answer": answer}

@router.get("/{restaurant_id}/summary")
def summary(restaurant_id: int):
    result = summarize_reviews(restaurant_id)
    return {"summary": result}

@router.get("/{restaurant_id}/insights")
def insights(restaurant_id: int):
    result = get_insights(restaurant_id)
    return result