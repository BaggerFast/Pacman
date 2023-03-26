import pygame as pg
from pacman.objects import ButtonController, Text
from pacman.scenes import base
from pacman.misc import Font


class GameOverScene(base.Scene):
    def create_objects(self) -> None:
        super().create_objects()
        self.__save_record()
        self.__create_score_text()
        self.__create_highscore_text()

    def create_title(self) -> None:
        text = ["GAME", "OVER"]
        for i in range(2):
            text[i] = Text(text[i], 40, font=Font.TITLE)
            text[i].move_center(self.game.width // 2, 30 + i * 40)
            self.static_objects.append(text[i])

    def create_buttons(self) -> None:
        names = {
            0: ("RESTART", self.game.scenes.MAIN, True),
            1: ("MENU", self.game.scenes.MENU, False),
        }
        buttons = []
        for i in range(len(names)):
            buttons.append(
                self.SceneButton(
                    game=self.game,
                    rect=pg.Rect(0, 0, 180, 35),
                    text=names[i][0],
                    scene=(names[i][1], names[i][2]),
                    text_size=Font.BUTTON_TEXT_SIZE,
                ).move_center(self.game.width // 2, 210 + 40 * i)
            )
        self.objects.append(ButtonController(buttons))

    def __create_score_text(self) -> None:
        self.__text_score = Text(f"Score: {self.game.score}", 20)
        self.__text_score.move_center(self.game.width // 2, 135)
        self.objects.append(self.__text_score)

    def __create_highscore_text(self) -> None:
        self.__text_highscore = Text(f"High score: {self.game.records.data[-1]}", 20)
        self.__text_highscore.move_center(self.game.width // 2, 165)
        self.objects.append(self.__text_highscore)

    def __save_record(self) -> None:
        self.game.records.add_new_record(int(self.game.score))

    def on_deactivate(self) -> None:
        self.game.sounds.gameover.stop()

    def on_activate(self) -> None:
        super().on_activate()
        self.game.sounds.pacman.stop()
        self.game.sounds.gameover.play()
