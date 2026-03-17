# Restaurant AI — Backend
HiwRaew AI is a restaurant review analyzer that transforms real customer feedback into actionable insights using a custom-built RAG pipeline. Each review is converted into a 1536-dimension vector via OpenAI Embeddings and stored in pgvector on PostgreSQL. When a user asks a question, the system retrieves only the most semantically relevant reviews using cosine similarity search, then passes them as context to GPT-4o-mini to generate summaries, pros/cons analysis, and Q&A responses — grounded entirely in real customer data.
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
