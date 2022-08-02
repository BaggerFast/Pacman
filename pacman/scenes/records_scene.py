import pygame as pg

from itertools import zip_longest
from misc.animator.sprite_sheet import SpriteSheet
from misc.constants import Color, Font
from misc.storage import LevelStorage
from pacman.buttons import Button, ButtonManager
from pacman.objects import ImageObject, Text
from pacman.scenes.base_scene import BaseScene
from pacman.scenes.manager import SceneManager
from pacman.scenes.util import Medal


# todo finish refactor


class RecordsScene(BaseScene):

    def _setup_logic(self) -> None:
        self.__medals = self.__get_medals()

    def _create_objects(self) -> None:
        back_button = Button(
            geometry=pg.Rect(0, 0, 180, 40),
            text='MENU',
            function=SceneManager().pop,
            center=(self.game.width // 2, 250)
        )
        yield ButtonManager([back_button])
        yield Text('RECORDS', 32, font=Font.TITLE).move_center(self.game.width // 2, 30)

    def __get_medals(self) -> list[Medal]:
        text_colors = [Color.GOLD, Color.SILVER, Color.BRONZE, Color.WHITE]
        medals_sprite = SpriteSheet(sprite_path='medal.png', sprite_size=(16, 16))[0]
        high_scores = LevelStorage().get_current_records()

        medals = []
        if not len(high_scores):
            return medals

        data = zip_longest(medals_sprite, text_colors, high_scores, fillvalue='')
        for i, (medal, text_color, score) in enumerate(data):
            if not score:
                return medals
            image = ImageObject(medal, (16, 55 + 35 * i)).scale(35, 35)
            text = Text(f'{score}', 30, pg.Rect(60, 55 + 35 * i, 0, 0), text_color)

            medals.append(Medal(image, text))

        return medals

    def render(self, screen: pg.Surface):
        super().render(screen)
        if not self.__medals:
            error_text = Text('NO RECORDS', 24, color=Color.RED).move_center(self.game.width // 2, 100)
            error_text.render()
            return
        for medal in self.__medals:
            medal.render(screen)
