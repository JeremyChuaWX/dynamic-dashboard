import os

from chromadb import HttpClient
from vanna.chromadb import ChromaDB_VectorStore
from vanna.ollama import Ollama
from vanna.openai import OpenAI_Chat
from vanna.utils import deterministic_uuid

from database import Database
from environment import Environment


class Vanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, db: Database):
        ChromaDB_VectorStore.__init__(
            self,
            config={
                "client": HttpClient(host=Environment.CHROMA_HOST),
            },
        )

        OpenAI_Chat.__init__(
            self,
            config={
                "api_key": Environment.OPENAI_API_KEY,
                "model": Environment.OPENAI_MODEL,
            },
        )

        self.connect_to_postgres(
            host=Environment.POSTGRES_HOST,
            dbname=Environment.POSTGRES_DB,
            user=Environment.POSTGRES_USER,
            password=Environment.POSTGRES_PASSWORD,
            port=Environment.POSTGRES_PORT,
        )

        self.idempotent_add_vanna_docs(
            db, Environment.VANNA_DDL_PATH, "ddl", self.ddl_collection
        )
        self.idempotent_add_vanna_docs(
            db, Environment.VANNA_DOCS_PATH, "doc", self.documentation_collection
        )

    def idempotent_add_vanna_docs(self, db: Database, path: str, type: str, collection):
        for filename in os.listdir(path):
            with open(os.path.join(path, filename)) as f:
                content = f.read()
            id = deterministic_uuid(content)
            if db.check_document_exists(id, type):
                print(
                    "idempotent_add_vanna_docs:",
                    f"{type} {filename} already exists, skipping ...",
                )
                continue
            collection.add(
                documents=content,
                embeddings=self.generate_embedding(content),
                ids=id + f"-{type}",
            )
            db.insert_document(id, type)


class OllamaVanna(ChromaDB_VectorStore, Ollama):
    def __init__(self, db: Database):
        ChromaDB_VectorStore.__init__(
            self,
            config={
                "client": HttpClient(host=Environment.CHROMA_HOST),
            },
        )

        Ollama.__init__(
            self,
            config={
                "ollama_host": Environment.OLLAMA_ADDRESS,
                "model": Environment.OLLAMA_MODEL,
            },
        )

        self.connect_to_postgres(
            host=Environment.POSTGRES_HOST,
            dbname=Environment.POSTGRES_DB,
            user=Environment.POSTGRES_USER,
            password=Environment.POSTGRES_PASSWORD,
            port=Environment.POSTGRES_PORT,
        )

        self.idempotent_add_vanna_docs(
            db, Environment.VANNA_DDL_PATH, "ddl", self.ddl_collection
        )
        self.idempotent_add_vanna_docs(
            db, Environment.VANNA_DOCS_PATH, "doc", self.documentation_collection
        )

    def idempotent_add_vanna_docs(self, db: Database, path: str, type: str, collection):
        for filename in os.listdir(path):
            with open(os.path.join(path, filename)) as f:
                content = f.read()
            id = deterministic_uuid(content)
            if db.check_document_exists(id, type):
                print(
                    "idempotent_add_vanna_docs:",
                    f"{type} {filename} already exists, skipping ...",
                )
                continue
            collection.add(
                documents=content,
                embeddings=self.generate_embedding(content),
                ids=id + f"-{type}",
            )
            db.insert_document(id, type)
