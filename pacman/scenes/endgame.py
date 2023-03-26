import pygame as pg

from pacman.misc.serializers import LevelStorage
from pacman.objects import ButtonController, Button, Text
from pacman.scenes import base
from pacman.misc import Font


class EndGameScene(base.Scene):
    def create_objects(self) -> None:
        super().create_objects()
        self.__save_record()
        self.__create_score_text()
        self.__create_highscore_text()
        self.__unlock_level()

    def create_title(self) -> None:
        text = ["YOU", "WON"]
        for i in range(len(text)):
            text[i] = Text(text[i], 40, font=Font.TITLE)
            text[i].move_center(self.game.width // 2, 30 + i * 40)
            self.static_objects.append(text[i])

    def create_buttons(self) -> None:
        buttons = [
            (
                Button(
                    game=self.game,
                    rect=pg.Rect(0, 0, 180, 35),
                    function=self.__next_level,
                    text="NEXT LEVEL",
                    text_size=Font.BUTTON_TEXT_SIZE,
                ).move_center(self.game.width // 2, 210)
                if self.__is_last_level()
                else self.SceneButton(
                    game=self.game,
                    rect=pg.Rect(0, 0, 180, 35),
                    text="EXIT",
                    scene=(self.game.scenes.MENU, False),
                    text_size=Font.BUTTON_TEXT_SIZE,
                ).move_center(self.game.width // 2, 210)
            ),
            self.SceneButton(
                game=self.game,
                rect=pg.Rect(0, 0, 180, 35),
                text="MENU",
                scene=(self.game.scenes.MENU, False),
                text_size=Font.BUTTON_TEXT_SIZE,
            ).move_center(self.game.width // 2, 250),
        ]
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

    def __unlock_level(self):
        if self.__is_last_level():
            next_level = LevelStorage().current
            LevelStorage().unlock_level(next_level)

    def __next_level(self):
        next_level = LevelStorage().current + 1
        LevelStorage().current = next_level
        self.game.records.update_records()
        self.game.scenes.set(self.game.scenes.MAIN, reset=True)

    def __is_last_level(self) -> bool:
        return (LevelStorage().current + 1) < self.game.maps.count

    def on_activate(self) -> None:
        super().on_activate()
        self.game.sounds.siren.stop()
        self.game.sounds.gameover.play()

    def on_deactivate(self) -> None:
        self.game.sounds.gameover.stop()
