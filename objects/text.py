import pygame
import pygame as pg

from objects.base import DrawableObject


class Text(DrawableObject):
    def __init__(self, game, text, size, rect=None, color=(255, 255, 255), font="Arial"):
        super().__init__(game)
        if rect:
            self.rect = pygame.rect.Rect(0, 0, rect[0], rect[1])
        else:
            self.rect = pygame.rect.Rect(0, 0, 0, 0)
        self.pos = rect if rect else (0, 0)
        self.size = size
        self.color = color
        self.font = pg.font.SysFont(font, self.size, True)
        self.update_text(text)

    def update_text(self, new_text, centered=True):
        self.text = new_text
        self.surface = self.font.render(self.text, False, self.color)
        new_rect = self.surface.get_rect()
        if centered:
            new_rect.center = self.rect.center
        else:
            new_rect.topleft = self.rect.topleft
        self.rect = new_rect

    def update_position(self, a=()):
        self.pos = a

    def process_draw(self):
        self.game.screen.blit(self.surface, self.rect)
