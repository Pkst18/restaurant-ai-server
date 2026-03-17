# Restaurant AI — Backend

FastAPI backend สำหรับระบบวิเคราะห์รีวิวร้านอาหารด้วย AI

## Tech Stack

- **Python** + **FastAPI**
- **PostgreSQL** + **pgvector** (Supabase)
- **OpenAI API** (embeddings + GPT-4o-mini)
- **RAG Pipeline** (custom implementation)

## Features

- `POST /restaurants` — เพิ่มร้านอาหาร
- `POST /restaurants/:id/reviews` — เพิ่มรีวิว
- `POST /restaurants/:id/ingest` — แปลงรีวิวเป็น vector embeddings
- `GET  /restaurants/:id/summary` — สรุปรีวิวด้วย AI + caching
- `GET  /restaurants/:id/insights` — วิเคราะห์ pros/cons/เมนู + caching
- `POST /restaurants/:id/ask` — Q&A chatbot จากข้อมูลร้านและรีวิว
