from enum import IntEnum
from typing import List, Union, Callable, Tuple
import pygame as pg
from misc.constants import Font, ButtonColor, BUTTON_DEFAULT_COLORS
from misc.interfaces import IDrawable, IEventful
from objects.base import BaseObject


class BtnStates(IntEnum):
    INITIAL = 0
    HOVER = 1
    CLICK = 2


class Button(BaseObject, IDrawable, IEventful):

    def __init__(self,
                 game,
                 rect: Union[tuple, pg.Rect],
                 text: str,
                 function: Callable[[], None] = None,
                 colors: ButtonColor = BUTTON_DEFAULT_COLORS,
                 center: Tuple[int, int] = None,
                 text_size: int = 60,
                 active: bool = True
                 ):
        BaseObject.__init__(self)
        # todo delete game
        self.game = game
        self.rect = rect
        self.function = function
        self.__text = text
        self.__font = pg.font.Font(Font.DEFAULT, text_size)
        self.active = active
        self.__colors: ButtonColor = colors
        self.state = BtnStates.INITIAL
        self.surfaces = self.prepare_surfaces()
        if center:
            self.move_center(*center)

    # region Public

    # region Implementation of IDrawable, IEventful

    def process_event(self, event: pg.event.Event) -> None:
        if not self.active:
            return
        self.process_mouse_button_down(event)
        self.process_mouse_button_up(event)
        self.process_mouse_click(event)
        self.process_mouse_motion(event)

    def process_draw(self, screen: pg.Surface) -> None:
        screen.blit(self.surfaces[self.state], self.rect.topleft)

    # endregion

    def mouse_hover(self, pos: Tuple[Union[int, float], Union[int, float]]) -> bool:
        return self.rect.collidepoint(pos) and self.active

    def process_mouse_motion(self, event: pg.event.Event) -> None:
        if event.type != pg.MOUSEMOTION:
            return
        if self.mouse_hover(event.pos):
            self.select()
        elif self.state != BtnStates.INITIAL:
            self.deselect()

    def process_mouse_button_down(self, event: pg.event.Event) -> None:
        if event.type != pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEWHEEL:
            return
        if self.mouse_hover(event.pos):
            self.activate()

    def process_mouse_button_up(self, event: pg.event.Event) -> None:
        if event.type != pg.MOUSEBUTTONUP or event.type == pg.MOUSEWHEEL:
            return
        if self.mouse_hover(event.pos) and event.button == pg.BUTTON_LEFT and self.state != BtnStates.INITIAL:
            self.deselect()

    def process_mouse_click(self, event: pg.event.Event) -> None:
        if not (event.type == pg.MOUSEBUTTONUP and event.type != pg.MOUSEWHEEL):
            return
        if self.rect.collidepoint(event.pos):
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
        for index in range(len(self.__colors.get_members_list())):
            surfaces.append(self.prepare_surface(index))
        return surfaces

    def prepare_surface(self, state_index: int) -> pg.surface.Surface:
        surface = pg.Surface(self.rect.size).convert_alpha()
        zero_rect = surface.get_rect()

        text_surface = self.__font.render(self.text, False, self.__colors[state_index].text)
        zero_text_rect = text_surface.get_rect()
        zero_text_rect.center = zero_rect.center

        pg.draw.rect(surface, self.__colors[state_index].background, zero_rect, 0)
        surface.blit(text_surface, zero_text_rect)

        return surface

    def select(self) -> None:
        self.state = BtnStates.HOVER

    def deselect(self) -> None:
        self.state = BtnStates.INITIAL

    def activate(self) -> None:
        self.state = BtnStates.CLICK

    def click(self) -> None:
        self.game.sounds.click.play()
        self.function()

    # endregion
