import pygame as pg

from pacman.data_core import Colors, PathManager
from pacman.misc import Font
from pacman.objects import ButtonController, ImageObject, Text
from pacman.scenes import base


class RecordsScene(base.Scene):
    def create_static_objects(self):
        self.__create_medals()
        self.__create_title()
        self.__create_error_label()

    def create_objects(self) -> None:
        super().create_objects()
        self.__create_text_labels()

    def create_buttons(self) -> None:
        back_button = self.SceneButton(
            game=self.game,
            geometry=pg.Rect(0, 0, 180, 40),
            text="MENU",
            scene=(self.game.scenes.MENU, False),
            center=(self.game.width // 2, 250),
            text_size=Font.BUTTON_TEXT_SIZE,
        )
        self.objects.append(ButtonController([back_button]))

    def __create_title(self) -> None:
        title = Text("RECORDS", 32, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        self.static_objects.append(title)

    def __create_error_label(self) -> None:
        self.__error_text = Text("NO RECORDS", 24, color=Colors.RED)
        self.__error_text.move_center(self.game.width // 2, 100)

    def __create_text_labels(self) -> None:
        self.game.records.update_records()
        self.medals_text = []
        text_colors = [Colors.GOLD, Colors.SILVER, Colors.BRONZE, Colors.WHITE, Colors.WHITE]
        y = 4
        for i in range(5):
            self.medals_text.append(
                Text(
                    str(self.game.records.data[y]),
                    30,
                    pg.Rect(60, 55 + 35 * i, 0, 0),
                    text_colors[i],
                )
            )
            y -= 1

    def __create_medals(self) -> None:
        self.__medals = []
        for i in range(5):
            self.__medals.append(
                ImageObject(
                    self.game,
                    PathManager.get_image_path(f"medal/{i}"),
                    (16, 55 + 35 * i),
                )
            )
            self.__medals[i].scale(35, 35)

    def additional_draw(self, screen: pg.Surface) -> None:
        super().additional_draw(screen)
        if self.game.records.data[4] == 0:
            self.__error_text.process_draw(screen)
        y = 4
        for i in range(5):
            if self.game.records.data[y] != 0:
                self.medals_text[i].process_draw(screen)
                self.__medals[i].process_draw(screen)
            y -= 1

    def additional_event_check(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.game.scenes.set(self.game.scenes.MENU)
