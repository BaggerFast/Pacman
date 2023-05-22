from typing import Generator

from pygame import Rect
from pygame.event import Event

from pacman.animator import sprite_slice
from pacman.data_core import Cfg, FontCfg
from pacman.misc import ImgObj, is_esc_pressed
from pacman.objects import Btn, BtnController, Text
from pacman.objects.buttons import BTN_DEF_COLORS, BTN_SKIN_BUY
from pacman.skin import SkinEnum
from pacman.storage import FruitStorage, SkinStorage

from .base import BaseScene, SceneManager


class SkinsScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.__skin_storage = SkinStorage()
        self.__fruit_sprite = sprite_slice(f"other/fruits", (12, 12))
        self.__preview = self.__get_skin_preview(self.__skin_storage.current)

        self.__button_pos_x = Cfg.RESOLUTION.h_width - 65
        self.__button_pos_y = 90
        self.__button_pos_multiply_y = 22
        self.__skins = sorted(SkinEnum, key=lambda s: self.__skin_storage.is_unlocked(s), reverse=True)

    # region Private

    def _generate_objects(self) -> Generator:
        yield Text("SELECT SKIN", 25, font=FontCfg.TITLE).move_center(Cfg.RESOLUTION.h_width, 30)
        yield self.__preview
        yield self.__get_buttons()
        for fruit in self.__get_fruit_bar():
            yield fruit
        for fruit_price in self.__get_fruit_price():
            yield fruit_price

    @staticmethod
    def __get_skin_preview(skin: SkinEnum) -> ImgObj:
        pos = Cfg.RESOLUTION.h_width + Cfg.RESOLUTION.h_width // 2, Cfg.RESOLUTION.h_height
        return skin.value.preview.scale(80, 80).move_center(*pos)

    def __get_fruit_bar(self) -> Generator:
        for i, fruit_img in enumerate(self.__fruit_sprite):
            yield ImgObj(fruit_img, (Cfg.RESOLUTION.WIDTH // 7 + i * 25, 60))
            yield Text(f"{FruitStorage().eaten_fruits[i]}", 10).move_center(Cfg.RESOLUTION.WIDTH // 7 + i * 25, 60)

    def __get_fruit_price(self) -> Generator:
        index_pos_y = self.__button_pos_multiply_y
        index_pos_x = 20
        pos_regarding_buttons_x = self.__button_pos_x + 45
        pos_regarding_buttons_y = self.__button_pos_y - 6
        for i, skin in enumerate(self.__skins):
            multiply_x = 0
            if not self.__skin_storage.is_unlocked(skin):
                skin_class = skin.value
                for j in skin_class.cost:
                    y = pos_regarding_buttons_y + index_pos_y * i
                    x = pos_regarding_buttons_x + index_pos_x * multiply_x
                    yield ImgObj(self.__fruit_sprite[j], (x, y))
                    yield Text(f"{skin_class.cost[j]}", 10).move_center(x, y)
                    multiply_x += 1

    def __get_buttons(self) -> BtnController:
        buttons = []
        btn_active_index = 0
        for i, skin in enumerate(self.__skins):
            colors = BTN_DEF_COLORS if self.__skin_storage.is_unlocked(skin) else BTN_SKIN_BUY
            skin_name = f"-{skin.value.name}-" if SkinStorage().current is skin else skin.value.name
            buttons.append(
                Btn(
                    rect=Rect(0, 0, 90, 20),
                    text=skin_name,
                    function=lambda s=skin: self.__select_skin(s),
                    select_function=lambda s=skin: self.__set_preview(s),
                    text_size=FontCfg.BUTTON_FOR_SKINS_TEXT_SIZE,
                    colors=colors,
                ).move_center(self.__button_pos_x, self.__button_pos_y + i * self.__button_pos_multiply_y)
            )
            if skin is SkinStorage().current:
                btn_active_index = len(buttons) - 1

        buttons.append(
            Btn(
                rect=Rect(0, 0, 180, 40),
                text="MENU",
                function=SceneManager().pop,
                select_function=lambda: self.__set_preview(self.__skin_storage.current),
                text_size=FontCfg.BUTTON_TEXT_SIZE,
            ).move_center(Cfg.RESOLUTION.h_width, 250)
        )
        return BtnController(buttons, btn_active_index)

    def __set_preview(self, skin: SkinEnum) -> None:
        self.__preview.image = self.__get_skin_preview(skin).image

    def __select_skin(self, skin: SkinEnum) -> None:
        if self.__skin_storage.is_unlocked(skin):
            self.__skin_storage.set_skin(skin)
            SceneManager().pop()
            return

        skin_class = skin.value

        for key in skin_class.cost.keys():
            if FruitStorage().eaten_fruits[key] < skin_class.cost[key]:
                return
        for key in skin_class.cost.keys():
            FruitStorage().store_fruit(key, -abs(skin_class.cost[key]))

        self.__skin_storage.unlock_skin(skin)
        SceneManager().pop()

    # endregion

    # region Public

    def process_event(self, event: Event) -> None:
        super().process_event(event)
        if is_esc_pressed(event):
            SceneManager().pop()

    # endregion
