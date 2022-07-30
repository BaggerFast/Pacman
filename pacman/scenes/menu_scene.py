import pygame as pg
from PIL import ImageFilter, Image
from misc.constants import Font, Color
from misc.storage import LevelStorage
from pacman.objects.map import rand_color
from pacman.objects import Text, ImageObject
from .base_scene import BaseScene
from .manager import SceneManager
from .util import MenuPreset
from ..buttons import ButtonManager, Button
from ..buttons.util import BTN_MENU


class MenuScene(BaseScene):

    def _setup_logic(self) -> None:
        self.preview = self.game.maps.full_surface
        self.color = rand_color()
        self.change_color()
        self.blur()

    def _create_objects(self) -> None:
        yield ImageObject(self.game, self.preview, (0, 0))
        yield self.__get_btn_manager()
        yield Text(self.game, 'PACMAN', 36, font=Font.TITLE).move_center(self.game.width // 2, 30)
        yield Text(self.game, str(LevelStorage()), 15, font=Font.TITLE).move_center(self.game.width // 2, 60)

    def __get_btn_manager(self):
        from . import MainScene, LevelScene, SkinScene, RecordsScene, SettingsScene
        sc = SceneManager()
        names = [
            MenuPreset("PLAY", lambda: sc.reset(MainScene(self.game))),
            MenuPreset("LEVELS", lambda: sc.append(LevelScene(self.game))),
            MenuPreset("SKINS", lambda: sc.append(SkinScene(self.game))),
            MenuPreset("RECORDS", lambda: sc.append(RecordsScene(self.game))),
            MenuPreset("SETTINGS", lambda: sc.append(SettingsScene(self.game))),
            MenuPreset("EXIT", self.game.exit_game),
        ]

        buttons = []
        for i, preset in enumerate(names):
            buttons.append(
                Button(
                    game=self.game,
                    geometry=pg.Rect(0, 0, 180, 26),
                    text=preset.name,
                    function=preset.func,
                    center=(self.game.width // 2, 95 + i * 28),
                    colors=BTN_MENU
                )
            )
        return ButtonManager(self.game, buttons)

    def change_color(self):
        for x in range(self.preview.get_width()):
            for y in range(self.preview.get_height()):
                if self.preview.get_at((x, y)) == Color.MAIN_MAP:
                    self.preview.set_at((x, y), self.color)

    def blur(self):
        blur_count = 5
        rect = self.preview.get_rect()
        surify = pg.image.tostring(self.preview, 'RGBA')
        impil = Image.frombytes('RGBA', (rect.width, rect.height), surify)
        piler = impil.resize(self.game.size).filter(ImageFilter.GaussianBlur(radius=blur_count))
        self.preview = pg.image.fromstring(piler.tobytes(), piler.size, piler.mode).convert()
