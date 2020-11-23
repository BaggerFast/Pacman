import pygame as pg
from objects.button import ButtonController, Button
from objects.text import Text
from scenes.base import BaseScene
from misc.constants import Color, Font
from scenes.main import GameScene


class GameoverScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)

    def create_objects(self) -> None:
        self.create_title()
        self.create_buttons()
        self.create_score_text()
        self.create_highscore_text()

    def create_title(self) -> None:
        title_game = Text(self.game, 'GAME', 40, color=Color.WHITE, font=Font.FILENAME)
        title_over = Text(self.game, 'OVER', 40, color=Color.WHITE, font=Font.FILENAME)
        title_game.move_center(self.game.width // 2, 30)
        title_over.move_center(self.game.width // 2, 60 + 20)
        self.objects.append(title_game)
        self.objects.append(title_over)

    def create_buttons(self) -> None:
        buttons = [
            Button(self.game, pg.Rect(0, 0, 110, 30),
                   self.start_menu, 'MENU',
                   center=(self.game.width // 2 + 180 // 3 - 10, self.game.height - 30),
                   text_size=Font.BUTTON_TEXT_SIZE),
            Button(self.game, pg.Rect(0, 0, 110, 30),
                   self.restart_game, 'RESTART',
                   center=(self.game.width // 2 - 180 // 3 + 10, self.game.height - 30),
                   text_size=Font.BUTTON_TEXT_SIZE)
        ]
        self.button_controller = ButtonController(self.game, buttons)
        self.objects.append(self.button_controller)

    def create_score_text(self) -> None:
        text_score = Text(self.game, f'Score: {self.game.score}', 20, color=Color.WHITE, font=Font.FILENAME)
        text_score.move_center(self.game.width // 2, 20 + 60 + 30 + 20)
        self.objects.append(text_score)

    def create_highscore_text(self) -> None:
        # :todo: high score берет не верные данные
        text_highscore = Text(self.game, f'High score: {self.game.score}', 20, color=Color.WHITE, font=Font.FILENAME)
        text_highscore.move_center(self.game.width // 2, 20 + 60 + 30 + 20 + 30)
        self.objects.append(text_highscore)

    def on_activate(self) -> None:
        self.button_controller.reset_state()

    def start_menu(self) -> None:
        self.game.set_scene('SCENE_MENU')

    def restart_game(self) -> None:
        self.game.scenes["SCENE_GAME"] = GameScene(self.game)
        self.game.score.score = 0
        self.game.set_scene('SCENE_GAME')
