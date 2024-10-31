from environment import Environment
from vanna.chromadb import ChromaDB_VectorStore
from vanna.ollama import Ollama


class Vanna(ChromaDB_VectorStore, Ollama):
    def __init__(self):
        ChromaDB_VectorStore.__init__(
            self,
            config={
                "path": Environment.CHROMADB_PATH,
            },
        )
        Ollama.__init__(
            self,
            config={
                "host": Environment.OLLAMA_HOST,
                "model": Environment.OLLAMA_MODEL,
            },
        )
        self.connect_to_postgres(
            host=Environment.POSTGRES_HOST,
            dbname=Environment.POSTGRES_DB,
            user=Environment.POSTRES_USER,
            password=Environment.POSGRES_PASSWORD,
            port=Environment.POSTGRES_PORT,
        )
        self.train(ddl=Environment.VANNA_DDL_PATH)
        self.train(documentation=Environment.VANNA_DOCUMENTATION_PATH)
