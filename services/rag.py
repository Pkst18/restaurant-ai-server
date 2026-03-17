from app.services.retriever import retrieve_reviews
from app.services.llm import chat
from app.db import get_connection
import json

def get_restaurant_info(restaurant_id: int) -> dict | None:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT * FROM restaurants WHERE id = %s",
            (restaurant_id,)
        )
        return cur.fetchone()
    finally:
        conn.close()

def ask_with_rag(restaurant_id: int, question: str) -> str:

    # ดึงข้อมูลร้านมาก่อนเลย
    restaurant = get_restaurant_info(restaurant_id)
    if not restaurant:
        return "ไม่พบข้อมูลร้านนี้"

    # ดึง review ที่เกี่ยวข้อง
    reviews = retrieve_reviews(restaurant_id, question, top_k=5)

    review_text = "\n".join([
        f"รีวิว {i+1}: {r['content_chunk']}"
        for i, r in enumerate(reviews)
    ]) if reviews else "ไม่มีข้อมูลรีวิว"

    # ประกอบข้อมูลร้านเป็น string
    restaurant_info = f"""
ชื่อร้าน: {restaurant['name']}
ที่อยู่: {restaurant['address'] or 'ไม่มีข้อมูล'}
เบอร์โทร: {restaurant['phone'] or 'ไม่มีข้อมูล'}
ราคา: {restaurant['price_min'] or '?'} - {restaurant['price_max'] or '?'} บาท
ประเภทอาหาร: {restaurant['cuisine'] or 'ไม่มีข้อมูล'}
รับจองโต๊ะ: {'มี' if restaurant['has_reservation'] else 'ไม่มี'}
Service charge: {'มี' if restaurant['service_charge'] else 'ไม่มี'}
ที่จอดรถ: {restaurant['parking'] or 'ไม่มีข้อมูล'}
Delivery: {', '.join(restaurant['delivery']) if restaurant['delivery'] else 'ไม่มี'}
เรื่องราวร้าน: {restaurant['story'] or 'ไม่มีข้อมูล'}
""".strip()

    messages = [
        {
            "role": "system",
            "content": """คุณคือผู้ช่วยตอบคำถามเกี่ยวกับร้านอาหาร
คุณมีข้อมูล 2 แหล่ง:
1. ข้อมูลร้าน — ที่อยู่ เบอร์ โทร ราคา การจอง ฯลฯ
2. รีวิวลูกค้า — ความคิดเห็นเกี่ยวกับอาหาร บริการ บรรยากาศ

ตอบโดยใช้ข้อมูลที่เกี่ยวข้องกับคำถาม
ถ้าไม่มีข้อมูลให้บอกตรงๆ ว่าไม่มีข้อมูล
ตอบเป็นภาษาไทย กระชับ"""
        },
        {
            "role": "user",
            "content": f"""ข้อมูลร้าน:
{restaurant_info}

รีวิวลูกค้า:
{review_text}

คำถาม: {question}"""
        }
    ]

    return chat(messages)