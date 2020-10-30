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

    def __init__(self, game, x, y, width, height, color=None, function=None, text='Define me!'):
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

    def move_center(self, x, y):
        super(ButtonObject, self).move_center(x, y)
        self.button.rect = self.rect

    def move(self, x, y):
        super().move(x, y)
        self.button.rect = self.rect

    @staticmethod
    def no_action(self):
        pass

    def set_text(self, text):
        self.text = text
        self.button.text = text
        self.button.render_text()

    def process_event(self, event):
        self.button.check_event(event)

    def process_draw(self):
        self.button.update(self.game.screen)


