import pygame as pg
from lib.BasicObjects.text import Text
import os.path


class BaseButton:
    def __init__(self, screen, cord, function, base_image, clicked_image=None,
                 hover_image=None):
        self.screen = screen
        self.base_image = base_image
        self.rect = self.base_image.get_rect()
        self.rect.x = cord[0]
        self.rect.y = cord[1]
        self.hover_image = \
            base_image if hover_image is None else hover_image
        self.clicked_image = \
            base_image if clicked_image is None else clicked_image

        self.draw_image = self.base_image

        self.function = function
        self.click = 'initial'

    def getPos(self):
        pos = pg.mouse.get_pos()
        return self.rect[0] <= pos[0] <= self.rect[2] + self.rect[0] \
            and self.rect[1] <= pos[1] <= self.rect[3] + self.rect[1]

    def checkEvents(self):
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN and self.getPos():
                self.click = 'click'
            elif event.type == pg.MOUSEBUTTONUP:
                self.click = 'initial'
                if self.getPos():
                    self.onClick()

    def update(self):
        if self.getPos() and self.click == 'initial':
            self.click = 'hover'
        elif not self.getPos() and self.click == 'hover':
            self.click = 'initial'
        self.checkEvents()

    def onClick(self):
        self.function()

    def draw(self):
        if self.click == 'click':
            self.draw_image = self.clicked_image
        elif self.click == 'initial':
            self.draw_image = self.base_image
        elif self.click == 'hover':
            self.draw_image = self.hover_image
        else:
            self.draw_image = self.base_image
        self.screen.blit(self.draw_image, self.rect)


class Button(BaseButton):
    def __init__(self, screen, rect: pg.Rect, function, text, static_text_color,
                 static_button_color, hover_text_color=None,
                 hover_button_color=None,  clicked_text_color=None,
                 clicked_button_color=None,
                 text_size=30, text_font=os.path.join('fonts', 'font0.ttf')):

        if clicked_text_color is None:
            clicked_text_color = static_text_color
        if hover_text_color is None:
            hover_text_color = static_text_color

        hover_image = clicked_image = None

        base_image = self.drawImage(static_button_color, static_text_color,
                                    text, text_font, text_size, rect)

        if hover_button_color is not None:
            hover_image = self.drawImage(hover_button_color, hover_text_color,
                                         text, text_font, text_size, rect)
        if clicked_button_color is not None:
            clicked_image = self.drawImage(clicked_button_color,
                                           clicked_text_color, text, text_font,
                                           text_size, rect)

        BaseButton.__init__(self, screen, (rect[0], rect[1]), function,
                            base_image, clicked_image, hover_image)

    def drawImage(self, color, text_color, text, text_font, text_size, rect):
        temp_surface = pg.Surface((rect[2], rect[3]))
        temp_surface.fill((0, 0, 0))

        pg.draw.rect(temp_surface, color, (5, 0, rect[2] - 10, rect[3]))
        pg.draw.rect(temp_surface, color, (0, 5, rect[2], rect[3] - 10))

        main_text = Text(text, color=text_color, font=text_font, size=text_size)
        main_text.update_position(main_text.surface.get_rect(
            center=(rect[2] // 2, rect[3] // 2)))
        main_text.draw(temp_surface)
        return temp_surface


class ButtonControl:
    def __init__(self, buttons: list):
        self.buttons = buttons
        self.button_number = None

    def set_current_button(self, number):
        self.current_button = self.buttons[number]
        self.current_button.click = 'initial'
        self.button_number = number
        self.buttons[self.button_number].click = 'hover'

    def mouse_action(self):
        if sum(pg.mouse.get_rel()):
            self.buttons[self.button_number].click = 'initial'
            for i in range(len(self.buttons)):
                self.buttons[i].update()
                if self.buttons[i].click == 'hover':
                    self.button_number = i


def main():
    a = ButtonControl([2, 2, 3])
    pg.display.init()
    pg.display.set_mode((100, 100))
    while True:
        pg.event.get()
        a.mouse_action()


if __name__ == "__main__":
    main()
