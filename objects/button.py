from typing import Callable

import pygame

from third_party.button import Button
from constants import Color
from objects.base import DrawableObject


class ButtonObject(DrawableObject):
    BUTTON_STYLE = {
        "hover_color": Color.BLUE,
        "clicked_color": Color.GREEN,
        "font_color": Color.WHITE,
        "clicked_font_color": Color.BLACK,
        "hover_font_color": Color.ORANGE,
    }

    def __init__(self, game,
                 x: int, y: int, width: int, height: int, color: pygame.color.Color = None,
                 function: Callable[[None], None] = None,
                 text: str = 'Define me!') -> None:
        super().__init__(game)
        self.color = color if color else Color.WHITE
        self.function = function if function else ButtonObject.no_action
        self.text = text
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.button = Button(
            rect=self.rect,
            color=self.color,
            function=self.function,
            text=self.text,
            **self.BUTTON_STYLE
        )

    def move_center(self, x: int, y: int) -> None:
        super(ButtonObject, self).move_center(x, y)
        self.button.rect = self.rect

    def move(self, x: int, y: int) -> None:
        super().move(x, y)
        self.button.rect = self.rect

    @staticmethod
    def no_action(self) -> None:
        pass

    def set_text(self, text) -> None:
        self.text = text
        self.button.text = text
        self.button.render_text()

    def process_event(self, event) -> None:
        self.button.check_event(event)

    def process_draw(self) -> None:
        self.button.update(self.game.screen)
