from app.db import get_connection
from app.services.embeddings import embed_text

def retrieve_reviews(restaurant_id: int,
                    query: str,
                    top_k: int = 5) -> list[dict]:
    conn = get_connection()
    cur = conn.cursor()
    try:
        # แปลง query เป็น vector ก่อน
        query_vector = embed_text(query)

        cur.execute(
            """SELECT 
                content_chunk,
                1 - (embedding <=> %s::vector) AS similarity
               FROM review_embeddings
               WHERE restaurant_id = %s
               ORDER BY embedding <=> %s::vector
               LIMIT %s""",
            (str(query_vector), restaurant_id, str(query_vector), top_k)
        )
        return cur.fetchall()
    finally:
        conn.close()