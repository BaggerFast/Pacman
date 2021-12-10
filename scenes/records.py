import pygame as pg
from misc import Color, Font, get_path
from misc.sprite_sheet import SpriteSheet
from objects import ImageObject, Text
from objects.button import Button
from scenes.base import BaseScene


class RecordsScene(BaseScene):
    medals = SpriteSheet(sprite_path=get_path('images/medal.png'), sprite_size=(16, 16))[0]

    def create_static_objects(self):
        self.__create_medals()
        self.__create_title()
        self.__create_error_label()

    def create_objects(self) -> None:
        super().create_objects()
        self.__create_text_labels()

    def button_init(self) -> None:
        yield Button(
            game=self.game,
            rect=pg.Rect(0, 0, 180, 40),
            text='MENU',
            function=self.game.scenes.MENU,
            center=(self.game.width // 2, 250),
            text_size=Font.BUTTON_TEXT_SIZE)

    def __create_title(self) -> None:
        title = Text(self.game, 'RECORDS', 32, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        self.static_objects.append(title)

    def __create_error_label(self) -> None:
        self.__error_text = Text(self.game, 'NO RECORDS', 24, color=Color.RED)
        self.__error_text.move_center(self.game.width // 2, 100)

    def __create_text_labels(self) -> None:
        def creator():
            text_colors = [Color.GOLD, Color.SILVER, Color.BRONZE, Color.WHITE, Color.WHITE]
            for i, text_color in enumerate(text_colors):
                yield Text(self.game, str(self.game.records.data[i]), 30, pg.Rect(60, 55 + 35 * i, 0, 0), text_color)

        self.game.records.update_records()
        self.medals_text = list(creator())

    def __create_medals(self) -> None:
        def creator():
            for i in range(len(self.medals)):
                image = ImageObject(self.game, self.medals[i], (16, 55 + 35 * i))
                image.scale(35, 35)
                yield image
        self.__medals = list(creator())

    def additional_draw(self) -> None:
        super().additional_draw()
        if sum(self.game.records.data) == 0:
            self.__error_text.process_draw()
        else:
            for i in range(len(self.medals)):
                if self.game.records.data[i]:
                    self.medals_text[i].process_draw()
                    self.__medals[i].process_draw()
