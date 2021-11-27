import pygame as pg
from misc import EvenType
from misc.keyboards.base import BaseKeyboard


class MenuKeyboard(BaseKeyboard):

    def configure(self):

        self.data_keys = [
            self.KeyControl([pg.K_SPACE, pg.K_RETURN], EvenType.PressBtn),
            self.KeyControl([pg.K_w, pg.K_UP], EvenType.PreviousBtn),
            self.KeyControl([pg.K_s, pg.K_DOWN], EvenType.NextBtn),
        ]
