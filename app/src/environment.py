import os
from typing import final


@final
class Environment:
    PORT = os.environ["PORT"]
    POSTGRES_HOST = os.environ["POSTGRES_HOST"]
    POSTGRES_DB = os.environ["POSTGRES_DB"]
    POSTRES_USER = os.environ["POSTRES_USER"]
    POSGRES_PASSWORD = os.environ["POSGRES_PASSWORD"]
    POSTGRES_PORT = os.environ["POSTGRES_PORT"]
    OLLAMA_HOST = os.environ["OLLAMA_HOST"]
    OLLAMA_MODEL = os.environ["OLLAMA_MODEL"]
    CHROMADB_PATH = os.environ["CHROMADB_PATH"]
    VANNA_DDL_PATH = os.environ["VANNA_DDL_PATH"]
    VANNA_DOCUMENTATION_PATH = os.environ["VANNA_DOCUMENTATION_PATH"]
