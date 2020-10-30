#!/usr/bin/env python3

import sys
import pygame

from game import Game


def main():
    pygame.init()
    pygame.font.init()
    Game().main_loop()
    sys.exit(0)


if __name__ == '__main__':
    main()
