from typing import Generator

from pygame import Rect
from pygame.event import Event

from pacman.data_core import Cfg, EvenType, FontCfg, event_append
from pacman.misc import is_esc_pressed
from pacman.objects import Btn, BtnController, Text
from pacman.objects.buttons import BTN_GREEN_COLORS, BTN_RED_COLORS
from pacman.sound import SoundController
from pacman.storage import SettingsStorage

from .base import BaseScene, SceneManager


class SettingsScene(BaseScene):
    def __init__(self):
        super().__init__()

        self.__volume_pos_y = 150
        self.__difficulty_pos = 210
        self.__volume_text = Text(f"{SettingsStorage().volume}%", 20).move_center(
            Cfg.RESOLUTION.h_width, self.__volume_pos_y
        )

    # region Private

    def _generate_objects(self) -> Generator:
        yield Text("SETTINGS", 30, font=FontCfg.TITLE).move_center(Cfg.RESOLUTION.h_width, 30)
        yield Text("VOLUME", 20).move_center(Cfg.RESOLUTION.h_width, self.__volume_pos_y - 30)
        yield self.__volume_text
        yield BtnController(self.__get_buttons())

    def __get_buttons(self) -> list[Btn]:
        return [
            Btn(
                rect=Rect(0, 0, 40, 35),
                text="-",
                function=lambda: self.click_sound(-5),
            ).move_center(Cfg.RESOLUTION.h_width - 60, self.__volume_pos_y),
            Btn(
                rect=Rect(0, 0, 40, 35),
                text="+",
                function=lambda: self.click_sound(5),
            ).move_center(Cfg.RESOLUTION.h_width + 65, self.__volume_pos_y),
        ]

    def click_sound(self, step):
        SettingsStorage().set_volume(SettingsStorage().volume + step)
        self.__volume_text.text = f"{SettingsStorage().volume}%"

    # endregion

    # region Public

    def process_event(self, event: Event) -> None:
        super().process_event(event)
        if is_esc_pressed(event):
            SceneManager().pop()

    # endregion
