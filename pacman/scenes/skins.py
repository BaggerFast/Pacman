import pygame as pg
from pygame.event import Event

from pacman.data_core import Cfg
from pacman.misc.animator.sprite_sheet import sprite_slice
from pacman.misc.constants import Font, BUTTON_SKIN_BUY
from pacman.misc.serializers import SkinStorage, FruitStorage
from pacman.misc.tmp_skin import SkinEnum
from pacman.misc.util import is_esc_pressed
from pacman.objects import Text, ImageObject
from pacman.objects.buttons import ButtonController, Button
from pacman.scene_manager import SceneManager
from pacman.scenes.base_scene import BaseScene


class SkinsScene(BaseScene):
    def _create_objects(self) -> None:
        self.skin_storage = SkinStorage()
        self.button_pos_x = Cfg.RESOLUTION.half_width - 65
        self.button_pos_y = 90
        self.button_pos_multiply_y = 25

        self.fruit_images = sprite_slice(f"fruits", (12, 12))

        self.skins = [
            ("PACMAN", SkinEnum.DEFAULT),
            ("EDGE", SkinEnum.EDGE),
            ("POKEBALL", SkinEnum.POKEBALL),
            ("WINDOWS", SkinEnum.WINDOWS),
            ("HALF-LIFE", SkinEnum.HALF_LIFE),
            ("CHROME", SkinEnum.CHROME),
        ]
        self.preview = self.skin_storage.current_instance.prerender_surface()

        self.objects += [
            Text("SELECT SKIN", 25, font=Font.TITLE).move_center(Cfg.RESOLUTION.half_width, 30),
            self.preview,
        ]
        self.create_buttons()
        self.create_fruits_and_text_we_have()
        self.create_fruits_and_text_for_skins()

    def create_fruits_and_text_we_have(self) -> None:
        for i, fruit_img in enumerate(self.fruit_images):
            self.objects += [
                ImageObject(fruit_img, (Cfg.RESOLUTION.WIDTH // 7 + i * 25, 60)),
                Text(f"{FruitStorage().eaten_fruits[i]}", 10).move_center(Cfg.RESOLUTION.WIDTH // 7 + i * 25, 60),
            ]

    def create_fruits_and_text_for_skins(self) -> None:
        index_pos_y = self.button_pos_multiply_y
        index_pos_x = 20
        pos_regarding_buttons_x = self.button_pos_x + 45
        pos_regarding_buttons_y = self.button_pos_y - 6
        for i, (skin_name, skin) in enumerate(self.skins):
            multiply_x = 0
            if not self.skin_storage.is_unlocked(skin):
                skin_class = skin.value
                for j in skin_class.skin_cost:
                    fruit = ImageObject(
                        self.fruit_images[j],
                        (
                            pos_regarding_buttons_x + index_pos_x * multiply_x,
                            pos_regarding_buttons_y + index_pos_y * i,
                        ),
                    )
                    text = Text(f"{skin_class.skin_cost[j]}", 10).move_center(
                        pos_regarding_buttons_x + index_pos_x * multiply_x,
                        pos_regarding_buttons_y + index_pos_y * i,
                    )
                    self.objects += [fruit, text]
                    multiply_x += 1

    def skin_button(self, skin: SkinEnum):
        self.preview.image = skin.value.image.image

    def select_skin(self, skin: SkinEnum) -> None:
        if self.skin_storage.is_unlocked(skin):
            self.skin_storage.set_skin(skin)
            SceneManager().pop()
            return

        skin_class = skin.value
        for key in skin_class.skin_cost.keys():
            if FruitStorage().eaten_fruits[key] < skin_class.skin_cost[key]:
                return
        for key in skin_class.skin_cost.keys():
            FruitStorage().store_fruit(key, -abs(skin_class.skin_cost[key]))

        self.skin_storage.unlock_skin(skin)
        SceneManager().pop()

    def create_buttons(self) -> None:
        buttons = []
        for i, (skin_name, skin) in enumerate(self.skins):
            if self.skin_storage.is_unlocked(skin):
                buttons.append(
                    Button(
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
                rect=pg.Rect(0, 0, 180, 40),
                text="MENU",
                function=SceneManager().pop,
                select_function=lambda: self.skin_button(self.skin_storage.current),
                text_size=Font.BUTTON_TEXT_SIZE,
            ).move_center(Cfg.RESOLUTION.half_width, 250)
        )
        self.objects.append(ButtonController(buttons))

    def process_event(self, event: Event) -> None:
        super().process_event(event)
        if is_esc_pressed(event):
            SceneManager().pop()
