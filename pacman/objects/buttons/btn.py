from typing import Callable, List, Tuple, Union

from pygame import BUTTON_LEFT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, Rect, Surface, draw
from pygame.event import Event
from pygame.font import Font

from pacman.data_core import FontCfg, IDrawable, IEventful
from pacman.data_core.enums import BtnStateEnum, SoundCh
from pacman.misc import RectObj
from pacman.sound import SoundController, Sounds

from .utils import BTN_DEF_COLORS, BtnColor


class Btn(RectObj, IDrawable, IEventful):
    def __init__(
        self,
        text: str,
        rect: Rect,
        function: Callable = None,
        select_function: Callable = None,
        colors: BtnColor = BTN_DEF_COLORS,
        text_size: int = 60,
        font: str = FontCfg.DEFAULT,
    ):
        super().__init__(rect)
        self.__function = function
        self.__select_function = select_function
        self.__text = text
        self.__font = Font(font, text_size)
        self._color: BtnColor = colors
        self.__state = BtnStateEnum.INITIAL
        self.__surfaces = self.__prepare_surfaces()

    # region Public

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, text: str) -> None:
        self.__text = text
        self.__surfaces = self.__prepare_surfaces()

    def _set_color(self, colors: BtnColor) -> None:
        self._color = colors
        self.__surfaces = self.__prepare_surfaces()

    def select(self) -> None:
        self.__state = BtnStateEnum.HOVER
        if isinstance(self.__select_function, Callable):
            self.__select_function()

    def deselect(self) -> None:
        self.__state = BtnStateEnum.INITIAL

    def activate(self) -> None:
        self.__state = BtnStateEnum.CLICK

    def click(self) -> None:
        if isinstance(self.__function, Callable):
            self.__function()
        SoundController.play(SoundCh.SYSTEM, Sounds.CLICK)

    def is_state(self, state: BtnStateEnum) -> bool:
        return self.__state is state

    def draw(self, screen: Surface) -> None:
        screen.blit(self.__surfaces[self.__state.value], self.rect.topleft)

    def event_handler(self, event: Event) -> None:
        self.__check_mouse_button_down(event)
        self.__check_mouse_button_up(event)
        self.__check_mouse_click(event)
        self.__check_mouse_motion(event)

    # endregion

    # region Private

    def __mouse_hover(self, pos: Tuple[Union[int, float], Union[int, float]]) -> bool:
        return self.rect.collidepoint(pos)

    def __check_mouse_motion(self, event: Event) -> None:
        if event.type != MOUSEMOTION:
            return
        if self.__mouse_hover(event.pos):
            self.select()
        elif self.__state != BtnStateEnum.INITIAL:
            self.deselect()

    def __check_mouse_button_down(self, event: Event) -> None:
        if event.type != MOUSEBUTTONDOWN:
            return
        if self.__mouse_hover(event.pos):
            self.activate()

    def __check_mouse_button_up(self, event: Event) -> None:
        if event.type != MOUSEBUTTONUP:
            return
        if self.__mouse_hover(event.pos) and event.button == BUTTON_LEFT and self.__state != BtnStateEnum.INITIAL:
            self.deselect()

    def __check_mouse_click(self, event: Event) -> None:
        if not event.type == MOUSEBUTTONUP:
            return
        if self.rect.collidepoint(event.pos):
            self.select()
            self.click()

    def __prepare_surfaces(self) -> List[Surface]:
        surfaces = []
        for index in range(len(self._color)):
            surfaces.append(self.__prepare_surface(index))
        return surfaces

    def __prepare_surface(self, state_index: int) -> Surface:
        surface = Surface(self.rect.size)
        surface = surface.convert_alpha()
        zero_rect = surface.get_rect()

        text_surface = self.__font.render(self.text, False, self._color[state_index].text)
        zero_text_rect = text_surface.get_rect()
        zero_text_rect.center = zero_rect.center

        draw.rect(surface, self._color[state_index].background, zero_rect, 0)
        surface.blit(text_surface, zero_text_rect)

        return surface

    # endregion
