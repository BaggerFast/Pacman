from typing import Generator

from pygame import Rect
from pygame.event import Event

from pacman.animator import sprite_slice
from pacman.data_core import Cfg, Colors, FontCfg
from pacman.misc import ImgObj, is_esc_pressed
from pacman.objects import Text
from pacman.objects.buttons import Btn, BtnController
from pacman.storage import LevelStorage

from .base import BaseScene, SceneManager


class RecordsScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.__error_text = Text("NO RECORDS", 24, color=Colors.RED).move_center(Cfg.RESOLUTION.h_width, 100)
        self.__highscores = LevelStorage().current_highscores()

    # region Private

    def _generate_objects(self) -> Generator:
        yield Text(f"{LevelStorage()}", 15, font=FontCfg.TITLE).move_center(Cfg.RESOLUTION.h_width, 60)
        yield Text("RECORDS", 32, font=FontCfg.TITLE).move_center(Cfg.RESOLUTION.h_width, 30)
        yield BtnController(self.__get_buttons())
        for medal in self.__get_medals():
            yield medal

    @staticmethod
    def __get_buttons() -> list[Btn]:
        return [
            Btn(
                rect=Rect(0, 0, 180, 40),
                text="MENU",
                function=SceneManager().pop,
                text_size=FontCfg.BUTTON_TEXT_SIZE,
            ).move_center(Cfg.RESOLUTION.h_width, 250)
        ]

    def __get_medals(self) -> Generator:
        medals_sprite = sprite_slice("other/medals", (16, 16))
        text_colors = [Colors.GOLD, Colors.SILVER, Colors.BRONZE, Colors.WHITE, Colors.WHITE]

        for i in range(len(self.__highscores)):
            if i > len(medals_sprite) and i > len(text_colors):
                return
            yield Text(f"{self.__highscores[i]}", 25, Rect(60, 75 + 35 * i, 0, 0), text_colors[i])
            yield ImgObj(medals_sprite[i], (16, 75 + 35 * i)).scale(30, 30)

    # endregion

    # region Public

    def draw(self) -> None:
        super().draw()
        if not len(self.__highscores):
            self.__error_text.draw(self._screen)
        return self._screen

    def process_event(self, event: Event) -> None:
        super().process_event(event)
        if is_esc_pressed(event):
            SceneManager().pop()

    # endregion
