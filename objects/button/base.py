from typing import Callable
from misc import Color
from objects.base import BaseObject
import pygame as pg


class BaseButton(BaseObject):
    def __init__(self, game, rect: pg.Rect, function: Callable[[], None]):
        super().__init__(game)
        self.rect = rect
        self.function = function

    def process_event(self, event: pg.event.Event) -> None:
        if event.type == pg.MOUSEBUTTONUP and event.type != pg.MOUSEWHEEL:
            if self.rect.collidepoint(event.pos):
                self.click()

    def process_draw(self) -> None:
        if not self.is_hidden:
            pg.draw.rect(self.game.screen, Color.WHITE, self.rect)

    def click(self) -> None:
        self.game.sounds.click.play()
        self.function()
