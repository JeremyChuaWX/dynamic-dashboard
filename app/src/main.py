from vanna import Vanna
from app import App


def main():
    vn = Vanna()
    app = App(vn)
    app.start()


if __name__ == "__main__":
    main()
