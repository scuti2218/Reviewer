from libs import SystemInfo, Player

def main():
    player: Player = Player()
    window: SystemInfo = SystemInfo(player)
    window.start()

if __name__ == "__main__":
    main()