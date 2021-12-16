import pygame as pg
from objects import Text
from misc import Font, BUTTON_DEFAULT_COLORS
from objects.button import Button
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
            self.static_objects.append(text)

    def button_init(self) -> None:
        names = {
            "RESTART": lambda: self.scene_manager.set(self.game.scenes.MAIN(self.game)),
            "MENU": lambda: self.scene_manager.set(self.game.scenes.MENU(self.game)),
        }
        for i, (name, scene) in enumerate(names.items()):
            yield Button(
                game=self.game,
                rect=pg.Rect(0, 0, 180, 35),
                text=name,
                function=scene,
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
