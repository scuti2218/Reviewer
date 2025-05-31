# from libs import SystemInfo, Player
from controllers import Controller
from services.TCL import check_tcl_path

def main():
    if not check_tcl_path():
        return
    controller = Controller()
    controller.update()

if __name__ == "__main__":
    main()