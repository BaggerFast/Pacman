import pygame as pg

from misc.constants.classes import MenuPreset
from objects import Text
from misc import Font, BUTTON_DEFAULT_COLORS
from objects.buttons import Button
from scenes.base import BaseScene


class GameOverScene(BaseScene):
    def __init__(self, game, score):
        super().__init__(game)
        self.score = score

    def create_objects(self) -> None:
        super().create_objects()
        self.objects += [self.__get_score_text, self.__get_highscore_text]

    def create_title(self) -> None:
        for i, text in enumerate(['GAME', 'OVER']):
            text = Text(self.game, text, 40, font=Font.TITLE)
            text.move_center(self.game.width // 2, 30 + i * 40)
            self.objects.append(text)

    def button_init(self) -> None:
        names = {
            MenuPreset("RESTART", lambda: self.scene_manager.reset(self.scenes.MAIN(self.game))),
            MenuPreset("MENU", lambda: self.scene_manager.reset(self.scenes.MENU(self.game))),
        }
        for i, menu_preset in enumerate(names):
            yield Button(
                game=self.game,
                rect=pg.Rect(0, 0, 180, 35),
                text=menu_preset.header,
                function=menu_preset.function,
                center=(self.game.width // 2, 210+40*i),
                text_size=Font.BUTTON_TEXT_SIZE,
                colors=BUTTON_DEFAULT_COLORS
            )

    @property
    def __get_score_text(self) -> Text:
        text_score = Text(self.game, f'Score: {self.score}', 20)
        text_score.move_center(self.game.width // 2, 135)
        return text_score

    @property
    def __get_highscore_text(self) -> Text:
        text_highscore = Text(self.game, f'High score: {self.game.records.data[0]}',  20)
        text_highscore.move_center(self.game.width // 2, 165)
        return text_highscore

    def on_exit(self) -> None:
        self.game.sounds.gameover.stop()

    def on_enter(self) -> None:
        self.game.sounds.pacman.stop()
        self.game.sounds.gameover.play()
