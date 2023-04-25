import pygame as pg

from pacman.data_core import Config
from pacman.misc import Font
from pacman.misc.serializers import MainStorage
from pacman.objects import ButtonController, Text, Button
from pacman.scene_manager import SceneManager
from pacman.scenes.base_scene import BaseScene


class GameOverScene(BaseScene):
    def __init__(self, game, score):
        super().__init__(game)
        self.score = score

    def _create_objects(self) -> None:
        super()._create_objects()
        self.objects += [
            Text("GAME", 40, font=Font.TITLE).move_center(Config.RESOLUTION.half_width, 30),
            Text("OVER", 40, font=Font.TITLE).move_center(Config.RESOLUTION.half_width, 70),
            Text(f"Score: {self.score}", 20).move_center(Config.RESOLUTION.half_width, 135),
            Text(f"High score: {MainStorage().get_highscore()}", 20).move_center(Config.RESOLUTION.half_width, 165),
        ]
        self.create_buttons()

    def create_buttons(self) -> None:
        from pacman.scenes.main import MainScene
        from pacman.scenes.menu import MenuScene

        names = [
            ("RESTART", lambda: SceneManager().reset(MainScene(self.game))),
            ("MENU", lambda: SceneManager().reset(MenuScene(self.game))),
        ]
        buttons = []
        for i, (name, fn) in enumerate(names):
            buttons.append(
                Button(
                    game=self.game,
                    rect=pg.Rect(0, 0, 180, 35),
                    text=name,
                    function=fn,
                    text_size=Font.BUTTON_TEXT_SIZE,
                ).move_center(Config.RESOLUTION.half_width, 210 + 40 * i)
            )
        self.objects.append(ButtonController(buttons))

    def on_enter(self) -> None:
        self.game.sounds.gameover.play()

    def on_exit(self) -> None:
        self.game.sounds.gameover.stop()

    # def on_activate(self) -> None:
    #     self.game.sounds.pacman.stop()