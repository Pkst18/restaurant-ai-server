from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.db import get_connection
from app.routers import restaurants, ai

load_dotenv()

app = FastAPI()

# เพิ่มตรงนี้
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/health/db")
def health_db():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT NOW() as time")
        row = cur.fetchone()
        conn.close()
        return {"status": "ok", "db_time": str(row["time"])}
    except Exception as e:
        return {"status": "error", "message": str(e)}

app.include_router(restaurants.router, prefix="/restaurants")
app.include_router(ai.router, prefix="/restaurants")