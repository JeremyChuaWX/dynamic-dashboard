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

    def insert_visualisation(self, question: str, sql_query: str, plotly_code: str):
        query = text("""
        INSERT INTO visualisations (
            question,
            sql_query,
            plotly_code
        ) VALUES (
            :question,
            :sql_query,
            :plotly_code
        ) RETURNING
            id
        ;
        """)
        with self.engine.begin() as connection:
            res = connection.execute(
                query,
                {
                    "question": question,
                    "sql_query": sql_query,
                    "plotly_code": plotly_code,
                },
            )
        return res.fetchone()[0]

    def select_one_visualisation(self, id: str):
        query = text("""
        SELECT
            id,
            question,
            sql_query,
            plotly_code
        FROM
            visualisations
        WHERE 1=1
            AND id = :id
        ;
        """)
        with self.engine.begin() as connection:
            res = connection.execute(
                query,
                {
                    "id": id,
                },
            )
        return res.fetchone()

    def select_many_visualisations(self):
        query = text("""
        SELECT
            id,
            question,
            sql_query,
            plotly_code
        FROM
            visualisations
        ;
        """)
        with self.engine.begin() as connection:
            res = connection.execute(query)
        return res.fetchall()

    def delete_one_visualisation(self, id: str):
        query = text("""
        DELETE FROM
            visualisations
        WHERE 1=1
            AND id = :id
        ;
        """)
        with self.engine.begin() as connection:
            res = connection.execute(
                query,
                {
                    "id": id,
                },
            )
        return res.fetchone()[0]

    def insert_layout(self, layout_str):
        query = text("""
        INSERT INTO layouts (
            layout
        )
        VALUES (
            :layout
        ) RETURNING (
            id
        )
        ;
        """)
        with self.engine.begin() as connection:
            res = connection.execute(
                query,
                {
                    "layout": layout_str,
                },
            )
        return res.fetchone()[0]

    def select_latest_layout(self):
        query = text("""
        SELECT
            layout
        FROM
            layouts
        ORDER BY
            created_at DESC
        LIMIT
            1
        ;
        """)
        with self.engine.begin() as connection:
            res = connection.execute(query).fetchone()
        return None if not res else res[0]
