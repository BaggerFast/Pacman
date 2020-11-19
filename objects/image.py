import pygame

from objects.base import DrawableObject


class ImageObject(DrawableObject):
    filename = 'images/basketball.png'

    def __init__(self, game, filename=None, x=None, y=None):
        super().__init__(game)
        if filename:
            self.filename = filename
        self.image = pygame.image.load(self.filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x if x else 0
        self.rect.y = y if y else 0

    def scale(self, x, y):
        self.image = pygame.transform.scale(self.image, (x, y))
        topleft = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)
        topleft = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft

    def process_draw(self):
        self.game.screen.blit(self.image, self.rect)