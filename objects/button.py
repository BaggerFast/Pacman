import pygame as pg

from misc.constants import Color
from objects.base import DrawableObject
from objects.text import Text


class BaseButton(DrawableObject):
    def __init__(self, game, cord, function, base_image, clicked_image=None, hover_image=None):
        super().__init__(game)
        self.base_image = base_image
        self.rect = self.base_image.get_rect()
        self.rect.x = cord[0]
        self.rect.y = cord[1]
        self.hover_image = base_image if hover_image is None else hover_image
        self.clicked_image = base_image if clicked_image is None else clicked_image
        self.draw_image = self.base_image
        self.function = function
        self.click = 'initial'

    def mouse_hover(self):
        pos = pg.mouse.get_pos()
        return self.rect[0] <= pos[0] <= self.rect[2] + self.rect[0] \
            and self.rect[1] <= pos[1] <= self.rect[3] + self.rect[1]

    def process_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and self.mouse_hover():
            self.click = 'click'
        elif event.type == pg.MOUSEBUTTONUP:
            self.click = 'initial'
            if self.mouse_hover():
                self.on_click()

    def process_logic(self):
        if self.mouse_hover() and self.click == 'initial':
            self.click = 'hover'
        elif not self.mouse_hover() and self.click == 'hover':
            self.click = 'initial'

    def on_click(self):
        self.function()

    def process_draw(self):
        if self.click == 'click':
            self.draw_image = self.clicked_image
        elif self.click == 'initial':
            self.draw_image = self.base_image
        elif self.click == 'hover':
            self.draw_image = self.hover_image
        else:
            self.draw_image = self.base_image
        self.game.screen.blit(self.draw_image, self.rect)


class Button(BaseButton):
    def __init__(self, game, rect: pg.Rect, function, text, static_text_color,
                 static_button_color, hover_text_color=None,
                 hover_button_color=None,  clicked_text_color=None,
                 clicked_button_color=None,
                 text_size=30, text_font='Arial'):
        self.game = game
        if clicked_text_color is None:
            clicked_text_color = static_text_color
        if hover_text_color is None:
            hover_text_color = static_text_color

        hover_image = clicked_image = None

        base_image = self.prepare_surface(
            static_button_color, static_text_color,
            text, text_font, text_size, rect
        )

        if hover_button_color:
            hover_image = self.prepare_surface(
                hover_button_color, hover_text_color,
                text, text_font, text_size, rect
            )
        if clicked_button_color:
            clicked_image = self.prepare_surface(
                clicked_button_color, clicked_text_color,
                text, text_font, text_size, rect
            )

        BaseButton.__init__(self, game, (rect.x, rect.y), function,
                            base_image, clicked_image, hover_image)

    def prepare_surface(self, color, text_color, text, text_font, text_size, rect):
        temp_surface = pg.Surface((rect.width, rect.height))
        temp_surface.fill(Color.BLACK)

        pg.draw.rect(temp_surface, color, (5, 0, rect.width - 10, rect.height))
        pg.draw.rect(temp_surface, color, (0, 5, rect.width, rect.height - 10))

        main_text = Text(None, text, color=text_color, font=text_font, size=text_size)
        main_text.move_center(rect.width // 2, rect.height // 2)
        temp_surface.blit(main_text.surface, main_text.rect)
        return temp_surface
