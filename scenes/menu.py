from random import randint

import pygame as pg
from PIL import ImageFilter, Image
from objects import ButtonController, Text, ImageObject
from scenes import base
from misc import Font, Color, VERSION


def rand_color():
    max_states = 7
    min_val = 200
    max_val = 230
    state = randint(0, max_states)
    if state == max_states:
        color = (255, 255, 255)
    elif state == max_states - 1:
        color = (randint(min_val, max_val), 0, 0)
    elif state == max_states - 2:
        color = (0, randint(min_val, max_val), 0)
    elif state == max_states - 3:
        color = (0, 0, randint(min_val, max_val))
    else:
        excluded_color = randint(0, 2)
        color = (randint(min_val, max_val) if excluded_color != 0 else 0,
                 randint(min_val, max_val) if excluded_color != 1 else 0,
                 randint(min_val, max_val) if excluded_color != 2 else 0)
    return color


class Scene(base.Scene):
    def __init__(self, game):
        self.first_run = True
        super(Scene, self).__init__(game)

    def create_objects(self) -> None:
        self.objects = []
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
        super(Scene, self).on_activate()

    def change_color(self) -> None:
        for x in range(self.preview.get_width()):
            for y in range(self.preview.get_height()):
                if self.preview.get_at((x, y)) == Color.MAIN_MAP:
                    self.preview.set_at((x, y), self.color)  # Set the color of the pixel

    def blur_preview(self) -> None:
        blur_count = 5
        rect = self.preview.get_rect()
        surify = pg.image.tostring(self.preview, 'RGBA')
        impil = Image.frombytes('RGBA', (rect.width, rect.height), surify)
        piler = impil.resize(self.game.size).\
            filter(ImageFilter.GaussianBlur(radius=blur_count))
        self.preview = pg.image.fromstring(piler.tobytes(), piler.size, piler.mode).convert()

    def animation_launch(self):
        self.game.timer = pg.time.get_ticks() / 1000

    def create_title(self) -> None:
        title = Text(self.game, 'PACMAN', 36, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        self.static_objects.append(title)

    def __create_indicator(self) -> None:
        self.__indicator = Text(self.game, self.game.maps.level_name(self.game.maps.cur_id).replace('_', ' '), 15, font=Font.TITLE)
        self.__indicator.move_center(self.game.width // 2, 60)
        self.objects.append(self.__indicator)

    def create_buttons(self) -> None:
        names = [
            ("PLAY", self.game.scenes.MAIN),
            ("LEVELS", self.game.scenes.LEVELS),
            ("SKINS", self.game.scenes.SKINS),
            ("RECORDS", self.game.scenes.RECORDS),
            ("SETTINGS", self.game.scenes.SETTINGS),
            ("CREDITS", self.game.scenes.CREDITS),
            ("EXIT", self.game.exit_game)
        ]
        buttons = []
        for i in range(len(names)):
            buttons.append(
                self.SceneButton(
                    game=self.game,
                    geometry=pg.Rect(0, 0, 180, 26),
                    text=names[i][0],
                    scene=names[i][1],
                    center=(self.game.width // 2, 95 + i * 28),
                    text_size=Font.BUTTON_TEXT_SIZE
                )
            )
        self.objects.append(ButtonController(self.game, buttons))
