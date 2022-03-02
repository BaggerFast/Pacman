import pygame as pg

from misc.constants import EvenType
from misc.keyboards.base import BaseKeyboard


class PacmanKeyboard(BaseKeyboard):

    def __init__(self):
        self.keys_control = [
            self.KeyControl([pg.K_a, pg.K_LEFT], EvenType.GoLeft),
            self.KeyControl([pg.K_d, pg.K_RIGHT], EvenType.GoRight),
            self.KeyControl([pg.K_w, pg.K_UP], EvenType.GoUp),
            self.KeyControl([pg.K_s, pg.K_DOWN], EvenType.GoDown),
        ]
        super().__init__()
