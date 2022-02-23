from typing import Tuple, Union

import pygame as pg

from misc.interfaces.object_interfaces import IDrawable
from objects.base import BaseObject


class ImageObject(BaseObject, IDrawable):

    def __init__(self, game, image: Union[str, pg.Surface] = None, pos: Tuple[int, int] = (0, 0)):
        BaseObject.__init__(self, game)
        self.image = self.parse_image(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    @staticmethod
    def parse_image(image):
        if isinstance(image, str):
            return pg.image.load(image).convert_alpha()
        elif isinstance(image, pg.Surface):
            return image

    def scale(self, x, y) -> None:
        self.image = pg.transform.scale(self.image, (x, y))
        topleft = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft

    def smoothscale(self, x, y) -> None:
        self.image = pg.transform.smoothscale(self.image, (x, y))
        topleft = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft

    def rotate(self, angle) -> None:
        self.image = pg.transform.rotate(self.image, angle)
        topleft = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft

    def process_draw(self) -> None:
        if not self.is_hidden:
            self.game.screen.blit(self.image, self.rect)
