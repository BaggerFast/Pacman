import sys
from datetime import datetime
import traceback
import pygame as pg
from game import Game


def main():
    pg.display.init()
    pg.font.init()
    pg.mixer.init()
    game: Game
    try:
        game = Game()
        game.main_loop()
    except Exception:
        print(traceback.format_exc())
        with open(f"exception-{datetime.now().strftime('%m-%d-%Y-%H-%M-%S')}.log", "w") as file:
            file.write(traceback.format_exc())
        game.exit_game()

    sys.exit(0)


if __name__ == '__main__':
    main()
