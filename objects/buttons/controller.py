from typing import Union
import pygame as pg

from config.settings import Keyboard
from misc.interfaces.igeneric_object import IDrawable, IEventful
from objects.buttons.button import Button


class ButtonController(IDrawable, IEventful):

    def __init__(self, buttons: list[Button]):
        self.buttons: list[Button] = buttons

        self.active_button_index: int = -1

        self.kb_actions = {
            Keyboard.DOWN: self.move_down,
            Keyboard.UP: self.move_up,
            Keyboard.ENTER: self.press_cur_btn,
        }

    # region Public

    # region Implementation of IDrawable, IEventful

    def process_draw(self, screen: pg.Surface) -> None:
        for button in self.buttons:
            button.process_draw(screen)

    def process_event(self, event: pg.event.Event) -> None:
        self.buttons_process_event(event)
        self.mouse_process_event(event)
        self.__parse_keyboard(event)

    def buttons_process_event(self, event: pg.event.Event) -> None:
        for button in self.buttons:
            button.process_event(event)

    def mouse_process_event(self, event: pg.event.Event) -> None:
        if event.type != pg.MOUSEMOTION:
            return
        for index, button in enumerate(self.buttons):
            if button.rect.collidepoint(event.pos):
                self.active_button_index = index
                return

    # endregion

    def deselect_cur_btn(self) -> None:
        self.buttons[self.active_button_index].deselect()

    def select_cur_btn(self) -> None:
        self.buttons[self.active_button_index].select()

    def press_cur_btn(self) -> None:
        self.buttons[self.active_button_index].activate()
        self.buttons[self.active_button_index].click()

    def move_up(self):
        self.deselect_cur_btn()
        self.active_button_index = (self.active_button_index - 1) % len(self.buttons)
        self.select_cur_btn()

    def move_down(self):
        self.deselect_cur_btn()
        self.active_button_index = (self.active_button_index + 1) % len(self.buttons)
        self.select_cur_btn()

    # endregion

    # region Private

    def __parse_keyboard(self, event) -> None:
        if event.type != pg.KEYDOWN:
            return
        for key in self.kb_actions:
            if event.key in key:
                self.kb_actions[key]()
                return

    # endregion
