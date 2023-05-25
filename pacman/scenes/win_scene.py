from typing import Generator

from pygame import Rect, Surface
from pygame.event import Event

from pacman.data_core import Cfg, EvenType, FontCfg, event_append
from pacman.data_core.enums import SoundCh
from pacman.misc import is_esc_pressed
from pacman.objects import Text
from pacman.objects.buttons import Btn, BtnController
from pacman.sound import SoundController, Sounds
from pacman.storage import LevelStorage

from .base import BlurScene, SceneManager


class WinScene(BlurScene):
    def __init__(self, blur_surface: Surface, score: int):
        super().__init__(blur_surface)
        self.__score = score
        LevelStorage().add_record(self.__score)
        LevelStorage().unlock_next_level()

    # region Private

    def _generate_objects(self) -> Generator:
        yield Text("YOU", 40, font=FontCfg.TITLE).move_center(Cfg.RESOLUTION.h_width, 30)
        yield Text("WON", 40, font=FontCfg.TITLE).move_center(Cfg.RESOLUTION.h_width, 70)
        yield Text(f"Score: {self.__score}", 20).move_center(Cfg.RESOLUTION.h_width, 135)
        yield Text(f"High score: {LevelStorage().get_highscore()}", 20).move_center(Cfg.RESOLUTION.h_width, 165)
        yield BtnController(self.__get_buttons())

    @staticmethod
    def __next_level():
        from pacman.scenes.main_scene import MainScene

        LevelStorage().set_next_level()
        SceneManager().reset(MainScene())

    def __get_buttons(self) -> list[Btn]:
        from .menu_scene import MenuScene

        buttons = []

        if not LevelStorage().is_last_level():
            buttons.append(
                Btn(
                    rect=Rect(0, 0, 180, 35),
                    function=self.__next_level,
                    text="NEXT LEVEL",
                    text_size=FontCfg.BUTTON_TEXT_SIZE,
                ).move_center(Cfg.RESOLUTION.h_width, 210)
            )
        buttons.append(
            Btn(
                rect=Rect(0, 0, 180, 35),
                text="MENU",
                function=lambda: SceneManager().reset(MenuScene()),
                text_size=FontCfg.BUTTON_TEXT_SIZE,
            ).move_center(Cfg.RESOLUTION.h_width, 250)
        )
        return buttons

    # endregion

    # region Public

    def process_event(self, event: Event) -> None:
        super().process_event(event)
        if is_esc_pressed(event):
            from pacman.scenes.menu_scene import MenuScene

            SceneManager().reset(MenuScene())

    def on_first_enter(self) -> None:
        SoundController.reset_play(SoundCh.BACKGROUND, Sounds.WIN)

    def on_last_exit(self) -> None:
        event_append(EvenType.SET_SETTINGS)
        SoundController.stop(SoundCh.BACKGROUND)

    # endregion
