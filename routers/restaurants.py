from fastapi import APIRouter
from app.db import get_connection
from app.services.ingestion import ingest_reviews
from app.services.cache import invalidate_cache

router = APIRouter()

@router.post("/")
def create_restaurant(body: dict):
    conn =get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO restaurants
            (name, address, phone, price_min, price_max,cuisine,
            has_reservation, service_charge,
            story, google_map_url, image_url, delivery) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *""",
            (
                body["name"],
                body["address"],
                body["phone"],
                body["price_min"],
                body["price_max"],
                body["cuisine"],
                body["has_reservation"],
                body["service_charge"],
                body["story"],
                body["google_map_url"],
                body["image_url"],
                body["delivery"]
            )
        )
        conn.commit()
        row = cur.fetchone()     # เพิ่มบรรทัดนี้
        return row        
    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()


@router.post("/{restaurant_id}/reviews")
def create_review(restaurant_id: int, body: dict):
    conn =get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO reviews
            (restaurant_id,source,author, rating, content,reviewed_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *""",
            (
                restaurant_id,
                body["source"],
                body["author"],
                body["rating"],
                body["content"],
                body["reviewed_at"]
            )
        )
        conn.commit()
        row = cur.fetchone()
        return row   
    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()
@router.post("/{restaurant_id}/ingest")
def ingest(restaurant_id: int):
    result = ingest_reviews(restaurant_id)
    return result       
@router.get("/{restaurant_id}")
def get_restaurant(restaurant_id: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT * FROM restaurants WHERE id = %s",
            (restaurant_id,)
        )
        row = cur.fetchone()
        if not row:
            return {"error": "ไม่พบร้านนี้"}
        return row
    finally:
        conn.close()
@router.get("/")
def get_restaurants():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT * FROM restaurants ORDER BY created_at DESC"
        )
        return cur.fetchall()
    finally:
        conn.close()