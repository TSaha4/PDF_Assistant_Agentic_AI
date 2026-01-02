# PDF Assistant with Groq and Phi

## Overview

This project is a PDF-based knowledge assistant built using **Phi**, **PgVector**, and **Groq API**.  
It allows you to load PDF documents into a vector database and query them interactively through a CLI assistant.

The project uses **PostgreSQL with pgvector** via **Docker** for vector storage and has been updated to handle embedding dimension mismatches.

Huge thanks to Krish Nair course for showing me the ropes.

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

## Important Docker/Database Changes

During development, we encountered embedding dimension mismatches because the previous table stored embeddings with 1536 dimensions, while the new embeddings (GeminiEmbedder) have 768 dimensions.

To fix this:

1. Drop the old table in PostgreSQL:
```sql
-- Connect to the database
\c ai
-- Drop the old table
DROP TABLE ai.recipes;
```

2. Restart the assistant. It will recreate the table automatically with the correct embedding dimensions.

This ensures the vector database works correctly with the new embeddings and avoids `expected 1536 dimensions, not 768` errors.

## Usage

Run the assistant:
```bash
python assistant.py
```

* The assistant will read the PDF(s) in `knowledge_base`.
* Interact with the assistant via CLI.
* Supports searching knowledge base and remembering previous sessions.

## Project Structure
```
PDF_Assistant/
├─ assistant.py
├─ requirements.txt
├─ .env
├─ README.md
└─ venv/
```
