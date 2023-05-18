from typing import Callable, List, Tuple, Union

import pygame as pg

from pacman.data_core.enums import BtnStateEnum
from pacman.data_core.interfaces import IDrawable, IEventful
from pacman.misc.constants import BUTTON_DEFAULT_COLORS, ButtonColor, Font
from pacman.misic import Music
from pacman.objects.base import MovementObject


class Button(MovementObject, IDrawable, IEventful):
    def __init__(
        self,
        rect: Union[tuple, pg.Rect],
        function: Callable = None,
        select_function: Callable = None,
        text: str = "",
        colors: ButtonColor = BUTTON_DEFAULT_COLORS,
        text_size: int = 60,
        font=Font.DEFAULT,
        active: bool = True,
    ):
        super().__init__()
        self.rect = rect
        self.function = function
        self.select_function = select_function
        self.__text = text
        self.font = pg.font.Font(font, text_size)
        self.active = active
        self.__colors: ButtonColor = colors
        self.state = BtnStateEnum.INITIAL
        self.surfaces = self.prepare_surfaces()

    def mouse_hover(self, pos: Tuple[Union[int, float], Union[int, float]]) -> bool:
        return self.rect.collidepoint(pos) and self.active

    def process_mouse_motion(self, event: pg.event.Event) -> None:
        if event.type != pg.MOUSEMOTION:
            return
        if self.mouse_hover(event.pos):
            self.select()
        elif self.state != BtnStateEnum.INITIAL:
            self.deselect()

    def process_mouse_button_down(self, event: pg.event.Event) -> None:
        if event.type != pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEWHEEL:
            return
        if self.mouse_hover(event.pos):
            self.activate()

    def process_mouse_button_up(self, event: pg.event.Event) -> None:
        if event.type != pg.MOUSEBUTTONUP or event.type == pg.MOUSEWHEEL:
            return
        if self.mouse_hover(event.pos) and event.button == pg.BUTTON_LEFT and self.state != BtnStateEnum.INITIAL:
            self.deselect()

    def process_mouse_click(self, event: pg.event.Event) -> None:
        if not (event.type == pg.MOUSEBUTTONUP and event.type != pg.MOUSEWHEEL):
            return
        if self.rect.collidepoint(event.pos):
            self.select()
            self.click()

    @property
    def colors(self):
        return self.__colors

    @colors.setter
    def colors(self, colors: ButtonColor):
        self.__colors = colors
        self.surfaces = self.prepare_surfaces()

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text: str):
        self.__text = text
        self.surfaces = self.prepare_surfaces()

    def prepare_surfaces(self) -> List[pg.Surface]:
        surfaces = []
        for index in range(len(self.__colors)):
            surfaces.append(self.prepare_surface(index))
        return surfaces

    def prepare_surface(self, state_index: int) -> pg.Surface:
        surface = pg.Surface(self.rect.size)
        surface = surface.convert_alpha()
        zero_rect = surface.get_rect()

        text_surface = self.font.render(self.text, False, self.__colors[state_index].text)
        zero_text_rect = text_surface.get_rect()
        zero_text_rect.center = zero_rect.center

        pg.draw.rect(surface, self.__colors[state_index].background, zero_rect, 0)
        surface.blit(text_surface, zero_text_rect)

        return surface

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.surfaces[self.state.value], self.rect.topleft)

    def event_handler(self, event: pg.event.Event) -> None:
        if not self.active:
            return
        self.process_mouse_button_down(event)
        self.process_mouse_button_up(event)
        self.process_mouse_click(event)
        self.process_mouse_motion(event)

    def select(self) -> None:
        self.state = BtnStateEnum.HOVER
        if isinstance(self.select_function, Callable):
            self.select_function()

    def deselect(self) -> None:
        self.state = BtnStateEnum.INITIAL

    def activate(self) -> None:
        self.state = BtnStateEnum.CLICK

    def click(self) -> None:
        Music().CLICK.play()
        if isinstance(self.function, Callable):
            self.function()

    def is_state(self, state: BtnStateEnum):
        return self.state is state
