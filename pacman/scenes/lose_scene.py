from typing import Generator

from pygame import Rect, Surface

from pacman.data_core import Cfg, EvenType, FontCfg, event_append
from pacman.data_core.enums import SoundCh
from pacman.objects import Btn, BtnController, Text
from pacman.sound import SoundController, Sounds
from pacman.storage import LevelStorage

from .base import BlurScene, SceneManager


class LoseScene(BlurScene):
    def __init__(self, blur_surface: Surface, score: int):
        super().__init__(blur_surface)
        self.__score = score

    # region Private

    def _generate_objects(self) -> Generator:
        yield Text("GAME", 40, font=FontCfg.TITLE).move_center(Cfg.RESOLUTION.h_width, 30)
        yield Text("OVER", 40, font=FontCfg.TITLE).move_center(Cfg.RESOLUTION.h_width, 70)
        yield Text(f"Score: {self.__score}", 20).move_center(Cfg.RESOLUTION.h_width, 135)
        yield Text(f"High score: {LevelStorage().get_highscore()}", 20).move_center(Cfg.RESOLUTION.h_width, 165)
        yield BtnController(self.__get_buttons())

    @staticmethod
    def __get_buttons() -> list[Btn]:
        from .main_scene import MainScene
        from .menu_scene import MenuScene

        names = [
            ("RESTART", lambda: SceneManager().reset(MainScene())),
            ("MENU", lambda: SceneManager().reset(MenuScene())),
        ]
        buttons = []
        for i, (name, fn) in enumerate(names):
            buttons.append(
                Btn(
                    rect=Rect(0, 0, 180, 35),
                    text=name,
                    function=fn,
                    text_size=FontCfg.BUTTON_TEXT_SIZE,
                ).move_center(Cfg.RESOLUTION.h_width, 210 + 40 * i)
            )
        return buttons

    # endregion

    # region Public

    def on_first_enter(self) -> None:
        event_append(EvenType.GET_SETTINGS)
        SoundController.reset_play(SoundCh.BACKGROUND, Sounds.LOSE)

    def on_last_exit(self) -> None:
        SoundController.stop(SoundCh.BACKGROUND)

    # endregion
