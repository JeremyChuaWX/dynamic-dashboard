from app import App
from database import Database
from environment import Environment
from llm import Vanna
from server import server


def main():
    database = Database()
    vanna = Vanna(database)
    app = App(server, vanna, database)
    server.run(host="0.0.0.0", port=Environment.PORT)


if __name__ == "__main__":
    main()
