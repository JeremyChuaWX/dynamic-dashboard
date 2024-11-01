from typing import Optional

from sqlalchemy import create_engine, text

from environment import Environment


class Database:
    def __init__(self):
        self.engine = create_engine(
            Environment.POSTGRES_ADDRESS,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=3600,
            connect_args={"connect_timeout": 5},
        )

    def check_document_exists(self, id: str, type: str):
        query = text("""
        SELECT
            COUNT(*) AS count
        FROM
            documents
        WHERE 1 = 1
            AND type = :type
            AND id = :id
        ;
        """)
        with self.engine.begin() as connection:
            res = connection.execute(
                query,
                {
                    "type": type,
                    "id": id,
                },
            )
        return res.fetchone()[0] > 0

    def insert_document(self, id: str, type: str):
        query = text("""
        INSERT INTO documents (
            type,
            id
        ) VALUES (
            :type,
            :id
        ) RETURNING
            id
        ;
        """)
        with self.engine.begin() as connection:
            res = connection.execute(
                query,
                {
                    "type": type,
                    "id": id,
                },
            )
        return res.fetchone()[0]

    def insert_visualisation(self, question: str):
        query = text("""
        INSERT INTO visualisations (
            question
        ) VALUES (
            :question
        ) RETURNING
            id
        ;
        """)
        with self.engine.begin() as connection:
            res = connection.execute(
                query,
                {
                    "question": question,
                },
            )
        return res.fetchone()[0]

    def update_visualisation(
        self,
        id: str,
        question: Optional[str],
        sql_query: Optional[str],
        plotly_code: Optional[str],
    ):
        query = text("""
        UPDATE visualisations
        SET
            question = COALESCE(:question, question),
            sql_query = COALESCE(:sql_query, sql_query),
            plotly_code = COALESCE(:plotly_code, plotly_code),
        WHERE
            id = :id
        RETURNING
            id
        ;
        """)
        with self.engine.begin() as connection:
            res = connection.execute(
                query,
                {
                    "id": id,
                    "question": question,
                    "sql_query": query,
                    "plotly_code": plotly_code,
                },
            )
        return res.fetchone()[0]
