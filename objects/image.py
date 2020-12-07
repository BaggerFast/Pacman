from typing import Tuple, Union

import pygame as pg

from objects import DrawableObject


class ImageObject(DrawableObject):
    def __init__(self, game, image: Union[str, pg.Surface] = None, pos: Tuple[int, int] = (0, 0)) -> None:
        super().__init__(game)
        if isinstance(image, str):
            self.__filename = image
            self.image = pg.image.load(self.__filename).convert_alpha()
        elif isinstance(image, pg.Surface):
            self.image = image

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

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
        self.game.screen.blit(self.image, self.rect)

    def process_event(self, event: pg.event.Event) -> None:
        pass

    def process_logic(self) -> None:
        pass
