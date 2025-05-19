# from libs import SystemInfo, Player
from app import Controller, View, Model
from app.services.TCL import check_tcl_path


def main():
    if check_tcl_path():
        view = View()
        model = Model()
        controller = Controller(view, model)
        controller.update()
    # player: Player = Player()
    # window: SystemInfo = SystemInfo(player)
    # window.start()

if __name__ == "__main__":
    main()