import pygame as pg

from misc.constants import Font
from objects.base import DrawableObject


class Text(DrawableObject):
    def __init__(self, game, text, size, rect=None, color=(255, 255, 255), font=Font.FILENAME):
        super().__init__(game)
        self.rect = rect if rect else pg.rect.Rect(0, 0, 0, 0)
        self.pos = rect if rect else (0, 0)
        self.size = size
        self.color = color
        self.font = pg.font.SysFont(font, self.size, True)
        self.update_text(text)

    def update_text(self, new_text):
        self.text = new_text
        self.surface = self.font.render(self.text, False, self.color)
        if type(self.rect) != tuple:
            topleft = self.rect.topleft
            self.rect = self.surface.get_rect()
            self.rect.topleft = topleft

    def update_position(self, a=()):
        self.pos = a

    def process_draw(self):
        self.game.screen.blit(self.surface, self.rect)
