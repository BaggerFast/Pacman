import pygame as pg
from pygame.event import Event

from pacman.data_core import Cfg, EvenType, FontCfg, event_append
from pacman.misc import is_esc_pressed
from pacman.objects import Text
from pacman.objects.buttons import Btn, ButtonController

from .blur_scene import BlurScene
from .scene_manager import SceneManager


class PauseScene(BlurScene):
    def __stop_game(self) -> None:
        from .menu import MenuScene

        event_append(EvenType.GET_SETTINGS)
        SceneManager().reset(MenuScene(self.game))

    def __restart_game(self) -> None:
        from pacman.scenes.main import MainScene

        event_append(EvenType.GET_SETTINGS)
        SceneManager().reset(MainScene(self.game))

    def _create_objects(self) -> None:
        super()._create_objects()

        names = [
            ("CONTINUE", SceneManager().pop),
            ("RESTART", self.__restart_game),
            ("MENU", self.__stop_game),
        ]
        buttons = []
        for i, (txt, fn) in enumerate(names):
            buttons.append(
                Btn(
                    rect=pg.Rect(0, 0, 180, 40),
                    text=txt,
                    function=fn,
                    text_size=FontCfg.BUTTON_TEXT_SIZE,
                ).move_center(Cfg.RESOLUTION.h_width, 100 + 45 * i)
            )
        self.objects += [
            ButtonController(buttons),
            Text("PAUSE", 40, font=FontCfg.TITLE).move_center(Cfg.RESOLUTION.h_width, 35),
        ]

    def process_event(self, event: Event) -> None:
        super().process_event(event)
        if is_esc_pressed(event):
            SceneManager().pop()
