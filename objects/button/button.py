from typing import List, Union, Callable, Tuple
import pygame as pg
from misc import Color, Font, ButtonColor, BUTTON_DEFAULT_COLORS
from objects.base import DrawableObject


class BaseButton(DrawableObject):
    def __init__(self, game, geometry: pg.Rect, function: Callable[[], None]):
        super().__init__(game)
        self.rect = geometry
        self.function = function

    def process_event(self, event: pg.event.Event) -> None:
        if event.type == pg.MOUSEBUTTONUP and event.type != pg.MOUSEWHEEL:
            if self.rect.collidepoint(event.pos):
                self.click()

    def process_draw(self) -> None:
        if not self.is_hidden:
            pg.draw.rect(self.game.screen, Color.WHITE, self.rect)

    def click(self) -> None:
        self.function()


class Button(BaseButton):
    STATE_INITIAL = 0
    STATE_HOVER = 1
    STATE_CLICK = 2

    def __init__(
        self,
        game,
        geometry: Union[tuple, pg.Rect],
        function: Callable[[], None] = None,
        text: str = 'Define me',
        colors: ButtonColor = BUTTON_DEFAULT_COLORS,
        center: Tuple[int, int] = None,
        text_size: int = 60,
        font=Font.DEFAULT,
        active: bool = True,
    ) -> None:

        super().__init__(game, geometry, function)
        self.__text = text
        self.font = pg.font.Font(font, text_size)
        self.active = active
        self.__colors: ButtonColor = colors
        self.deselect()
        self.surfaces = self.prepare_surfaces()
        self.left_button_pressed = False
        if center:
            self.move_center(*center)

    def mouse_hover(self, pos: Tuple[Union[int, float], Union[int, float]]) -> bool:
        return bool(self.rect.collidepoint(pos)) and self.active

    def process_mouse_motion(self, event: pg.event.Event) -> None:
        if event.type != pg.MOUSEMOTION:
            return
        if self.mouse_hover(event.pos):
            if not self.left_button_pressed and self.state != self.STATE_HOVER:
                self.select()
        elif self.state != self.STATE_INITIAL:
            self.deselect()

    def process_mouse_button_down(self, event: pg.event.Event) -> None:
        if event.type != pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEWHEEL:
            return
        if event.button == pg.BUTTON_LEFT:
            self.left_button_pressed = True
        if self.mouse_hover(event.pos):
            self.activate()

    def process_mouse_button_up(self, event: pg.event.Event) -> None:
        if event.type != pg.MOUSEBUTTONUP or event.type == pg.MOUSEWHEEL:
            return
        if event.button == pg.BUTTON_LEFT:
            self.left_button_pressed = False
        if self.mouse_hover(event.pos) and event.button == pg.BUTTON_LEFT and self.state != self.STATE_INITIAL:
            self.deselect()

    def process_event(self, event: pg.event.Event) -> None:
        if self.active:
            self.process_mouse_motion(event)
            self.process_mouse_button_down(event)
            self.process_mouse_button_up(event)
            if event.type == pg.MOUSEBUTTONUP and event.type != pg.MOUSEWHEEL:
                if self.rect.collidepoint(event.pos):
                    self.click()
                    self.game.sounds.click.play()

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

    def prepare_surface(self, state_index: int) -> pg.Surface:
        surface = pg.Surface(self.rect.size).convert_alpha()
        zero_rect = surface.get_rect()

        text_surface = self.font.render(self.text, False, self.__colors[state_index].text)
        zero_text_rect = text_surface.get_rect()
        zero_text_rect.center = zero_rect.center

        pg.draw.rect(surface, self.__colors[state_index].background, zero_rect, 0)
        surface.blit(text_surface, zero_text_rect)

        return surface

    def process_draw(self) -> None:
        if not self.is_hidden:
            self.game.screen.blit(self.surfaces[self.state], self.rect.topleft)

    def select(self) -> None:
        self.state = self.STATE_HOVER

    def deselect(self) -> None:
        self.state = self.STATE_INITIAL

    def activate(self) -> None:
        self.state = self.STATE_CLICK
