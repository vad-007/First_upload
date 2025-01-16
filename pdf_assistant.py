import typer
from typing import Optional, List
from phi.assistant import Assistant
from phi.storage.assistant.postgres import PgAssistantStorage as PostgresAssistant
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector2
import psycopg2
import time
import openai


import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set environment variable for API key
os.environ["GorqCloud_API_KEY"] = os.getenv("GorqCloud_API_KEY")
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# Define the knowledge base
knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    vector_db=PgVector2(collection="recipes", db_url=db_url),
)

# Load the knowledge base
knowledge_base.load()
storage = PostgresAssistant(table_name="pdf.assistant",db_url=db_url)

def pdf_assistant(new:bool=False,user:str="user"):
    run_id : Optional[str] = None

    if not new:
        existing_run_id = List[str]= storage.get_latest_run_id(user)
        if len(existing_run_id) > 0:
            run_id = existing_run_id[0]
            print(f"Resuming Run ID: {run_id}\n")




    assistant = Assistant(
    run_id=run_id,
    user_id= user,
    storage=storage,
    knowledge_bases=[knowledge_base],
    vector_db=PgVector2(collection="recipes", db_url=db_url),
    show_tool_calls=True,
    search_knowledge=True,
    read_chat_history=True,
)

    if run_id is None:
        run_id = assistant.run_id
        print(f"Run ID: {run_id}\n")
    else:
        print(f"Resuming Run ID: {run_id}\n")

    assistant.cli_app(markdown=True)

if __name__ == "__main__":
    typer.run(pdf_assistant)

# Define the assistant
'''assistant = Assistant(
    name="PDF Assistant",
    storage=PostgresAssistant(),
    knowledge_bases=[knowledge_base],
    vector_db=PgVector2()
)

# Define the CLI app
def pdf_assistant():
    run_id = assistant.run_id
    if run_id is None:
        run_id = assistant.start_run()
        print(f"Run ID: {run_id}\n")
    else:
        print(f"Resuming Run ID: {run_id}\n")

    assistant.cli_app(markdown=True)

def run_with_retry(func, retries=5, delay=1):
    for i in range(retries):
        try:
            return func()
        except openai.error.RateLimitError as e:
            print(f"Rate limit exceeded: {e}")
            if i < retries - 1:
                wait_time = delay * (2 ** i)  # Exponential backoff
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print("Max retries reached. Exiting.")
                raise'''

if __name__ == "__main__":
    typer.run(pdf_assistant)