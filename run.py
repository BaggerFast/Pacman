import sys
import pygame as pg
from game import Game


def main():
    pg.display.init()
    pg.font.init()
    pg.mixer.init()
    game = Game()
    game.main_loop()
    sys.exit(0)


if __name__ == "__main__":
    main()
