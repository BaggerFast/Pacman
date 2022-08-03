import pygame as pg
from PIL import ImageFilter, Image
from misc.animator.animator import Animator1
from misc.animator.sprite_sheet import SpriteSheet
from misc.constants import Font, Color
from misc.storage import LevelStorage, SkinStorage
from pacman.objects.map import rand_color
from pacman.objects import Text, ImageObject
from .base_scene import BaseScene
from .manager import SceneManager
from .util import MenuPreset
from ..buttons import ButtonManager, Button
from ..buttons.util import BTN_MENU


# todo ui


class MenuScene(BaseScene):

    def _setup_logic(self) -> None:
        self.preview = self.game.maps.full_surface
        self.color = rand_color()

        sptite = SpriteSheet(f'pacman/{SkinStorage().current}/walk.png', (13, 13))[0]
        self.pacman_anim = Animator1(sptite, time_out=85)
        self.pacman_anim.start()

        self.change_color()
        self.blur()

    def _create_objects(self) -> None:
        yield ImageObject(self.preview, (0, 0))
        yield self.__get_btn_manager()
        yield Text('PACMAN', 36, font=Font.TITLE).move_center(self.game.width // 2, 35)

        margin = self.game.width // 2 + 8
        texts = [f'Coins:50', f'{LevelStorage()}',
                 f'1st:{LevelStorage().get_current_records(True)}', f'{SkinStorage()}']
        for i, text in enumerate(texts):
            yield Text(text, 13, color=Color.GRAY).move(margin, 85 + i * 28)

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

        buttons = [
            Button(
                geometry=pg.Rect(0, 0, 180, 26),
                text=preset.name,
                function=preset.func,
                center=(self.game.width // 2 - 55, 92 + i * 28),
                colors=BTN_MENU
            )
            for i, preset in enumerate(names)
        ]
        return ButtonManager(buttons)

    def update(self):
        self.pacman_anim.update()
        super().update()

    def render(self, screen: pg.Surface):
        super().render(screen)
        pg.draw.line(screen, Color.GRAY, (self.game.width // 2, 80), (self.game.width // 2, 247))
        image = pg.transform.scale(self.pacman_anim.current_image, (50, 50))
        screen.blit(image, (self.game.width // 2 + 8, 197))

    def change_color(self):
        for x in range(self.preview.get_width()):
            for y in range(self.preview.get_height()):
                if self.preview.get_at((x, y)) == Color.MAIN_MAP:
                    self.preview.set_at((x, y), self.color)

    def blur(self):
        blur_count = 3
        rect = self.preview.get_rect()
        surify = pg.image.tostring(self.preview, 'RGBA')
        impil = Image.frombytes('RGBA', (rect.width, rect.height), surify)
        piler = impil.resize(self.game.size).filter(ImageFilter.GaussianBlur(radius=blur_count))
        self.preview = pg.image.fromstring(piler.tobytes(), piler.size, piler.mode).convert()
