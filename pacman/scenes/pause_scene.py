from typing import Generator

from pygame import Rect
from pygame.event import Event

from pacman.data_core import Cfg, EvenType, FontCfg, event_append
from pacman.misc import is_esc_pressed
from pacman.objects import Text
from pacman.objects.buttons import Btn, BtnController

from .base import BlurScene, SceneManager


class PauseScene(BlurScene):
    # region Private

    def _generate_objects(self) -> Generator:
        yield Text("PAUSE", 40, font=FontCfg.TITLE).move_center(Cfg.RESOLUTION.h_width, 35)
        yield BtnController(self.__get_buttons())

    @staticmethod
    def __stop_game() -> None:
        from .menu_scene import MenuScene

        event_append(EvenType.GET_SETTINGS)
        SceneManager().reset(MenuScene())

    @staticmethod
    def __restart_game() -> None:
        from pacman.scenes.main_scene import MainScene

        event_append(EvenType.GET_SETTINGS)
        SceneManager().reset(MainScene())

    def __get_buttons(self) -> list[Btn]:
        names = [
            ("CONTINUE", SceneManager().pop),
            ("RESTART", self.__restart_game),
            ("MENU", self.__stop_game),
        ]
        buttons = []
        for i, (txt, fn) in enumerate(names):
            buttons.append(
                Btn(
                    rect=Rect(0, 0, 180, 40),
                    text=txt,
                    function=fn,
                    text_size=FontCfg.BUTTON_TEXT_SIZE,
                ).move_center(Cfg.RESOLUTION.h_width, 100 + 45 * i)
            )
        return buttons

    # endregion

    # region Public

    def process_event(self, event: Event) -> None:
        super().process_event(event)
        if is_esc_pressed(event):
            SceneManager().pop()

    # endregion
