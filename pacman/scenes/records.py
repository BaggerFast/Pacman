from typing import NamedTuple

import pygame as pg
from pacman import scenes
from pacman.misc import PathManager
from pacman.misc import SpriteSheet
from pacman.misc.constants import Font, Color
from pacman.objects import ImageObject, Text
from pacman.objects.buttons import Button
from pacman.serializers import LevelSerializer


class Medal(NamedTuple):
    SPRITE: ImageObject
    TEXT: Text

    def process_draw(self, screen):
        self.SPRITE.process_draw(screen)
        self.TEXT.process_draw(screen)


class RecordsScene(scenes.BaseScene):
    medals_sprite = SpriteSheet(sprite_path=PathManager.get_image_path('medal.png'), sprite_size=(16, 16))[0]

    def __init__(self, game):
        super().__init__(game)
        self.__create_medals()

    # region Public

    # region Implementation of BaseScene

    def additional_draw(self, screen: pg.Surface) -> None:
        if not self.__medals:
            error_text = Text('NO RECORDS', 24, color=Color.RED)
            error_text.move_center(self.game.width // 2, 100)
            error_text.process_draw(screen)
            return
        for medal in self.__medals:
            medal.process_draw(screen)

    # endregion

    # endregion

    # region Private

    # region Implementation of BaseScene

    def _button_init(self) -> None:
        yield Button(
            game=self.game,
            rect=pg.Rect(0, 0, 180, 40),
            text='MENU',
            function=self._scene_manager.pop,
            center=(self.game.width // 2, 250),
            text_size=Font.BUTTON_TEXT_SIZE)

    def _create_title(self) -> None:
        title = Text('RECORDS', 32, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        self.objects.append(title)

    # endregion

    def __create_medals(self):
        text_colors = [Color.GOLD, Color.SILVER, Color.BRONZE, Color.WHITE, Color.WHITE]
        self.__medals = []
        high_scores = LevelSerializer().get_current_records()
        for i in range(len(self.medals_sprite)):
            if i > len(high_scores) - 1:
                return

            image = ImageObject(self.medals_sprite[i], (16, 55 + 35 * i))
            image.scale(35, 35)

            text_color = Color.WHITE if i > len(text_colors) + 1 else text_colors[i]
            text = Text(f'{high_scores[i]}', 30, pg.Rect(60, 55 + 35 * i, 0, 0), text_color)
            self.__medals.append(Medal(image, text))

    # endregion
