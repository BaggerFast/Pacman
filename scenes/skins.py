from copy import copy
import pygame as pg
import scenes
from misc.constants import Font, BUTTON_SKIN_BUY
from misc.constants.skin_names import SkinsNames
from misc.path import get_image_path
from misc.sprite_sheet import SpriteSheet
from objects import Text, ImageObject
from objects.buttons import ButtonController, Button, SkinButton, BuyButton


class SkinsScene(scenes.BaseScene):

    def __init__(self, game):
        super().__init__(game)
        self.skins = {
            SkinsNames.default: self.game.skins.default,
            SkinsNames.edge: self.game.skins.edge,
            SkinsNames.pokeball: self.game.skins.pokeball,
            SkinsNames.half_life: self.game.skins.half_life,
            SkinsNames.windows: self.game.skins.windows,
            SkinsNames.chrome: self.game.skins.chrome,
        }
        self.fruit_images: list[str] = SpriteSheet(get_image_path('fruits.png'), (14, 14))[0]

    def _create_objects(self) -> None:
        self.preview = copy(self.game.skins.current.image)
        self.objects.append(self.preview)
        self.create_buttons()
        self.create_fruits_and_text_we_have()
        self.create_fruits_and_text_for_skins()

    def create_fruits_and_text_we_have(self) -> None:
        def creator():
            for i, fruit_img in enumerate(self.fruit_images):
                yield ImageObject(fruit_img, (self.game.width // 8 - 9 + i * 25, 60))
                text = Text(str(self.game.eaten_fruits[i]), 10)
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
                    yield ImageObject(self.fruit_images[i], (
                        pos_regarding_buttons_x + index_pos_x * multiply_x,
                        pos_regarding_buttons_y + index_pos_y * index))
                    text = Text(str(skin.skin_cost[i]), 10)
                    text.move_center(pos_regarding_buttons_x + index_pos_x * multiply_x,
                                     pos_regarding_buttons_y + index_pos_y * index)
                    yield text
                    multiply_x += 1

        index_pos_y = self.button_pos_multiply_y
        index_pos_x = 20
        pos_regarding_buttons_x = self.button_pos_x + 45
        pos_regarding_buttons_y = self.button_pos_y - 6
        self.objects += list(creator())

    def _create_title(self) -> None:
        title = Text('SELECT SKIN', 25, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        self.objects.append(title)

    def _button_init(self):
        for i, (skin_name, skin) in enumerate(self.skins.items()):
            if skin.is_unlocked:
                yield SkinButton(
                    game=self.game,
                    rect=pg.Rect(0, 0, 90, 25),
                    text=skin_name,
                    value=skin,
                    center=(self.button_pos_x, self.button_pos_y + i * self.button_pos_multiply_y),
                    text_size=Font.BUTTON_FOR_SKINS_TEXT_SIZE,
                    active=skin.name in self.game.unlocked_skins
                )
            else:
                yield BuyButton(
                    game=self.game,
                    rect=pg.Rect(0, 0, 90, 25),
                    text=skin_name,
                    value=skin,
                    center=(self.button_pos_x, self.button_pos_y + i * self.button_pos_multiply_y),
                    text_size=Font.BUTTON_FOR_SKINS_TEXT_SIZE,
                    colors=BUTTON_SKIN_BUY
                )
        yield Button(
            game=self.game,
            rect=pg.Rect(0, 0, 180, 40),
            text='MENU',
            function=self._scene_manager.pop,
            center=(self.game.width // 2, 250),
            text_size=Font.BUTTON_TEXT_SIZE)

    def create_buttons(self) -> None:
        self.button_pos_x = self.game.width // 2 - 65
        self.button_pos_y = 90
        self.button_pos_multiply_y = 25
        button_controller = ButtonController(self.game, list(self._button_init()))
        # for button in button_controller.buttons:
        #     if not type(button) in [SkinButton, BuyButton]:
        #         return
        #     if self.game.skins.current.name == buttons[index].value.name:
        #         if not (buttons[index].text.startswith("-") or buttons[index].text.endswith("-")):
        #             buttons[index].text = '-' + buttons[index].text + '-'
        #     else:
        #         buttons[index].text = buttons[index].text.strip('-')
        self.objects.append(button_controller)
