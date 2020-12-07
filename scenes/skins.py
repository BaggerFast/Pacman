from copy import copy

import pygame as pg

from objects import ButtonController, Text, Button, ImageObject
from scenes import base
from misc import Font, get_path, get_list_path


class Scene(base.Scene):
    class SkinButton(Button):
        def __init__(self, **args) -> object:
            self.value = args.pop("value")
            super().__init__(**args)

        def click(self):
            self.game.skins.current = self.value

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

    def process_event(self, event: pg.event.Event) -> None:
        self.is_current = False
        super().process_event(event)

    def create_static_objects(self):
        self.is_current = False
        self.fruit_images = get_list_path('png', 'images', 'fruit')
        self.fruits_for_skins = {
            0: {           #Default
                0: 0,
                1: 0,
            },
            1: {           #Chrome
                3: 3,
                4: 2,
            },
            2: {           #Half-life
                6: 4,
                7: 3,
            }
                }
        self.__create_title()

    def create_objects(self) -> None:
        self.objects = []
        self.preview = copy(self.game.skins.current.image)
        self.objects.append(self.preview)
        self.create_fruits_and_text_we_have()
        self.create_fruits_and_text_for_skins()
        self.create_buttons()

    def create_fruits_and_text_we_have(self):
        for index in range(len(self.fruit_images)):
            fruit = ImageObject(self.game, self.fruit_images[index], (self.game.width // 8 - 9 + index * 25, 60))
            self.objects.append(fruit)
            text = Text(self.game,str(self.game.eaten_fruits[index]),10)
            text.move_center(self.game.width // 8 - 10 + index * 25, 60)
            self.objects.append(text)

    def create_fruits_and_text_for_skins(self):
        index_pos_y = 33
        index_pos_x = 20
        for index in self.fruits_for_skins:
            multiply_x = 0
            for i in self.fruits_for_skins[index]:
                fruit = ImageObject(self.game, self.fruit_images[i], (self.game.width // 2 - 20 + index_pos_x * multiply_x, 109 + index_pos_y * index))
                text = Text(self.game, str(self.fruits_for_skins[index][i]), 10)
                text.move_center(self.game.width // 2 - 20 + index_pos_x * multiply_x, 109 + index_pos_y * index)
                self.objects.append(fruit)
                self.objects.append(text)
                multiply_x +=1

    def __create_title(self) -> None:
        title = Text(self.game, 'SELECT SKIN', 25, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        self.static_objects.append(title)

    def create_buttons(self) -> None:
        buttons = []

        skins = {
            0: ('PACMAN', self.game.skins.default),
            1: ('CHROME', self.game.skins.chrome),
            2: ('HALF-LIFE', self.game.skins.half_life),
        }

        for i in range(len(skins)):
            buttons.append(self.SkinButton(
                game=self.game,
                geometry=pg.Rect(0, 0, 75, 33),
                text=skins[i][0],
                value=skins[i][1],
                center=(self.game.width // 2 - 65, 115 + i * 33),
                text_size=Font.BUTTON_FOR_SKINS_TEXT_SIZE,
                active=skins[i][1].name in self.game.unlocked_skins))

        buttons.append(self.SceneButton(
            game=self.game,
            geometry=pg.Rect(0, 0, 180, 40),
            text='MENU',
            scene=(self.game.scenes.MENU, False),
            center=(self.game.width // 2, 250),
            text_size=Font.BUTTON_TEXT_SIZE))

        self.objects.append(ButtonController(self.game, buttons))
