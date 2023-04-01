import pygame as pg

from pacman.data_core import Config
from pacman.misc.serializers import MainStorage
from pacman.objects import ButtonController, Text, Button
from pacman.scenes import base
from pacman.misc import Font


class GameOverScene(base.Scene):
    def create_objects(self) -> None:
        super().create_objects()
        self.__create_score_text()
        self.__create_highscore_text()

    def create_title(self) -> None:
        text = ["GAME", "OVER"]
        for i in range(2):
            text[i] = Text(text[i], 40, font=Font.TITLE)
            text[i].move_center(Config.RESOLUTION.half_width, 30 + i * 40)
            self.static_objects.append(text[i])

    def create_buttons(self) -> None:
        names = {
            0: ("RESTART", self.game.scenes.MAIN, True),
            1: ("MENU", self.game.scenes.MENU, False),
        }
        buttons = []
        for i in range(len(names)):
            buttons.append(
                Button(
                    game=self.game,
                    rect=pg.Rect(0, 0, 180, 35),
                    text=names[i][0],
                    function=lambda: self.click_btn(names[i][1], names[i][2]),
                    text_size=Font.BUTTON_TEXT_SIZE,
                ).move_center(Config.RESOLUTION.half_width, 210 + 40 * i)
            )
        self.objects.append(ButtonController(buttons))

    def __create_score_text(self) -> None:
        self.__text_score = Text(f"Score: {self.game.score}", 20)
        self.__text_score.move_center(Config.RESOLUTION.half_width, 135)
        self.objects.append(self.__text_score)

    def __create_highscore_text(self) -> None:
        self.__text_highscore = Text(f"High score: {MainStorage().get_highscore()}", 20)
        self.__text_highscore.move_center(Config.RESOLUTION.half_width, 165)
        self.objects.append(self.__text_highscore)

    def on_deactivate(self) -> None:
        self.game.sounds.gameover.stop()

    def on_activate(self) -> None:
        super().on_activate()
        self.game.sounds.pacman.stop()
        self.game.sounds.gameover.play()
