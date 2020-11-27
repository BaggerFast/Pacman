import sys
import pygame as pg
from Pacman import Pacman


def main():
    pg.display.init()
    pg.font.init()
    pg.mixer.init()
    game = Pacman()
    game.main_loop()
    sys.exit(0)


if __name__ == '__main__':
    main()
