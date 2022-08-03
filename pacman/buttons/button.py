import pygame as pg

from typing import Callable
from misc.constants import Font
from misc.misc import Font_hint
from misc.patterns.entities import EventEntity, RenderEntity
from pacman.buttons.util import BtnState, BTN_DEFAULT_COLORS, ButtonColor

# todo delete Game
from pacman.objects import DrawableObject


# todo finish refactor

class Button(DrawableObject, EventEntity, RenderEntity):

    def __init__(self,
                 text: str,
                 geometry: tuple | pg.Rect,
                 function: Callable = None,
                 colors: ButtonColor = BTN_DEFAULT_COLORS,
                 center: tuple[int, int] = None,
                 font: Font_hint = pg.font.Font(Font.DEFAULT, 21)) -> None:

        super().__init__()
        self.rect = geometry
        self.function = function
        self.__text = text
        self.__font = font
        self._colors = colors
        self.state = BtnState.INITIAL
        self.surfaces = self.prepare_surfaces()

        if center:
            self.move_center(*center)

    def mouse_hover(self, pos: tuple[int, int]) -> bool:
        return bool(self.rect.collidepoint(pos))

    def process_mouse_click(self, event: pg.event.Event) -> None:
        if not (event.type == pg.MOUSEBUTTONUP and event.type != pg.MOUSEWHEEL):
            return
        if self.rect.collidepoint(event.pos):
            self.click()

    def process_mouse_motion(self, event: pg.event.Event) -> None:
        if event.type != pg.MOUSEMOTION:
            return
        if self.mouse_hover(event.pos):
            self.select()
        elif self.state != BtnState.INITIAL:
            self.deselect()

    def process_mouse_button_down(self, event: pg.event.Event) -> None:
        if event.type != pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEWHEEL:
            return
        if self.mouse_hover(event.pos):
            self.activate()

    def process_mouse_button_up(self, event: pg.event.Event) -> None:
        if event.type != pg.MOUSEBUTTONUP or event.type == pg.MOUSEWHEEL:
            return
        if not (event.button == pg.BUTTON_LEFT and self.state != BtnState.INITIAL):
            return
        if self.mouse_hover(event.pos):
            self.deselect()

    def render(self, screen: pg.Surface) -> None:
        screen.blit(self.surfaces[self.state - 1], self.rect.topleft)

    def event_handler(self, event: pg.event.Event) -> None:
        self.process_mouse_button_down(event)
        self.process_mouse_button_up(event)
        self.process_mouse_click(event)
        self.process_mouse_motion(event)

    @property
    def colors(self):
        return self._colors

    @colors.setter
    def colors(self, colors: ButtonColor):
        self._colors = colors
        self.surfaces = self.prepare_surfaces()

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text: str):
        self.__text = text
        self.surfaces = self.prepare_surfaces()

    def prepare_surfaces(self) -> list[pg.Surface]:
        surfaces = []
        for index in range(len(self._colors.get_members_list())):
            surfaces.append(self.prepare_surface(index))
        return surfaces

    def prepare_surface(self, state_index: int) -> pg.Surface:
        surface = pg.surface.Surface(self.rect.size)
        surface = surface.convert_alpha()
        zero_rect = surface.get_rect()

        text_surface = self.__font.render(self.text, False, self._colors[state_index].text)
        zero_text_rect = text_surface.get_rect()
        zero_text_rect.center = zero_rect.center

        pg.draw.rect(surface, self._colors[state_index].background, zero_rect, 0)
        surface.blit(text_surface, zero_text_rect)

        return surface

    def select(self) -> None:
        self.state = BtnState.HOVER

    def deselect(self) -> None:
        self.state = BtnState.INITIAL

    def activate(self) -> None:
        self.state = BtnState.CLICK

    def click(self) -> None:
        self.function()
