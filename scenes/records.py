import pygame as pg
import scenes
from misc.constants import Color, Font
from misc.path import get_image_path
from misc.sprite_sheet import SpriteSheet
from objects import ImageObject, Text
from objects.buttons import Button


class RecordsScene(scenes.BaseScene):
    medals = SpriteSheet(sprite_path=get_image_path('medal.png'), sprite_size=(16, 16))[0]

    def start_logic(self):
        self.__create_medals()
        self.__create_error_label()

    def create_objects(self) -> None:
        super().create_objects()
        self.__create_text_labels()

    def button_init(self) -> None:
        yield Button(
            game=self.game,
            rect=pg.Rect(0, 0, 180, 40),
            text='MENU',
            function=self._scene_manager.pop,
            center=(self.game.width // 2, 250),
            text_size=Font.BUTTON_TEXT_SIZE)

    def create_title(self) -> None:
        title = Text('RECORDS', 32, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        self.objects.append(title)

    def __create_error_label(self) -> None:
        self.__error_text = Text('NO RECORDS', 24, color=Color.RED)
        self.__error_text.move_center(self.game.width // 2, 100)

    def __create_text_labels(self) -> None:
        def creator():
            text_colors = [Color.GOLD, Color.SILVER, Color.BRONZE, Color.WHITE, Color.WHITE]
            for i, text_color in enumerate(text_colors):
                if self.game.records.data[i] <= 0:
                    break
                yield Text(str(self.game.records.data[i]), 30, pg.Rect(60, 55 + 35 * i, 0, 0), text_color)

        self.game.records.update_records()
        self.medals_text = list(creator())

    def __create_medals(self) -> None:
        def creator():
            for i in range(len(self.medals)):
                image = ImageObject(self.medals[i], (16, 55 + 35 * i))
                image.scale(35, 35)
                yield image
        self.__medals = list(creator())

    def additional_draw(self, screen: pg.Surface) -> None:
        if not self.medals_text:
            self.__error_text.process_draw(screen)
        else:
            for i in range(len(self.medals_text)):
                self.medals_text[i].process_draw(screen)
                self.__medals[i].process_draw(screen)
