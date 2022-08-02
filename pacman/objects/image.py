from typing import Tuple
import pygame as pg

from misc.misc import load_image
from misc.patterns.entities import RenderEntity
from pacman.objects import DrawableObject


class ImageObject(DrawableObject, RenderEntity):
    def __init__(self, image: str | pg.Surface = None, pos: Tuple[int, int] = (0, 0)) -> None:
        super().__init__()
        if isinstance(image, str):
            self.image = load_image(image).convert_alpha()
        elif isinstance(image, pg.Surface):
            self.image = image
        else:
            raise Exception
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    def scale(self, x, y) -> "ImageObject":
        self.image = pg.transform.scale(self.image, (x, y))
        topleft = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        return self

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

    def render(self, screen: pg.Surface) -> None:
        screen.blit(self.image, self.rect)
