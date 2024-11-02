import os
from typing import final


@final
class Environment:
    PORT = os.environ["PORT"]
    POSTGRES_HOST = os.environ["POSTGRES_HOST"]
    POSTGRES_DB = os.environ["POSTGRES_DB"]
    POSTGRES_USER = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
    POSTGRES_PORT = os.environ["POSTGRES_PORT"]
    POSTGRES_ADDRESS = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
    OLLAMA_ADDRESS = os.environ["OLLAMA_ADDRESS"]
    OLLAMA_MODEL = os.environ["OLLAMA_MODEL"]
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
    OPENAI_MODEL = os.environ["OPENAI_MODEL"]
    CHROMA_HOST = os.environ["CHROMA_HOST"]
    ASSETS_PATH = os.environ["ASSETS_PATH"]
    VANNA_DDL_PATH = os.path.join(ASSETS_PATH, "vanna_ddl")
    VANNA_DOCS_PATH = os.path.join(ASSETS_PATH, "vanna_docs")
