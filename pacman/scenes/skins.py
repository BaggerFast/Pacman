import pygame as pg
from pygame.event import Event

from pacman.data_core import PathManager, Dirs, Config
from pacman.misc import Font, BUTTON_SKIN_BUY
from pacman.misc.serializers import MainStorage, SkinStorage
from pacman.misc.skins import Skin
from pacman.misc.util import is_esc_pressed
from pacman.objects import ButtonController, Text, Button, ImageObject
from pacman.scene_manager import SceneManager
from pacman.scenes.base_scene import BaseScene


class SkinsScene(BaseScene):
    def _create_objects(self) -> None:
        self.button_pos_x = Config.RESOLUTION.half_width - 65
        self.button_pos_y = 90
        self.button_pos_multiply_y = 25

        self.fruit_images = PathManager.get_list_path(f"{Dirs.IMAGE}/fruit", ext="png")

        self.skins = [
            ("PACMAN", self.game.skins.default),
            ("HALF-LIFE", self.game.skins.half_life),
            ("WINDOWS", self.game.skins.windows),
            ("POKEBALL", self.game.skins.pokeball),
            ("EDGE", self.game.skins.edge),
            ("CHROME", self.game.skins.chrome),
        ]
        self.preview = self.game.skins.current.prerender_surface()

        self.objects += [
            Text("SELECT SKIN", 25, font=Font.TITLE).move_center(Config.RESOLUTION.half_width, 30),
            self.preview,
        ]
        self.create_buttons()
        self.create_fruits_and_text_we_have()
        self.create_fruits_and_text_for_skins()

    def create_fruits_and_text_we_have(self) -> None:
        for i, fruit_img in enumerate(self.fruit_images):
            self.objects += [
                ImageObject(fruit_img, (Config.RESOLUTION.WIDTH // 8 - 9 + i * 25, 60)),
                Text(f"{MainStorage().eaten_fruits[i]}", 10).move_center(
                    Config.RESOLUTION.WIDTH // 8 - 10 + i * 25, 60
                ),
            ]

    def create_fruits_and_text_for_skins(self) -> None:
        index_pos_y = self.button_pos_multiply_y
        index_pos_x = 20
        pos_regarding_buttons_x = self.button_pos_x + 45
        pos_regarding_buttons_y = self.button_pos_y - 6
        for i, (skin_name, skin) in enumerate(self.skins):
            multiply_x = 0
            if not skin.is_unlocked:
                for j in skin.skin_cost:
                    fruit = ImageObject(
                        self.fruit_images[j],
                        (
                            pos_regarding_buttons_x + index_pos_x * multiply_x,
                            pos_regarding_buttons_y + index_pos_y * i,
                        ),
                    )
                    text = Text(f"{skin.skin_cost[j]}", 10).move_center(
                        pos_regarding_buttons_x + index_pos_x * multiply_x,
                        pos_regarding_buttons_y + index_pos_y * i,
                    )
                    self.objects += [fruit, text]
                    multiply_x += 1

    def skin_button(self, skin: Skin):
        self.preview.image = skin.image.image

    def select_skin(self, skin: Skin) -> None:
        if skin.is_unlocked:
            self.game.skins.current = skin
            SceneManager().pop()
            return
        for key in skin.skin_cost.keys():
            if MainStorage().eaten_fruits[key] < skin.skin_cost[key]:
                return
        for key in skin.skin_cost.keys():
            MainStorage().store_fruit(key, -skin.skin_cost[key])
        SkinStorage().unlock_skin(skin.name)
        self.game.skins.current = skin
        SceneManager().pop()

    def create_buttons(self) -> None:
        buttons = []
        for i, (skin_name, skin) in enumerate(self.skins):
            if skin.is_unlocked:
                buttons.append(
                    Button(
                        game=self.game,
                        rect=pg.Rect(0, 0, 90, 25),
                        text=skin_name,
                        function=lambda s=skin: self.select_skin(s),
                        select_function=lambda s=skin: self.skin_button(s),
                        text_size=Font.BUTTON_FOR_SKINS_TEXT_SIZE,
                    ).move_center(self.button_pos_x, self.button_pos_y + i * self.button_pos_multiply_y)
                )
            else:
                buttons.append(
                    Button(
                        game=self.game,
                        rect=pg.Rect(0, 0, 90, 25),
                        text=skin_name,
                        function=lambda s=skin: self.select_skin(s),
                        select_function=lambda s=skin: self.skin_button(s),
                        text_size=Font.BUTTON_FOR_SKINS_TEXT_SIZE,
                        colors=BUTTON_SKIN_BUY,
                    ).move_center(self.button_pos_x, self.button_pos_y + i * self.button_pos_multiply_y)
                )

        buttons.append(
            Button(
                game=self.game,
                rect=pg.Rect(0, 0, 180, 40),
                text="MENU",
                function=SceneManager().pop,
                select_function=lambda: self.skin_button(self.game.skins.default),
                text_size=Font.BUTTON_TEXT_SIZE,
            ).move_center(Config.RESOLUTION.half_width, 250)
        )
        self.objects.append(ButtonController(buttons))

    def process_event(self, event: Event) -> None:
        super().process_event(event)
        if is_esc_pressed(event):
            SceneManager().pop()
