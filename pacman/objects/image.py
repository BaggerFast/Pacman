from typing import Tuple, Union
import pygame as pg
from PIL import Image, ImageFilter
from pygame import Surface, Rect
from pacman.data_core.interfaces import IDrawable
from pacman.misc.loaders import load_image
from pacman.objects import MovementObject


class ImageObject(MovementObject, IDrawable):
    def __init__(self, image: Union[str, pg.Surface] = None, pos: Tuple[int, int] = (0, 0)) -> None:
        super().__init__()
        if isinstance(image, str):
            self.image = load_image(image).convert_alpha()
        elif isinstance(image, pg.Surface):
            self.image = image

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    def scale(self, x, y) -> "ImageObject":
        self.image = pg.transform.scale(self.image, (x, y))
        topleft = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        return self

    def smoothscale(self, x, y) -> "ImageObject":
        self.image = pg.transform.smoothscale(self.image, (x, y))
        topleft = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        return self

    def blur(self, blur_count: int = 5) -> "ImageObject":
        impil = Image.frombytes('RGBA', self.rect.size, pg.image.tostring(self.image, 'RGBA'))
        impil = impil.filter(ImageFilter.GaussianBlur(radius=blur_count))
        self.image = pg.image.fromstring(impil.tobytes(), impil.size, "RGBA").convert()
        return self

    def swap_color(self, from_color, to_color) -> "ImageObject":
        for x in range(self.image.get_width()):
            for y in range(self.image.get_height()):
                if self.image.get_at((x, y)) == from_color:
                    self.image.set_at((x, y), to_color)
        return self

    def rotate(self, angle) -> "ImageObject":
        self.image = pg.transform.rotate(self.image, angle)
        topleft = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        return self

    def rect(self) -> Rect:
        return self.image.get_rect()

    def draw(self, screen: Surface) -> None:
        screen.blit(self.image, self.rect)
