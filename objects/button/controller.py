from typing import List, Tuple, Union

import pygame as pg

from objects import DrawableObject
from objects.button.button import Button


class ButtonController(DrawableObject):
    keys_previous = [pg.K_UP, pg.K_w]
    keys_next = [pg.K_DOWN, pg.K_s]
    keys_activate = [pg.K_SPACE, pg.K_RETURN]

    def __init__(self, game, buttons: List[Button]) -> None:
        super().__init__(game)
        self.buttons = buttons
        self.active_button_index = -1

    def reset_state(self) -> None:
        self.deselect_current_button()
        self.active_button_index = -1

    def set_state(self, index):
        self.active_button_index = index

    def deselect_current_button(self) -> None:
        self.buttons[self.active_button_index].deselect()

    def select_previous_button(self) -> None:
        self.buttons[self.active_button_index].deselect()
        self.active_button_index -= 1
        if self.active_button_index < 0:
            self.active_button_index = len(self.buttons) - 1
        if self.buttons[self.active_button_index].active:
            self.buttons[self.active_button_index].select()
        else:
            self.select_previous_button()

    def select_next_button(self) -> None:
        self.buttons[self.active_button_index].deselect()
        self.active_button_index += 1
        if self.active_button_index == len(self.buttons):
            self.active_button_index = 0
        if self.buttons[self.active_button_index].active:
            self.buttons[self.active_button_index].select()
        else:
            self.select_next_button()

    def activate_current_button(self) -> None:
        self.game.sounds.click.play()
        self.buttons[self.active_button_index].activate()

    def click_current_button(self) -> None:
        self.buttons[self.active_button_index].select()
        self.buttons[self.active_button_index].click()

    def process_key_down(self, event: pg.event.Event) -> None:
        if event.type != pg.KEYDOWN:
            return
        if event.key in self.keys_previous:
            self.select_previous_button()
        elif event.key in self.keys_next:
            self.select_next_button()
        elif event.key in self.keys_activate:
            self.activate_current_button()

    def process_key_up(self, event: pg.event.Event) -> None:
        if event.type != pg.KEYUP:
            return
        if event.key in [pg.K_SPACE, pg.K_RETURN]:
            self.click_current_button()

    def get_button_under_mouse(self, pos: Tuple[Union[int, float], Union[int, float]]) -> Union[int, None]:
        for index in range(len(self.buttons)):
            if self.buttons[index].rect.collidepoint(pos):
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

    def process_event(self, event: pg.event.Event) -> None:
        self.process_button_events(event)
        self.process_key_down(event)
        self.process_key_up(event)
        self.process_mouse_motion(event)

    def process_draw(self) -> None:
        for button in self.buttons:
            button.process_draw()

    def process_logic(self) -> None:
        for button in self.buttons:
            button.process_logic()
