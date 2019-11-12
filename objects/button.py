from third_party.button import Button
from constants import Color
from objects.base import DrawObject


class Btn(DrawObject):
    BUTTON_STYLE = {
        "hover_color": Color.BLUE,
        "font_color": Color.RED,
        "clicked_color": Color.GREEN,
        "clicked_font_color": Color.BLACK,
        "hover_font_color": Color.ORANGE
    }

    def __init__(self, game, geometry=(10, 10, 100, 40), color=(255, 255, 0), text='Test', function=None):
        super().__init__(game)
        self.geometry = geometry
        self.color = color
        self.function = function if function else Btn.no_action
        self.internal_button = Button(self.geometry, self.color, self.function, **Btn.BUTTON_STYLE)
        self.internal_button.text = text
        self.internal_button.render_text()

    @staticmethod
    def no_action(self):
        pass

    def process_event(self, event):
        self.internal_button.check_event(event)

    def process_draw(self):
        self.internal_button.update(self.game.screen)