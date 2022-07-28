import pygame as pg

from misc.constants import Font, BUTTON_TRANSPERENT_COLORS
from pacman.objects import Text
from .base import Scene
from ..buttons.button import Button
from ..buttons.manager import ButtonManager
from ..buttons.scene_button import SceneButton


class GameWinScene(Scene):
    def create_objects(self) -> None:
        super().create_objects()
        self.__save_record()
        self.__create_score_text()
        self.__create_highscore_text()
        self.__unlock_level()

    def create_title(self) -> None:
        text = ["YOU", "WON"]
        for i in range(len(text)):
            text[i] = Text(self.game, text[i], 40, font=Font.TITLE)
            text[i].move_center(self.game.width // 2, 30 + i * 40)
            self.static_objects.append(text[i])

    def create_buttons(self) -> None:
        buttons = [
            Button(
                self.game, pg.Rect(0, 0, 180, 35),
                self.__next_level, 'NEXT LEVEL',
                center=(self.game.width // 2, 210),
                text_size=Font.BUTTON_TEXT_SIZE,
                colors=BUTTON_TRANSPERENT_COLORS
            )
            if self.__is_last_level() else SceneButton(
                game=self.game,
                geometry=pg.Rect(0, 0, 180, 35),
                text='EXIT',
                scene=(self.game.scenes.MENU, False),
                center=(self.game.width // 2, 210),
                text_size=Font.BUTTON_TEXT_SIZE,
                colors=BUTTON_TRANSPERENT_COLORS
            ),
            SceneButton(
                game=self.game,
                geometry=pg.Rect(0, 0, 180, 35),
                text='MENU',
                scene=(self.game.scenes.MENU, False),
                center=(self.game.width // 2, 250),
                text_size=Font.BUTTON_TEXT_SIZE,
                colors=BUTTON_TRANSPERENT_COLORS
            )
        ]
        self.objects.append(ButtonManager(self.game, buttons))

    def __create_score_text(self) -> None:
        self.__text_score = Text(self.game, f'Score: {self.game.score}', 20)
        self.__text_score.move_center(self.game.width // 2, 135)
        self.objects.append(self.__text_score)

    def __create_highscore_text(self) -> None:
        self.__text_highscore = Text(self.game, f'High score: {self.game.records.data[-1]}', 20)
        self.__text_highscore.move_center(self.game.width // 2, 165)
        self.objects.append(self.__text_highscore)

    def __save_record(self) -> None:
        self.game.records.add_new_record(int(self.game.score))

    def __unlock_level(self):
        if self.__is_last_level():
            next_level = self.game.maps.cur_id + 1
            self.game.unlock_level(next_level)

    def __next_level(self):
        next_level = self.game.maps.cur_id + 1
        self.game.maps.cur_id = next_level
        self.game.records.update_records()
        self.game.scenes.set(self.game.scenes.MAIN, reset=True)

    def __is_last_level(self):
        return (self.game.maps.cur_id + 1) < self.game.maps.count

    def on_activate(self) -> None:
        super().on_activate()
        self.game.sounds.siren.stop()
        self.game.sounds.gameover.play()

    def on_deactivate(self) -> None:
        self.game.sounds.gameover.stop()
