from typing import Union
import pygame as pg
from misc.constants import EvenType
from misc.interfaces.igeneric_object import IDrawable, IEventful
from objects.buttons.button import Button


class ButtonController(IDrawable, IEventful):
    # todo refactor
    CURRENT_BTN = (pg.K_SPACE, pg.K_RETURN)
    NEXT_BTN = (pg.K_s, pg.K_DOWN)
    PREV_BTN = (pg.K_w, pg.K_UP)

    def __init__(self, game, buttons):
        self.game = game
        self.buttons = buttons
        self.active_button_index = -1
        self.kb_actions = {
            self.NEXT_BTN: lambda: self.select_button_checker(1),
            self.PREV_BTN: lambda: self.select_button_checker(-1),
            self.CURRENT_BTN: self.press_current_button,
        }

    # region Public

    # region Implementation of IDrawable, IEventful

    def process_event(self, event: pg.event.Event) -> None:
        self.process_button_events(event)
        self.process_key_down(event)
        self.process_mouse_motion(event)
        self.__parse_keyboard(event)

    def process_draw(self, screen: pg.Surface) -> None:
        for button in self.buttons:
            button.process_draw(screen)

    # endregion

    def button_add(self, button: Button):
        self.buttons.append(button)

    def deselect_current_button(self) -> None:
        self.buttons[self.active_button_index].deselect()

    def select_current_button(self) -> None:
        self.buttons[self.active_button_index].select()

    def select_button_checker(self, index: int) -> None:
        active_button_index = (self.active_button_index + index) % len(self.buttons)
        if self.buttons[active_button_index].active:
            self.deselect_current_button()
            self.active_button_index = active_button_index
            self.select_current_button()

    def press_current_button(self) -> None:
        self.buttons[self.active_button_index].activate()
        self.buttons[self.active_button_index].click()

    def process_key_down(self, event: pg.event.Event) -> None:
        if event.type in self.kb_actions.keys():
            if not (event.type == EvenType.PressBtn and self.active_button_index < 0):
                self.kb_actions[event.type]()

    def get_button_under_mouse(self, pos) -> Union[int, None]:
        for index, button in enumerate(self.buttons):
            if button.rect.collidepoint(pos):
                return index
        return None

    def process_mouse_motion(self, event: pg.event.Event) -> None:
        if event.type != pg.MOUSEMOTION:
            return
        index = self.get_button_under_mouse(event.pos)
        if index:
            self.active_button_index = index

    def process_button_events(self, event: pg.event.Event) -> None:
        for button in self.buttons:
            button.process_event(event)

    # endregion

    # Private

    def __parse_keyboard(self, event):
        if event.type != pg.KEYDOWN:
            return
        for key in self.kb_actions.keys():
            if event.key in key:
                self.kb_actions[key]()
                return

    # endregion
