from app.services.retriever import retrieve_reviews
from app.services.llm import chat
from app.services.cache import get_cache, set_cache

def summarize_reviews(restaurant_id: int) -> str:
    # เช็ค cache ก่อนเลย
    cached = get_cache(restaurant_id, "summary")
    if cached:
        print("✅ cache hit — ไม่เรียก OpenAI")
        return cached

    print("⏳ cache miss — เรียก OpenAI")
    reviews = retrieve_reviews(
        restaurant_id,
        query="ภาพรวมร้านอาหาร บรรยากาศ อาหาร บริการ",
        top_k=10
    )

    if not reviews:
        return "ไม่พบข้อมูลรีวิวของร้านนี้"

    review_text = "\n".join([
        f"รีวิว {i+1}: {r['content_chunk']}"
        for i, r in enumerate(reviews)
    ])

    messages = [
        {
            "role": "system",
            "content": """คุณคือผู้ช่วยสรุปรีวิวร้านอาหาร
สรุปให้ครอบคลุมใน 3-5 ประโยค โดยพูดถึง:
- ภาพรวมอาหาร
- การบริการ
- บรรยากาศ
- ความคุ้มค่า
ตอบเป็นภาษาไทย กระชับ ได้ใจความ"""
        },
        {
            "role": "user",
            "content": f"รีวิวทั้งหมด:\n{review_text}\n\nสรุปรีวิวร้านนี้ให้หน่อย"
        }
    ]

    result = chat(messages)
    set_cache(restaurant_id, "summary", result)  # บันทึกลง cache
    return result