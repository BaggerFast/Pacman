import pygame as pg
from misc import Font
from objects import DrawableObject
from typing import Tuple


class Text(DrawableObject):
    def __init__(self, game, text: str = "",
                 size: Tuple[int, int] = (0, 0),
                 rect: pg.Rect = pg.rect.Rect(0, 0, 0, 0),
                 color=pg.Color(255, 255, 255),
                 font=Font.DEFAULT) -> None:

        super().__init__(game)
        self.rect = rect
        self.pos = rect
        self.size = size
        self.color = color
        self.font = pg.font.Font(font, self.size)
        self.text = text
        self.surface: pg.Surface = None
        self.update_text()

    def update_text(self, new_text: str = None) -> None:
        self.text = new_text if new_text else self.text
        self.surface = self.font.render(self.text, False, self.color)
        if type(self.rect) != tuple:
            topleft = self.rect.topleft
            self.rect = self.surface.get_rect()
            self.rect.topleft = topleft

    def update_color(self, new_color: pg.Color) -> None:
        self.color = new_color
        self.surface = self.font.render(self.text, False, self.color)
        if type(self.rect) != tuple:
            topleft = self.rect.topleft
            self.rect = self.surface.get_rect()
            self.rect.topleft = topleft

    def update_position(self, pos: Tuple[int, int]) -> None:
        self.pos = pos

    def process_draw(self) -> None:
        self.game.screen.blit(self.surface, self.rect)

    def process_event(self, event) -> None:
        pass

    def process_logic(self) -> None:
        pass
