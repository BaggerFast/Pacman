from copy import copy

import pygame as pg

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
            for key in self.value[1].skin_cost.keys():
                if self.game.eaten_fruits[key] < self.value[1].skin_cost[key]:
                    flag = False

            self.select()
            if flag:
                for key in self.value[1].skin_cost.keys():
                    self.game.store_fruit(key, -self.value[1].skin_cost[key])
                self.game.unlock_skin(self.value[1].name)
                self.game.scenes.current.create_objects()

        def deselect(self) -> None:
            scene = self.game.scenes.current
            if not scene.is_current:
                scene.preview.image = self.game.skins.current.image.image
            super().deselect()

        def select(self) -> None:
            scene = self.game.scenes.current
            scene.is_current = True
            scene.preview.image = self.value[1].image.image
            super().select()

    def process_event(self, event: pg.event.Event) -> None:
        self.is_current = False
        super().process_event(event)

    def create_static_objects(self) -> None:
        self.is_current = False
        self.fruit_images = get_list_path('png', 'images', 'fruit')
        self.__create_title()

    def create_objects(self) -> None:
        self.skins = {
            0: ('PACMAN', self.game.skins.default),
            1: ('EDGE', self.game.skins.edge),
            2: ('POKEBALL', self.game.skins.pokeball),
            3: ('HALF-LIFE', self.game.skins.half_life),
            4: ('WINDOWS', self.game.skins.windows),
            5: ('CHROME', self.game.skins.chrome),
        }
        self.objects = []
        self.preview = copy(self.game.skins.current.image)
        self.objects.append(self.preview)
        self.create_buttons()
        self.create_fruits_and_text_we_have()
        self.create_fruits_and_text_for_skins()

    def create_fruits_and_text_we_have(self) -> None:
        for index in range(len(self.fruit_images)):
            fruit = ImageObject(self.game, self.fruit_images[index], (self.game.width // 8 - 9 + index * 25, 60))
            self.objects.append(fruit)
            text = Text(self.game, str(self.game.eaten_fruits[index]), 10)
            text.move_center(self.game.width // 8 - 10 + index * 25, 60)
            self.objects.append(text)

    def create_fruits_and_text_for_skins(self) -> None:
        index_pos_y = self.button_pos_multiply_y
        index_pos_x = 20
        pos_regarding_buttons_x = self.button_pos_x + 45
        pos_regarding_buttons_y = self.button_pos_y - 6
        for index in self.skins:
            multiply_x = 0
            if not self.skins[index][1].is_unlocked:
                for i in self.skins[index][1].skin_cost:
                    fruit = ImageObject(self.game, self.fruit_images[i], (
                        pos_regarding_buttons_x + index_pos_x * multiply_x,
                        pos_regarding_buttons_y + index_pos_y * index))
                    text = Text(self.game, str(self.skins[index][1].skin_cost[i]), 10)
                    text.move_center(pos_regarding_buttons_x + index_pos_x * multiply_x,
                                     pos_regarding_buttons_y + index_pos_y * index)
                    self.objects.append(fruit)
                    self.objects.append(text)
                    multiply_x += 1

    def __create_title(self) -> None:
        title = Text(self.game, 'SELECT SKIN', 25, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        self.static_objects.append(title)

    def create_buttons(self) -> None:
        buttons = []

        self.button_pos_x = self.game.width // 2 - 65
        self.button_pos_y = 90
        self.button_pos_multiply_y = 25
        for i in range(len(self.skins)):
            if self.skins[i][1].is_unlocked:
                buttons.append(self.SkinButton(
                    game=self.game,
                    geometry=pg.Rect(0, 0, 90, 25),
                    text=self.skins[i][0],
                    value=self.skins[i][1],
                    center=(self.button_pos_x, self.button_pos_y + i * self.button_pos_multiply_y),
                    text_size=Font.BUTTON_FOR_SKINS_TEXT_SIZE,
                    active=self.skins[i][1].name in self.game.unlocked_skins))
            else:
                buttons.append(self.BuyButton(
                    game=self.game,
                    geometry=pg.Rect(0, 0, 90, 25),
                    text=self.skins[i][0],
                    value=self.skins[i],
                    center=(self.button_pos_x, self.button_pos_y + i * self.button_pos_multiply_y),
                    text_size=Font.BUTTON_FOR_SKINS_TEXT_SIZE,
                    colors=BUTTON_SKIN_BUY
                ))

        buttons.append(self.SceneButton(
            game=self.game,
            geometry=pg.Rect(0, 0, 180, 40),
            text='MENU',
            scene=self.game.scenes.MENU,
            center=(self.game.width // 2, 250),
            text_size=Font.BUTTON_TEXT_SIZE))

        self.__button_controller = ButtonController(self.game, buttons)
        self.objects.append(self.__button_controller)
        self.update_button_text()

    def update_button_text(self):
        buttons = self.__button_controller.buttons
        for index in range(len(buttons)):
            if hasattr(buttons[index], "value") and hasattr(buttons[index].value, "name"):
                if self.game.skins.current.name == buttons[index].value.name:
                    if not (buttons[index].text.startswith("-") or buttons[index].text.endswith("-")):
                        buttons[index].text = '-' + buttons[index].text + '-'
                else:
                    buttons[index].text = buttons[index].text.strip('-')
