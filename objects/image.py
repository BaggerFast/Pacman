from typing import Tuple, Union
import pygame as pg
from misc.interfaces import IDrawable
from objects.base import BaseObject


class ImageObject(BaseObject, IDrawable):

    def __init__(self, image: Union[str, pg.Surface] = None, pos: Tuple[int, int] = (0, 0), is_hidden=False):
        BaseObject.__init__(self)
        self.is_hidden = is_hidden
        self.image = self.parse_image(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    # region Public

    # region Implementation of IDrawable

    def process_draw(self, screen: pg.Surface) -> None:
        if not self.is_hidden:
            screen.blit(self.image, self.rect)

    # endregion

    @staticmethod
    def parse_image(image):
        if isinstance(image, str):
            return pg.image.load(image).convert_alpha()
        if isinstance(image, pg.Surface):
            return image

    def scale(self, x, y) -> None:
        self.image = pg.transform.scale(self.image, (x, y))
        topleft = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft

    def smooth_scale(self, x, y) -> None:
        self.image = pg.transform.smoothscale(self.image, (x, y))
        topleft = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft

    def rotate(self, angle) -> None:
        self.image = pg.transform.rotate(self.image, angle)
        topleft = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft

    # endregion
