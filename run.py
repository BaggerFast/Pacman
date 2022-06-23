import os
import traceback
from datetime import datetime
from game import Game
from config.settings import DEBUG, Dir


def parse_exceptions():
    if DEBUG:
        print(traceback.print_exc())
        return
    if not os.path.exists(Dir.LOG):
        os.makedirs(Dir.LOG)
    with open(f"{Dir.LOG}/{datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}.log", "w") as file:
        file.write(traceback.format_exc())


def main():
    try:
        game = Game()
        game.main_loop()
    except Exception:
        parse_exceptions()


if __name__ == '__main__':
    main()
