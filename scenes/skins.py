import pygame as pg

from copy import copy
from misc.constants.skin_names import SkinsNames
from objects import ButtonController, Text, Button, ImageObject
from scenes import base
from misc import Font, get_list_path, BUTTON_SKIN_BUY


class Scene(base.Scene):
    class SkinButton(Button):
        def __init__(self, **args):
            self.value = args.pop("value")
            super().__init__(**args)

        def click(self) -> None:
            self.game.skins.current = self.value
            self.select()
            self.game.scenes.current.update_button_text()

        def deselect(self) -> None:
            scene = self.game.scenes.current
            if not scene.is_current:
                scene.preview.image = self.game.skins.current.image.image
            super().deselect()

        def select(self) -> None:
            scene = self.game.scenes.current
            scene.is_current = True
            scene.preview.image = self.value.image.image
            super().select()

    class BuyButton(Button):
        def __init__(self, **args):
            self.value = args.pop("value")
            super().__init__(**args)

        def click(self) -> None:
            flag = True
            self.select()
            for key in self.value.skin_cost.keys():
                flag = self.game.eaten_fruits[key] > self.value.skin_cost[key]
            if not flag:
                return
            for key in self.value.skin_cost.keys():
                self.game.store_fruit(key, -self.value.skin_cost[key])
            self.game.unlock_skin(self.value.name)
            self.game.scenes.current.create_objects()

    def create_static_objects(self) -> None:
        self.skins = {
            SkinsNames.default: self.game.skins.default,
            SkinsNames.edge: self.game.skins.edge,
            SkinsNames.pokeball: self.game.skins.pokeball,
            SkinsNames.half_life: self.game.skins.half_life,
            SkinsNames.windows: self.game.skins.windows,
            SkinsNames.chrome: self.game.skins.chrome,
        }
        self.is_current = False
        self.fruit_images: list[str] = get_list_path('images/fruit', ext='png')
        self.__create_title()

    def create_objects(self) -> None:
        self.objects = []
        self.preview = copy(self.game.skins.current.image)
        self.objects.append(self.preview)
        self.create_buttons()
        self.create_fruits_and_text_we_have()
        self.create_fruits_and_text_for_skins()

    def create_fruits_and_text_we_have(self) -> None:
        def creator():
            for i, fruit_img in enumerate(self.fruit_images):
                yield ImageObject(self.game, fruit_img, (self.game.width // 8 - 9 + i * 25, 60))
                text = Text(self.game, str(self.game.eaten_fruits[i]), 10)
                text.move_center(self.game.width // 8 - 10 + i * 25, 60)
                yield text
        self.objects += list(creator())

    def create_fruits_and_text_for_skins(self) -> None:

        def creator():
            for index, (skin_name, skin) in enumerate(self.skins.items()):
                multiply_x = 0
                if skin.is_unlocked:
                    continue
                for i in skin.skin_cost:
                    yield ImageObject(self.game, self.fruit_images[i], (
                        pos_regarding_buttons_x + index_pos_x * multiply_x,
                        pos_regarding_buttons_y + index_pos_y * index))
                    text = Text(self.game, str(skin.skin_cost[i]), 10)
                    text.move_center(pos_regarding_buttons_x + index_pos_x * multiply_x,
                                     pos_regarding_buttons_y + index_pos_y * index)
                    yield text
                    multiply_x += 1

        index_pos_y = self.button_pos_multiply_y
        index_pos_x = 20
        pos_regarding_buttons_x = self.button_pos_x + 45
        pos_regarding_buttons_y = self.button_pos_y - 6
        self.objects += list(creator())

    def __create_title(self) -> None:
        title = Text(self.game, 'SELECT SKIN', 25, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        self.static_objects.append(title)

    def button_init(self):
        for i, (skin_name, skin) in enumerate(self.skins.items()):
            if skin.is_unlocked:
                yield self.SkinButton(
                        game=self.game,
                        geometry=pg.Rect(0, 0, 90, 25),
                        text=skin_name,
                        value=skin,
                        center=(self.button_pos_x, self.button_pos_y + i * self.button_pos_multiply_y),
                        text_size=Font.BUTTON_FOR_SKINS_TEXT_SIZE,
                        active=skin.name in self.game.unlocked_skins
                )
            else:
                yield self.BuyButton(
                    game=self.game,
                    geometry=pg.Rect(0, 0, 90, 25),
                    text=skin_name,
                    value=skin,
                    center=(self.button_pos_x, self.button_pos_y + i * self.button_pos_multiply_y),
                    text_size=Font.BUTTON_FOR_SKINS_TEXT_SIZE,
                    colors=BUTTON_SKIN_BUY
                )

        yield self.SceneButton(
            game=self.game,
            geometry=pg.Rect(0, 0, 180, 40),
            text='MENU',
            scene=self.game.scenes.MENU,
            center=(self.game.width // 2, 250),
            text_size=Font.BUTTON_TEXT_SIZE
        )

    def create_buttons(self) -> None:
        self.button_pos_x = self.game.width // 2 - 65
        self.button_pos_y = 90
        self.button_pos_multiply_y = 25
        self.__button_controller = ButtonController(self.game, list(self.button_init()))
        self.objects.append(self.__button_controller)
        self.update_button_text()

    def update_button_text(self):
        for button in self.__button_controller.buttons:
            if not (hasattr(button, "value") and hasattr(button.value, "name")):
                continue
            if self.game.skins.current.name == button.value.name:
                if not (button.text.startswith("-") or button.text.endswith("-")):
                    button.text = f'-{button.text}-'
            else:
                button.text = button.text.strip('-')
