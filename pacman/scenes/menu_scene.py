from typing import Generator

from pygame import Rect, Surface
from pygame.event import Event

from pacman.data_core import Cfg, Colors, EvenType, FontCfg, event_append
from pacman.data_core.data_classes import Cheat
from pacman.misc import ImgObj, is_esc_pressed, rand_color
from pacman.objects import CheatController, MapViewLoader, Text
from pacman.objects.buttons import Btn, BtnController
from pacman.storage import LevelStorage, SkinStorage

from .base import BaseScene, SceneManager


class MenuScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.__map_color = rand_color()
        self.__map_view_loader = MapViewLoader()
        self.__preview = self.__generate_map_preview()
        self.__level_text = Text(f"{LevelStorage()}", 15, font=FontCfg.TITLE).move_center(Cfg.RESOLUTION.h_width, 60)
        self.__pacman_anim = SkinStorage().current_instance.walk
        self.__pacman_preview = (
            ImgObj(self.__pacman_anim.current_image)
            .scale(75, 75)
            .move_center(Cfg.RESOLUTION.h_width + Cfg.RESOLUTION.h_width // 2, Cfg.RESOLUTION.h_height)
        )

    # region Private

    def _generate_objects(self) -> Generator:
        yield self.__level_text
        yield Text("PACMAN", 36, font=FontCfg.TITLE).move_center(Cfg.RESOLUTION.h_width, 30)
        yield self.__level_text
        yield BtnController(self.__get_buttons())
        yield CheatController([Cheat("pycman", lambda: event_append(EvenType.UNLOCK_SAVES))])

    def __play_game(self) -> None:
        from pacman.scenes.main_scene import MainScene

        event_append(EvenType.SET_SETTINGS)
        SceneManager().append(MainScene(self.__map_color))

    def __get_buttons(self) -> list[Btn]:
        from .levels_scene import LevelsScene
        from .records_scene import RecordsScene
        from .settings_scene import SettingsScene
        from .skins_scene import SkinsScene

        scene_manager = SceneManager()
        names = [
            ("PLAY", self.__play_game),
            ("LEVELS", lambda: scene_manager.append(LevelsScene())),
            ("SKINS", lambda: scene_manager.append(SkinsScene())),
            ("RECORDS", lambda: scene_manager.append(RecordsScene())),
            ("SETTINGS", lambda: scene_manager.append(SettingsScene())),
            ("EXIT", lambda: event_append(EvenType.EXIT)),
        ]
        buttons = []
        for i, (name, fn) in enumerate(names):
            buttons.append(
                Btn(
                    rect=Rect(0, 0, 180, 26),
                    text=name,
                    function=fn,
                    text_size=FontCfg.BUTTON_TEXT_SIZE,
                ).move_center(Cfg.RESOLUTION.h_width // 1.5, 92 + i * 28)
            )
        return buttons

    def __generate_map_preview(self) -> ImgObj:
        self.__map_color = rand_color()
        map_preview = self.__map_view_loader.get_view(LevelStorage().current).prerender()
        return map_preview.swap_color(Colors.MAIN_MAP, self.__map_color).scale(*tuple(Cfg.RESOLUTION)).blur(3)

    # endregion

    # region Public

    def process_logic(self) -> None:
        super().process_logic()
        self.__pacman_anim.update()

    def process_event(self, event: Event) -> None:
        super().process_event(event)
        if is_esc_pressed(event):
            self.__preview = self.__generate_map_preview()

    def draw(self) -> Surface:
        self.__preview.draw(self._screen)
        self._objects.draw(self._screen)
        self.__pacman_preview.image = self.__pacman_anim.current_image
        self.__pacman_preview.scale(75, 75).draw(self._screen)
        return self._screen

    def on_enter(self) -> None:
        self.__pacman_anim = SkinStorage().current_instance.walk
        self.__level_text.text = f"{LevelStorage()}"

    # endregion
