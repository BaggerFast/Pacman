import sys
import pygame


from game import Game


if __name__ == '__main__':
    pygame.init()
    g = Game()
    g.main_loop()
    sys.exit(0)