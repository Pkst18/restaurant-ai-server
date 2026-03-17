from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# ใช้แปลงคำถามจาก user เป็น embedding vector เพื่อใช้ในการค้นหาในฐานข้อมูล
def embed_text(text: str) -> list[float]:
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding
#แปลงรีวิวหลายๆ อันเป็น embedding vector ทีเดียว เพื่อประสิทธิภาพที่ดีกว่า
def embed_many(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(
        input=texts,
        model="text-embedding-3-small"
    )
    return [item.embedding for item in response.data]