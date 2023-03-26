import pygame as pg
from PIL import ImageFilter, Image

from pacman.data_core import Colors
from pacman.misc.serializers import LevelStorage
from pacman.objects.map import rand_color
from pacman.objects import ButtonController, Text, ImageObject
from pacman.scenes import base
from pacman.misc import Font


class MenuScene(base.Scene):
    def create_objects(self) -> None:
        self.objects = []
        self.preview = self.game.maps.full_surface
        self.color = rand_color()
        self.change_color()
        self.blur()
        self.image = ImageObject(self.game, self.preview, (0, 0))
        self.objects.append(self.image)
        self.create_buttons()
        self.__create_indicator()

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
        piler = impil.resize(self.game.size).filter(ImageFilter.GaussianBlur(radius=blur_count))
        self.preview = pg.image.fromstring(piler.tobytes(), piler.size, piler.mode).convert()

    def create_title(self) -> None:
        title = Text("PACMAN", 36, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        self.static_objects.append(title)

    def __create_indicator(self) -> None:
        self.__indicator = Text(f"{LevelStorage()}", 15, font=Font.TITLE).move_center(self.game.width // 2, 60)
        self.objects.append(self.__indicator)

    def create_buttons(self) -> None:
        names = {
            0: ("PLAY", self.game.scenes.MAIN, True),
            1: ("LEVELS", self.game.scenes.LEVELS, False),
            2: ("SKINS", self.game.scenes.SKINS, False),
            3: ("RECORDS", self.game.scenes.RECORDS, False),
            4: ("SETTINGS", self.game.scenes.SETTINGS, False),
            5: ("EXIT", self.game.exit_game, None),
        }
        buttons = []
        for i in range(len(names)):
            buttons.append(
                self.SceneButton(
                    game=self.game,
                    rect=pg.Rect(0, 0, 180, 26),
                    text=names[i][0],
                    scene=(names[i][1], names[i][2]),
                    text_size=Font.BUTTON_TEXT_SIZE,
                ).move_center(self.game.width // 2, 95 + i * 28)
            )
        self.objects.append(ButtonController(buttons))
