import pygame as pg
from PIL import ImageFilter, Image

from pacman.data_core import Colors, Config
from pacman.misc import Font
from pacman.misc.serializers import LevelStorage
from pacman.objects import ButtonController, Text, ImageObject, Button
from pacman.objects.map import rand_color
from pacman.scene_manager import SceneManager
from pacman.scenes.base_scene import BaseScene


class MenuScene(BaseScene):

    def _create_objects(self) -> None:
        self.preview = self.game.maps.full_surface
        self.color = rand_color()
        self.change_color()
        self.blur()
        self.image = ImageObject(self.preview, (0, 0))
        self.objects.append(self.image)
        self.create_buttons()
        self.__create_indicator()
        self.objects.append(Text("PACMAN", 36, font=Font.TITLE).move_center(Config.RESOLUTION.half_width, 30))

    def change_color(self):
        for x in range(self.preview.get_width()):
            for y in range(self.preview.get_height()):
                if self.preview.get_at((x, y)) == Colors.MAIN_MAP:
                    self.preview.set_at((x, y), self.color)

    def blur(self):
        blur_count = 5
        rect = self.preview.get_rect()
        surify = pg.image.tostring(self.preview, "RGBA")
        impil = Image.frombytes("RGBA", (rect.width, rect.height), surify)
        piler = impil.resize(tuple(Config.RESOLUTION)).filter(ImageFilter.GaussianBlur(radius=blur_count))
        self.preview = pg.image.fromstring(piler.tobytes(), piler.size, piler.mode).convert()

    def __create_indicator(self) -> None:
        self.__indicator = Text(f"{LevelStorage()}", 15, font=Font.TITLE).move_center(Config.RESOLUTION.half_width, 60)
        self.objects.append(self.__indicator)

    def create_buttons(self) -> None:
        from pacman.scenes.main import MainScene
        from pacman.scenes.skins import SkinsScene
        from pacman.scenes.levels import LevelsScene
        from pacman.scenes.records import RecordsScene
        from pacman.scenes.settings import SettingsScene

        scene_manager = SceneManager()
        names = [
            ("PLAY", lambda: scene_manager.append(MainScene(self.game))),
            ("LEVELS", lambda: scene_manager.append(LevelsScene(self.game))),
            ("SKINS", lambda: scene_manager.append(SkinsScene(self.game))),
            ("RECORDS", lambda: scene_manager.append(RecordsScene(self.game))),
            ("SETTINGS", lambda: scene_manager.append(SettingsScene(self.game))),
            ("EXIT", self.game.exit_game),
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
