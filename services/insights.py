from app.services.retriever import retrieve_reviews
from app.services.llm import chat
from app.services.cache import get_cache, set_cache
import json

def get_insights(restaurant_id: int) -> dict:
    # เช็ค cache ก่อน
    cached = get_cache(restaurant_id, "insights")
    if cached:
        print("✅ cache hit — ไม่เรียก OpenAI")
        return json.loads(cached)  # แปลง string → dict

    print("⏳ cache miss — เรียก OpenAI")
    reviews = retrieve_reviews(
        restaurant_id,
        query="เมนูอาหาร ข้อดี ข้อเสีย สิ่งที่ดี สิ่งที่ควรปรับปรุง",
        top_k=10
    )

    if not reviews:
        return {"error": "ไม่พบข้อมูลรีวิว"}

    review_text = "\n".join([
        f"รีวิว {i+1}: {r['content_chunk']}"
        for i, r in enumerate(reviews)
    ])

    messages = [
        {
            "role": "system",
            "content": """คุณคือผู้ช่วยวิเคราะห์รีวิวร้านอาหาร
วิเคราะห์แล้วตอบเป็น JSON เท่านั้น ห้ามมีข้อความอื่น
รูปแบบ:
{
  "pros": ["ข้อดี 1", "ข้อดี 2"],
  "cons": ["ข้อเสีย 1", "ข้อเสีย 2"],
  "popular_menus": ["เมนูยอดนิยม 1", "เมนูยอดนิยม 2"]
}"""
        },
        {
            "role": "user",
            "content": f"รีวิวทั้งหมด:\n{review_text}\n\nวิเคราะห์ข้อดี ข้อเสีย และเมนูยอดนิยม"
        }
    ]

    result = chat(messages)
    set_cache(restaurant_id, "insights", result)  # บันทึกลง cache
    
    try:
        return json.loads(result)
    except:
        return {"error": "AI ตอบผิดรูปแบบ", "raw": result}

    # แปลง string JSON → dict
    try:
        return json.loads(result)
    except:
        return {"error": "AI ตอบผิดรูปแบบ", "raw": result}