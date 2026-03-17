from app.db import get_connection

def get_cache(restaurant_id: int, cache_type: str) -> str | None:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """SELECT result FROM ai_cache
               WHERE restaurant_id = %s 
               AND cache_type = %s
               ORDER BY created_at DESC
               LIMIT 1""",
            (restaurant_id, cache_type)
        )
        row = cur.fetchone()
        return row["result"] if row else None
    finally:
        conn.close()

def set_cache(restaurant_id: int, cache_type: str, result: str):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # ลบ cache เก่าก่อน แล้วค่อยเพิ่มใหม่
        cur.execute(
            """DELETE FROM ai_cache
               WHERE restaurant_id = %s 
               AND cache_type = %s""",
            (restaurant_id, cache_type)
        )
        cur.execute(
            """INSERT INTO ai_cache 
               (restaurant_id, cache_type, result)
               VALUES (%s, %s, %s)""",
            (restaurant_id, cache_type, result)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
    finally:
        conn.close()

def invalidate_cache(restaurant_id: int):
    """เรียกตอนมีรีวิวใหม่เข้ามา — ล้าง cache ทั้งหมดของร้านนั้น"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM ai_cache WHERE restaurant_id = %s",
            (restaurant_id,)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
    finally:
        conn.close()