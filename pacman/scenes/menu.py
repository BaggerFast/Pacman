import pygame as pg
from pacman.data_core import Colors, Config
from pacman.events.events import EvenType
from pacman.events.utils import event_append
from pacman.misc import Font
from pacman.misc.serializers import LevelStorage, StorageLoader
from pacman.objects import ButtonController, Text, Button, ImageObject
from pacman.objects.map import rand_color
from pacman.scene_manager import SceneManager
from pacman.scenes.base_scene import BaseScene


class MenuScene(BaseScene):
    def _create_objects(self) -> None:
        super()._create_objects()
        self.preview = ImageObject(self.game.maps.full_surface).swap_color(Colors.MAIN_MAP, rand_color()).blur(3)
        self.preview.scale(*tuple(Config.RESOLUTION))
        self.__level_text = Text(f"{LevelStorage()}", 15, font=Font.TITLE).move_center(Config.RESOLUTION.half_width, 60)
        self.objects += [
            self.preview,
            Text("PACMAN", 36, font=Font.TITLE).move_center(Config.RESOLUTION.half_width, 30),
            self.__level_text,
        ]
        self.create_buttons()

    def play_game(self) -> None:
        from pacman.scenes.main import MainScene

        event_append(EvenType.SET_SETTINGS)
        SceneManager().append(MainScene(self.game))

    def create_buttons(self) -> None:
        from pacman.scenes.skins import SkinsScene
        from pacman.scenes.levels import LevelsScene
        from pacman.scenes.records import RecordsScene
        from pacman.scenes.settings import SettingsScene

        scene_manager = SceneManager()
        names = [
            ("PLAY", self.play_game),
            ("LEVELS", lambda: scene_manager.append(LevelsScene(self.game))),
            ("SKINS", lambda: scene_manager.append(SkinsScene(self.game))),
            ("RECORDS", lambda: scene_manager.append(RecordsScene(self.game))),
            ("SETTINGS", lambda: scene_manager.append(SettingsScene(self.game))),
            ("EXIT", lambda: event_append(EvenType.EXIT)),
        ]
        buttons = []
        for i, (name, fn) in enumerate(names):
            buttons.append(
                Button(
                    game=self.game,
                    rect=pg.Rect(0, 0, 180, 26),
                    text=name,
                    function=fn,
                    text_size=Font.BUTTON_TEXT_SIZE,
                ).move_center(Config.RESOLUTION.half_width, 95 + i * 28)
            )
        self.objects.append(ButtonController(buttons))

    def on_enter(self) -> None:
        self.__level_text.text = f"{LevelStorage()}"
