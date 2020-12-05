from typing import List, Union, Callable, Tuple
import pygame as pg
from misc import Color, Font, Sounds, ButtonColor, BUTTON_DEFAULT_COLORS
from objects.base import DrawableObject


class BaseButton(DrawableObject):
    def __init__(self, game, geometry: pg.Rect, function: Callable[[], None]) -> None:
        super().__init__(game)
        self.rect = geometry
        self.function = function

    def process_event(self, event: pg.event.Event) -> None:
        if event.type == pg.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                self.click()

    def process_draw(self) -> None:
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
        value=True,
        scene: tuple = (None, None)
    ) -> None:

        super().__init__(game, geometry, function)
        self.text = text
        self.font = pg.font.Font(font, text_size)
        self.active = active
        self.colors: ButtonColor = colors
        self.state = self.STATE_INITIAL
        self.surfaces = self.prepare_surfaces()
        self.left_button_pressed = False
        self.value = value
        self.scene = scene
        self.name = self.text
        if center:
            self.move_center(*center)

    def mouse_hover(self, pos: Tuple[Union[int, float], Union[int, float]]) -> bool:
        return bool(self.rect.collidepoint(pos)) and self.active

    def process_mouse_motion(self, event: pg.event.Event) -> None:
        if event.type != pg.MOUSEMOTION:
            return
        if self.mouse_hover(event.pos):
            if not self.left_button_pressed:
                self.state = self.STATE_HOVER
        else:
            self.state = self.STATE_INITIAL

    def process_mouse_button_down(self, event: pg.event.Event) -> None:
        if event.type != pg.MOUSEBUTTONDOWN:
            return
        if event.button == pg.BUTTON_LEFT:
            self.left_button_pressed = True
        if self.mouse_hover(event.pos):
            self.state = self.STATE_CLICK
            self.game.sounds.click.play()

    def process_mouse_button_up(self, event: pg.event.Event) -> None:
        if event.type != pg.MOUSEBUTTONUP:
            return
        if event.button == pg.BUTTON_LEFT:
            self.left_button_pressed = False
        if self.mouse_hover(event.pos) and event.button == pg.BUTTON_LEFT:
            self.state = self.STATE_INITIAL

    def process_event(self, event: pg.event.Event) -> None:
        if self.active:
            self.process_mouse_motion(event)
            self.process_mouse_button_down(event)
            self.process_mouse_button_up(event)
            super().process_event(event)

    def update_text(self, text: str) -> None:
        self.text = text
        self.surfaces = self.prepare_surfaces()

    def prepare_surfaces(self) -> List[pg.Surface]:
        surfaces = []
        for index in range(len(self.colors.get_members_list())):
            surfaces.append(self.prepare_surface(index))
        return surfaces

    def prepare_surface(self, state_index: int) -> pg.Surface:
        surface = pg.surface.Surface(self.rect.size)
        zero_rect = surface.get_rect()

        text_surface = self.font.render(self.text, False, self.colors[state_index].text)
        zero_text_rect = text_surface.get_rect()
        zero_text_rect.center = zero_rect.center

        pg.draw.rect(surface, self.colors[state_index].background, zero_rect, 0)
        surface.blit(text_surface, zero_text_rect)

        return surface

    def process_draw(self) -> None:
        self.game.screen.blit(self.surfaces[self.state], self.rect.topleft)

    def select(self) -> None:
        self.state = self.STATE_HOVER

    def deselect(self) -> None:
        self.state = self.STATE_INITIAL

    def activate(self) -> None:
        self.state = self.STATE_CLICK


class LvlButton(Button):
    def click(self):
        self.game.level_id = self.value
        self.game.records.update_records()
        self.game.scenes.set(self.game.scenes.MENU, reset=True)


class SceneButton(Button):
    def click(self):
        if callable(self.scene[0]):
            self.scene[0]()
        else:
            self.game.scenes.set(self.scene[0], reset=self.scene[1])


class SettingButtons(Button):
    def click(self):
        self.game.settings.MUTE = not self.game.settings.MUTE
        if self.game.settings.MUTE:
            self.update_text(self.name + "-")
        else:
            self.update_text(self.name + "+")
        self.a = self.game.sounds.__dict__
        for key in self.a.keys():
            self.a[key].update_volume()
        print(self.game.settings.MUTE)
