from copy import copy
from typing import Generator

from pygame import KEYDOWN, Surface
from pygame.event import Event

from pacman.data_core import Cfg, Colors, FontCfg, KbKeys
from pacman.data_core.enums import SoundCh
from pacman.misc import ImgObj, is_esc_pressed
from pacman.objects import Btn, BtnController, MapViewLoader, Text
from pacman.sound import SoundController, Sounds
from pacman.storage import LevelStorage

from .base import BaseScene, SceneManager


class LevelsScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.__map_view_loader = MapViewLoader()

        self.preview = self.__get_level_preview(self.__current_level)

        self.text_level = Text("", 20)

        self.text_l = Text("L", 40, color=Colors.DARK_GRAY).move_center(
            Cfg.RESOLUTION.WIDTH // 6 - 10, Cfg.RESOLUTION.h_height
        )

        self.text_r = Text("R", 40, color=Colors.DARK_GRAY).move_center(
            Cfg.RESOLUTION.WIDTH - (Cfg.RESOLUTION.WIDTH // 6 - 16), Cfg.RESOLUTION.h_height
        )

        self.__set_text_level()

    # region Private

    def _generate_objects(self) -> Generator:
        yield Text("SELECT LEVEL", 25, font=FontCfg.TITLE).move_center(Cfg.RESOLUTION.h_width, 30)
        yield self.preview
        yield self.text_level
        yield BtnController(self.__get_buttons())

    @property
    def __current_level(self) -> int:
        return LevelStorage().current

    def __get_buttons(self) -> list[Btn]:
        return [
            Btn(
                text="",
                rect=copy(self.preview.rect),
                function=SceneManager().pop,
                text_size=FontCfg.BUTTON_TEXT_SIZE,
            )
        ]

    def __get_level_preview(self, level_id: id) -> ImgObj:
        map_preview = self.__map_view_loader.get_view(level_id).prerender()
        scale = Cfg.RESOLUTION.WIDTH * 0.6, Cfg.RESOLUTION.HEIGHT * 0.6
        return map_preview.smoothscale(*scale).move_center(Cfg.RESOLUTION.h_width, Cfg.RESOLUTION.h_height)

    def __update_preview(self):
        SoundController.play(SoundCh.SYSTEM, Sounds.CLICK)
        self.preview.image = self.__get_level_preview(self.__current_level).image
        self.__set_text_level()

    def __set_text_level(self) -> None:
        self.text_level.text = f"Level: {self.__current_level + 1}/{LevelStorage().len}"
        self.text_level.move_center(Cfg.RESOLUTION.h_width, Cfg.RESOLUTION.h_height)

    # endregion

    # region Public

    def draw(self) -> Surface:
        super().draw()
        if not self.__current_level == 0:
            self.text_l.draw(self._screen)
        if not self.__current_level + 1 >= LevelStorage().len_unlocked:
            self.text_r.draw(self._screen)
        return self._screen

    def process_event(self, event: Event) -> None:
        super().process_event(event)
        if is_esc_pressed(event):
            SceneManager().pop()
        if event.type == KEYDOWN:
            if event.key in KbKeys.RIGHT and self.__current_level != LevelStorage().len - 1:
                if not (self.__current_level + 1 >= LevelStorage().len_unlocked):
                    LevelStorage().set_next_level()
                    self.__update_preview()
            elif event.key in KbKeys.LEFT and self.__current_level != 0:
                LevelStorage().set_prev_level()
                self.__update_preview()

    # endregion
