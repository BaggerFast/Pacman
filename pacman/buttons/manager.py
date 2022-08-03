import pygame as pg

from misc.patterns.entities import EventEntity, RenderEntity
from pacman.buttons.button import Button
from settings import Keyboard


# todo finish refactor

class ButtonManager(RenderEntity, EventEntity):

    def __init__(self, buttons: list[Button]) -> None:
        super().__init__()
        self.buttons = buttons
        self.active_button_index = -1
        self.move_down()

        self.kb_actions = {
            Keyboard.DOWN: self.move_down,
            Keyboard.UP: self.move_up,
            Keyboard.ENTER: self.click_cur_btn,
        }

    def buttons_event_handler(self, event: pg.event.Event) -> None:
        for button in self.buttons:
            button.event_handler(event)

    def mouse_event_handler(self, event: pg.event.Event) -> None:
        if event.type != pg.MOUSEMOTION:
            return
        for index, button in enumerate(self.buttons):
            if button.rect.collidepoint(event.pos):
                self.active_button_index = index
                return

    def __parse_keyboard(self, event) -> None:
        if event.type != pg.KEYDOWN:
            return
        for key in self.kb_actions:
            if event.key in key:
                self.kb_actions[key]()
                return

    def move_up(self):
        self.deselect_cur_btn()
        self.active_button_index = (self.active_button_index - 1) % len(self.buttons)
        self.select_cur_btn()

    def move_down(self):
        self.deselect_cur_btn()
        self.active_button_index = (self.active_button_index + 1) % len(self.buttons)
        self.select_cur_btn()

    # region Entity Implementation

    def event_handler(self, event: pg.event.Event) -> None:
        self.buttons_event_handler(event)
        self.mouse_event_handler(event)
        self.__parse_keyboard(event)

    def render(self, screen: pg.Surface) -> None:
        for button in self.buttons:
            button.render(screen)

    # endregion

    # region CurrentBtn

    def deselect_cur_btn(self) -> None:
        self.buttons[self.active_button_index].deselect()

    def select_cur_btn(self) -> None:
        self.buttons[self.active_button_index].select()

    def click_cur_btn(self) -> None:
        self.buttons[self.active_button_index].click()

    # endregion
