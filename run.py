import sys
import pygame as pg
from game import Game
from misc import get_path


def pg_setup():
    __icon = pg.transform.scale(pg.image.load(get_path("ico", "png", "images")), (256, 256))
    pg.font.init()
    pg.mixer.init()
    pg.display.init()
    pg.display.set_icon(__icon)
    pg.display.set_caption("PACMAN")


def main():
    pg_setup()
    game = Game()
    game.main_loop()
    sys.exit(0)


if __name__ == "__main__":
    main()
