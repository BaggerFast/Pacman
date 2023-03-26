from typing import List

import pygame as pg

from pacman.data_core import KbKeys
from pacman.data_core.enums import BtnStateEnum
from pacman.objects import DrawableObject
from pacman.objects.button.button import Button


class ButtonController(DrawableObject):
    def __init__(self, buttons: List[Button]):
        super().__init__()
        self.buttons = buttons
        self.active_button_index = 0
        self.current.select()

        self.kb_down_actions = {
            KbKeys.DOWN: self.move_down,
            KbKeys.UP: self.move_up,
            KbKeys.ENTER: lambda: self.current.activate(),
        }

    @property
    def current(self) -> Button:
        return self.buttons[self.active_button_index]

    def move_up(self):
        self.current.deselect()
        self.active_button_index = (self.active_button_index - 1) % len(self.buttons)
        if not self.current.active:
            self.move_up()
        self.current.select()

    def move_down(self) -> None:
        self.current.deselect()
        self.active_button_index = (self.active_button_index + 1) % len(self.buttons)
        if not self.current.active:
            self.move_down()
        self.current.select()

    def unpress_cur_btn(self):
        if not self.current.is_state(BtnStateEnum.CLICK):
            return
        self.current.select()
        self.current.click()

    def __parse_keyboard(self, event) -> None:
        if event.type == pg.KEYDOWN:
            for key in self.kb_down_actions:
                if event.key in key:
                    self.kb_down_actions[key]()
                    return
        elif event.type == pg.KEYUP:
            if event.key in KbKeys.ENTER:
                self.unpress_cur_btn()

    def process_draw(self, screen: pg.Surface) -> None:
        if self.current.is_state(BtnStateEnum.INITIAL):
            self.current.select()
        for button in self.buttons:
            button.process_draw(screen)

    def process_event(self, event: pg.event.Event) -> None:
        self.buttons_process_event(event)
        self.check_hover_btn()
        self.__parse_keyboard(event)

    def buttons_process_event(self, event: pg.event.Event) -> None:
        for button in self.buttons:
            button.process_event(event)

    def check_hover_btn(self) -> None:
        for index, button in enumerate(self.buttons):
            if button.is_state(BtnStateEnum.HOVER):
                self.active_button_index = index
                return
