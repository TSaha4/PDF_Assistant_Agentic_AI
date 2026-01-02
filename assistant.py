import typer
from typing import Optional

from phi.agent import Agent
from phi.model.groq import Groq

from phi.storage.agent.postgres import PgAgentStorage
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector2
from phi.embedder.google import GeminiEmbedder

import os
from dotenv import load_dotenv

load_dotenv()

# Load API keys
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

if not os.environ["GROQ_API_KEY"]:
    raise ValueError("Missing GROQ_API_KEY in .env")

if not os.environ["GOOGLE_API_KEY"]:
    raise ValueError("Missing GOOGLE_API_KEY in .env")

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    vector_db=PgVector2(
        collection="recipes",
        db_url=db_url,
        embedder=GeminiEmbedder()
    ),
    chunk=False
)

knowledge_base.load()

storage = PgAgentStorage(
    table_name="pdf_assistant",
    db_url=db_url
)


def get_existing_run_id(user: str) -> Optional[str]:
    """Fetch first previous run id if available."""

    if not hasattr(storage, "list_runs"):
        return None

    runs = storage.list_runs(user_id=user)

    if not runs:
        return None

    first = runs[0]

    # list_runs may return dicts or objects — handle both
    return getattr(first, "run_id", first.get("run_id") if isinstance(first, dict) else None)


def pdf_assistant(new: bool = False, user: str = "user"):
    run_id: Optional[str] = None

    if not new:
        run_id = get_existing_run_id(user)

    assistant = Agent(
        model=Groq(id="llama-3.3-70b-versatile"),
        run_id=run_id,
        user_id=user,
        knowledge_base=knowledge_base,
        storage=storage,
        show_tool_calls=True,
        search_knowledge=True,
        read_chat_history=True,
    )

    if run_id is None:
        print(f"Started Run: {assistant.run_id}\n")
    else:
        print(f"Continuing Run: {run_id}\n")

    assistant.cli_app(markdown=True)


if __name__ == "__main__":
    typer.run(pdf_assistant)
