from app.db import get_connection
from app.services.embeddings import embed_many

def ingest_reviews(restaurant_id: int):
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # 1. ดึงรีวิวที่ยังไม่ได้ embed
        cur.execute(
            """SELECT r.id, r.content 
               FROM reviews r
               WHERE r.restaurant_id = %s
               AND r.id NOT IN (
                   SELECT DISTINCT review_id 
                   FROM review_embeddings 
                   WHERE restaurant_id = %s
               )""",
            (restaurant_id, restaurant_id)
        )
        reviews = cur.fetchall()

        if not reviews:
            return {"message": "ไม่มีรีวิวใหม่ที่ต้อง ingest"}

        # 2. แปลงเป็น vector ทีเดียวทั้งหมด
        texts = [r["content"] for r in reviews]
        vectors = embed_many(texts)

        # 3. บันทึกลง review_embeddings
        for review, vector in zip(reviews, vectors):
            cur.execute(
                """INSERT INTO review_embeddings
                   (review_id, restaurant_id, content_chunk, embedding)
                   VALUES (%s, %s, %s, %s::vector)""",
                (
                    review["id"],
                    restaurant_id,
                    review["content"],
                    str(vector)   # แปลง list → string ก่อนส่ง pgvector
                )
            )

        conn.commit()
        return {"message": f"ingest สำเร็จ {len(reviews)} รีวิว"}

    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        conn.close()