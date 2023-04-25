import pygame as pg
from pygame import Surface
from pygame.event import Event

from pacman.data_core import Colors, PathManager, Config
from pacman.misc import Font
from pacman.misc.serializers import LevelStorage, MainStorage
from pacman.misc.util import is_esc_pressed
from pacman.objects import ButtonController, ImageObject, Text, Button
from pacman.scene_manager import SceneManager
from pacman.scenes.base_scene import BaseScene


class RecordsScene(BaseScene):
    def _create_objects(self) -> None:
        super()._create_objects()
        self.__indicator = Text(f"level {LevelStorage().current+1}", 12, font=Font.DEFAULT).move_center(
            Config.RESOLUTION.half_width, 55
        )
        self.objects += [
            self.__indicator,
            Text("RECORDS", 32, font=Font.TITLE).move_center(Config.RESOLUTION.half_width, 30),
        ]
        self.__error_text = Text("NO RECORDS", 24, color=Colors.RED).move_center(Config.RESOLUTION.half_width, 100)
        self.__create_text_labels()
        self.__create_medals()
        self.create_buttons()

    def create_buttons(self) -> None:
        back_button = Button(
            game=self.game,
            rect=pg.Rect(0, 0, 180, 40),
            text="MENU",
            function=SceneManager().pop,
            text_size=Font.BUTTON_TEXT_SIZE,
        ).move_center(Config.RESOLUTION.half_width, 250)
        self.objects.append(ButtonController([back_button]))

    def __create_text_labels(self) -> None:
        self.medals_text = []
        text_colors = [Colors.GOLD, Colors.SILVER, Colors.BRONZE, Colors.WHITE, Colors.WHITE]
        y = 4
        for i in range(5):
            text = "." * 12 if not MainStorage().current_highscores()[y] else f"{MainStorage().current_highscores()[y]}"
            text_color = Colors.WHITE if not MainStorage().current_highscores()[y] else text_colors[i]
            self.medals_text.append(
                Text(
                    text,
                    25,
                    pg.Rect(60, 60 + 35 * i, 0, 0),
                    text_color,
                )
            )
            y -= 1

    def __create_medals(self) -> None:
        self.__medals = []
        for i in range(5):
            self.__medals.append(
                ImageObject(
                    PathManager.get_image_path(f"medal/{i}"),
                    (16, 60 + 35 * i),
                ).scale(30, 30)
            )

    def draw(self, screen: Surface) -> None:
        super().draw(screen)
        if not sum(MainStorage().current_highscores()):
            self.__error_text.draw(screen)
            return
        y = 4
        for i in range(5):
            if y != -1:
                self.medals_text[i].draw(screen)
                self.__medals[i].draw(screen)
            y -= 1

    def process_event(self, event: Event) -> None:
        super().process_event(event)
        if is_esc_pressed(event):
            SceneManager().pop()
