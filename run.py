import sys
from datetime import datetime
import traceback
import pygame as pg
from game import Game
from misc import DEBUG


def main():
    pg.display.init()
    pg.font.init()
    pg.mixer.init()
    try:
        game: Game = Game()
        game.main_loop()
    except Exception:
        print(traceback.format_exc())
        if not DEBUG:
            with open(f"exception-{datetime.now().strftime('%m-%d-%Y-%H-%M-%S')}.log", "w") as file:
                file.write(traceback.format_exc())
        game.exit_game()


if __name__ == '__main__':
    main()
