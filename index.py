from app import Controller, View, Model


def main():
    view = View()
    model = Model()
    controller = Controller(view, model)
    controller.update()

if __name__ == "__main__":
    main()