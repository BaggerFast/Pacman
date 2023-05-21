from typing import Tuple, Union

from PIL import Image, ImageFilter
from pygame import Rect, Surface
from pygame import image as img
from pygame import transform

from pacman.data_core import IDrawable
from pacman.misc import load_image

from .rect_obj import RectObj


class ImgObj(RectObj, IDrawable):
    def __init__(self, image: Union[str, Surface] = None, pos: Tuple[int, int] = (0, 0)) -> None:
        if isinstance(image, str):
            self.image = load_image(image).convert_alpha()
        elif isinstance(image, Surface):
            self.image = image

        super().__init__(self.image.get_rect())
        self.rect.x, self.rect.y = pos

    def scale(self, x, y) -> "ImgObj":
        self.image = transform.scale(self.image, (x, y))
        topleft = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        return self

    def smoothscale(self, x, y) -> "ImgObj":
        self.image = transform.smoothscale(self.image, (x, y))
        topleft = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        return self

    def blur(self, blur_count: int = 5) -> "ImgObj":
        impil = Image.frombytes("RGBA", self.rect.size, img.tostring(self.image, "RGBA"))
        impil = impil.filter(ImageFilter.GaussianBlur(radius=blur_count))
        self.image = img.fromstring(impil.tobytes(), impil.size, "RGBA").convert()
        return self

    def swap_color(self, from_color, to_color) -> "ImgObj":
        for x in range(self.image.get_width()):
            for y in range(self.image.get_height()):
                if self.image.get_at((x, y)) == from_color:
                    self.image.set_at((x, y), to_color)
        return self

    def rotate(self, angle) -> "ImgObj":
        self.image = transform.rotate(self.image, angle)
        topleft = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        return self

    def rect(self) -> Rect:
        return self.image.get_rect()

    def draw(self, screen: Surface) -> None:
        screen.blit(self.image, self.rect)
