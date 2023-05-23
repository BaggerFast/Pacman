from typing import Generator

from pygame import Rect
from pygame.event import Event

from pacman.data_core import Cfg, FontCfg
from pacman.misc import is_esc_pressed
from pacman.objects import Btn, BtnController, Text
from pacman.objects.buttons import BTN_GREEN_COLORS, BTN_RED_COLORS, BoolBtn
from pacman.storage import SettingsStorage

from .base import BaseScene, SceneManager


class SettingsScene(BaseScene):
    def __init__(self):
        super().__init__()

        self.__volume_pos_y = 180
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
            BoolBtn(
                state=not SettingsStorage().MUTE,
                text="SOUND",
                rect=Rect(0, 0, 180, 35),
                color_true=BTN_GREEN_COLORS,
                color_false=BTN_RED_COLORS,
                text_size=FontCfg.BUTTON_TEXT_SIZE,
                function=self.__update_mute,
            ).move_center(Cfg.RESOLUTION.h_width, 75),
            BoolBtn(
                state=SettingsStorage().fun,
                text="FUN",
                rect=Rect(0, 0, 180, 35),
                color_true=BTN_GREEN_COLORS,
                color_false=BTN_RED_COLORS,
                text_size=FontCfg.BUTTON_TEXT_SIZE,
                function=SettingsStorage().update_fun,
            ).move_center(Cfg.RESOLUTION.h_width, 115),
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
            Btn(
                rect=Rect(0, 0, 180, 40),
                text="BACK",
                function=SceneManager().pop,
                text_size=FontCfg.BUTTON_TEXT_SIZE,
            ).move_center(Cfg.RESOLUTION.h_width, 250),
        ]

    def click_sound(self, step):
        SettingsStorage().set_volume(SettingsStorage().volume + step)
        self.__volume_text.text = f"{SettingsStorage().volume}%"
        self.__volume_text.move_center(Cfg.RESOLUTION.h_width, self.__volume_pos_y)

    @staticmethod
    def __update_mute():
        SettingsStorage().MUTE = not SettingsStorage().MUTE

    # endregion

    # region Public

    def process_event(self, event: Event) -> None:
        super().process_event(event)
        if is_esc_pressed(event):
            SceneManager().pop()

    # endregion
