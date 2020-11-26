import pygame as pg

from objects import DrawableObject


class ImageObject(DrawableObject):
    def __init__(self, game, filename=None, x=None, y=None):
        super().__init__(game)
        if filename:
            self.__filename = filename
        self.image = pg.image.load(self.__filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x if x else 0
        self.rect.y = y if y else 0

    def scale(self, x, y):
        self.image = pg.transform.scale(self.image, (x, y))
        topleft = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft

    def rotate(self, angle):
        self.image = pg.transform.rotate(self.image, angle)
        topleft = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft

    def process_draw(self):
        self.game.screen.blit(self.image, self.rect)
