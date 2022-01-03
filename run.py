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
        game.exit_game()
    except Exception:
        if not DEBUG:
            time = datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
            with open(f"exception-{time}.log", "w") as file:
                file.write(traceback.format_exc())
        else:
            print(traceback.print_exc())


if __name__ == '__main__':
    main()
