import sys
import pygame as pg

from data_core import PathManager
from game import Game


def pg_setup():
    icon_path = PathManager.get_image_path("ico")
    icon = pg.transform.scale(pg.image.load(icon_path), (256, 256))
    pg.font.init()
    pg.mixer.init()
    pg.display.init()
    pg.display.set_icon(icon)
    pg.display.set_caption("PACMAN")


def main():
    pg_setup()
    game = Game()
    game.main_loop()
    sys.exit(0)


if __name__ == "__main__":
    main()
