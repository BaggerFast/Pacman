import pygame as pg
from PIL import ImageFilter, Image
from objects import Text, ImageObject
from objects.button import Button
from objects.map import rand_color
from misc import Font, Color, VERSION
from scenes.base import BaseScene


class MenuScene(BaseScene):
    def __init__(self, game):
        self.first_run = True
        super().__init__(game)

    def create_objects(self) -> None:
        self.objects: list = []
        self.preview = self.game.maps.full_surface
        self.color = rand_color()
        self.game.map_color = self.color
        self.change_color()
        self.blur_preview()
        self.image = ImageObject(self.game, self.preview, (0, 0))
        self.objects.append(self.image)
        self.create_buttons()
        self.__create_indicator()
        self.animation_launch()
        ver = Text(self.game, VERSION, 8, font=Font.TITLE)
        ver.move(self.game.width - 50, 270)
        self.objects.append(ver)

    def on_activate(self) -> None:
        self.game.pred = False
        super().on_activate()

    def change_color(self) -> None:
        for x in range(self.preview.get_width()):
            for y in range(self.preview.get_height()):
                if self.preview.get_at((x, y)) == Color.MAIN_MAP:
                    self.preview.set_at((x, y), self.color)

    def blur_preview(self) -> None:
        blur_count = 5
        rect = self.preview.get_rect()
        surify = pg.image.tostring(self.preview, 'RGBA')
        impil = Image.frombytes('RGBA', (rect.width, rect.height), surify)
        piler = impil.resize(self.game.size). \
            filter(ImageFilter.GaussianBlur(radius=blur_count))
        self.preview = pg.image.fromstring(piler.tobytes(), piler.size, piler.mode).convert()

    def animation_launch(self):
        self.game.timer = pg.time.get_ticks() / 1000

    def create_title(self) -> None:
        title = Text(self.game, 'PACMAN', 36, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        self.static_objects.append(title)

    def __create_indicator(self) -> None:
        self.__indicator = Text(self.game, self.game.maps.level_name, 15,
                                font=Font.TITLE)
        self.__indicator.move_center(self.game.width // 2, 60)
        self.objects.append(self.__indicator)

    def button_init(self):
        names = {
            "PLAY": self.game.scenes.MAIN,
            "LEVELS": self.game.scenes.LEVELS,
            "SKINS": self.game.scenes.SKINS,
            "RECORDS": self.game.scenes.RECORDS,
            "SETTINGS": self.game.scenes.SETTINGS,
            "CREDITS": self.game.scenes.CREDITS,
            "EXIT": self.game.exit_game,
        }
        for i, (name, func) in enumerate(names.items()):
            yield Button(
                game=self.game,
                rect=pg.Rect(0, 0, 180, 26),
                text=name,
                function=func,
                center=(self.game.width // 2, 95 + i * 28),
                text_size=Font.BUTTON_TEXT_SIZE
            )
