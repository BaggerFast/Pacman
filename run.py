from pygame import display, font, mixer, transform

from pacman import Game
from pacman.misc import load_image


def pg_setup():
    icon = transform.scale(load_image("ico"), (256, 256))
    font.init()
    mixer.init()
    display.init()
    display.set_icon(icon)
    display.set_caption("PACMAN")


def main():
    pg_setup()
    game = Game()
    game.main_loop()


if __name__ == "__main__":
    main()
