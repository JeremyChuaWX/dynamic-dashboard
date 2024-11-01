from llm import Vanna
from database import Database
from app import App


def main():
    db = Database()
    vn = Vanna(db)
    app = App(vn, db)
    app.start()


if __name__ == "__main__":
    main()
