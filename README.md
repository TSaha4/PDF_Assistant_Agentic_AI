# PDF Assistant with Groq and Phi

## Overview

This project is a PDF-based knowledge assistant built using **Phi**, **PgVector**, and **Groq API**.  
It allows you to load PDF documents into a vector database and query them interactively through a CLI assistant.

The project has been updated to run PostgreSQL with **pgvector** using **Docker**.

---

## Features

- Load PDF documents into a PostgreSQL vector database (`pgvector`)
- Use **Groq API** as the language model backend
- Use **GeminiEmbedder** from Google for embeddings
- CLI-based interactive assistant
- Stores user sessions in PostgreSQL for continuity

---

## Requirements

- Python 3.10+
- Docker
- PostgreSQL 16 with pgvector
- API Keys:
  - `GROQ_API_KEY`
  - `GOOGLE_API_KEY`

---

## Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd PDF_Assistant
```

2. Create a Python virtual environment:
```bash
conda create -n pdf_assistant python=3.10 -y
conda activate pdf_assistant
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up `.env` file in project root:
```env
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
```

## Docker Setup for PostgreSQL with pgvector

Run PostgreSQL with pgvector in Docker:
```bash
docker run -d \
  -e POSTGRES_DB=ai \
  -e POSTGRES_USER=ai \
  -e POSTGRES_PASSWORD=ai \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v pgvolume:/var/lib/postgresql/data \
  -p 5532:5432 \
  --name pgvector \
  phidata/pgvector:16
```

Verify Docker container is running:
```bash
docker ps
```

## Usage

Run the assistant:
```bash
python assistant.py
```

* The assistant will read the PDF(s) in `knowledge_base`.
* Interact with the assistant via CLI.
* Supports searching knowledge base and remembering previous sessions.

## Notes

* The previous version used OpenAI API, now switched to Groq API (free tier available).
* PostgreSQL database should be running before executing the assistant.
* If you update embeddings (e.g., using GeminiEmbedder), you may need to drop and recreate the vector table to avoid dimension mismatches.
```sql
-- Example: drop table in psql
DROP TABLE ai.recipes;
```

## Project Structure
```
PDF_Assistant/
├─ assistant.py
├─ requirements.txt
├─ .env
├─ README.md
└─ venv/
```

## Git Ignore

* Virtual environment
* `.env`
* Logs
* Cache files
* Docker overrides

Refer to `.gitignore` for details.