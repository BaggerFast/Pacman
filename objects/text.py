import pygame as pg

from misc import Font
from objects import DrawableObject


class Text(DrawableObject):
    def __init__(self, game, text, size, rect=None, color=(255, 255, 255), font=Font.ALTFONT):
        super().__init__(game)
        self.rect = rect if rect else pg.rect.Rect(0, 0, 0, 0)
        self.pos = rect if rect else (0, 0)
        self.size = size
        self.color = color
        self.font = pg.font.Font(font, self.size)
        self.update_text(text)

    def update_text(self, new_text):
        self.text = new_text
        self.surface = self.font.render(self.text, False, self.color)
        if type(self.rect) != tuple:
            topleft = self.rect.topleft
            self.rect = self.surface.get_rect()
            self.rect.topleft = topleft

    def update_color(self, new_color):
        self.color = new_color
        self.surface = self.font.render(self.text, False, self.color)
        if type(self.rect) != tuple:
            topleft = self.rect.topleft
            self.rect = self.surface.get_rect()
            self.rect.topleft = topleft

    def update_position(self, a=()):
        self.pos = a

    def process_draw(self):
        self.game.screen.blit(self.surface, self.rect)

    def process_event(self, event):
        pass

    def process_logic(self):
        pass
