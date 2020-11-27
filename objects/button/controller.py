from typing import List, Tuple, Union

import pygame as pg

from misc.constants import SOUNDS
from misc.path import get_sound_path
from objects.base import DrawableObject
from objects.button.button import Button


class ButtonController(DrawableObject):
    click_sound = pg.mixer.Sound(get_sound_path(SOUNDS["Click"]))
    keys_previous = [pg.K_UP, pg.K_LEFT, pg.K_w, pg.K_a]
    keys_next = [pg.K_DOWN, pg.K_RIGHT, pg.K_s, pg.K_d, pg.K_TAB]
    keys_activate = [pg.K_SPACE, pg.K_RETURN]

    def __init__(self, game, buttons: List[Button]) -> None:
        super().__init__(game)
        self.buttons = buttons
        self.active_button_index = -1
        self.click_sound.set_volume(0.5)

    def reset_state(self):
        self.deselect_current_button()
        self.active_button_index = -1

    def deselect_current_button(self):
        self.buttons[self.active_button_index].deselect()

    def select_previous_button(self) -> None:
        self.buttons[self.active_button_index].deselect()
        self.active_button_index -= 1
        if self.active_button_index < 0:
            self.active_button_index = len(self.buttons) - 1
        self.buttons[self.active_button_index].select()

    def select_next_button(self) -> None:
        self.buttons[self.active_button_index].deselect()
        self.active_button_index += 1
        if self.active_button_index == len(self.buttons):
            self.active_button_index = 0
        self.buttons[self.active_button_index].select()

    def activate_current_button(self) -> None:
        self.click_sound.play()
        self.buttons[self.active_button_index].activate()

    def click_current_button(self) -> None:
        self.buttons[self.active_button_index].click()

    def process_keydown(self, event: pg.event.Event) -> None:
        if event.type != pg.KEYDOWN:
            return
        if event.key in self.keys_previous:
            self.select_previous_button()
        elif event.key in self.keys_next:
            self.select_next_button()
        elif event.key in self.keys_activate:
            self.activate_current_button()

    def process_keyup(self, event: pg.event.Event) -> None:
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
        self.process_keydown(event)
        self.process_keyup(event)
        self.process_mouse_motion(event)

    def process_draw(self) -> None:
        for button in self.buttons:
            button.process_draw()
