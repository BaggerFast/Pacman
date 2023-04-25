import pygame as pg
from pygame.event import Event

from pacman.data_core import Config
from pacman.misc import Font
from pacman.misc.serializers import LevelStorage, MainStorage
from pacman.misc.util import is_esc_pressed
from pacman.objects import ButtonController, Button, Text
from pacman.scene_manager import SceneManager
from pacman.scenes.base_scene import BaseScene


class GameWinScene(BaseScene):
    def __init__(self, game, score):
        super().__init__(game)
        self.score = score

    def _create_objects(self) -> None:
        super()._create_objects()
        MainStorage().add_record(self.game.score)
        self.__unlock_level()

        self.objects += [
            Text("YOU", 40, font=Font.TITLE).move_center(Config.RESOLUTION.half_width, 30),
            Text("WON", 40, font=Font.TITLE).move_center(Config.RESOLUTION.half_width, 70),
            Text(f"Score: {self.score}", 20).move_center(Config.RESOLUTION.half_width, 135),
            Text(f"High score: {MainStorage().get_highscore()}", 20).move_center(Config.RESOLUTION.half_width, 165),
        ]

    def create_buttons(self) -> None:
        from pacman.scenes.menu import MenuScene

        buttons = []
        if not self.__is_last_level():
            buttons.append(
                Button(
                    game=self.game,
                    rect=pg.Rect(0, 0, 180, 35),
                    function=self.__next_level,
                    text="NEXT LEVEL",
                    text_size=Font.BUTTON_TEXT_SIZE,
                ).move_center(Config.RESOLUTION.half_width, 210)
            )
        else:
            buttons.append(
                Button(
                    game=self.game,
                    rect=pg.Rect(0, 0, 180, 35),
                    text="EXIT",
                    function=lambda: SceneManager().reset(MenuScene(self.game)),
                    text_size=Font.BUTTON_TEXT_SIZE,
                ).move_center(Config.RESOLUTION.half_width, 210)
            )
        buttons.append(
            Button(
                game=self.game,
                rect=pg.Rect(0, 0, 180, 35),
                text="MENU",
                function=lambda: SceneManager().reset(MenuScene(self.game)),
                text_size=Font.BUTTON_TEXT_SIZE,
            ).move_center(Config.RESOLUTION.half_width, 250)
        )
        self.objects.append(ButtonController(buttons))

    def __unlock_level(self):
        if not self.__is_last_level():
            LevelStorage().unlock_level(LevelStorage().current + 1)

    def __next_level(self):
        from pacman.scenes.main import MainScene

        LevelStorage().current += 1
        SceneManager().reset(MainScene(self.game))

    def __is_last_level(self) -> bool:
        return (LevelStorage().current + 1) == self.game.maps.count

    def process_event(self, event: Event) -> None:
        super().process_event(event)
        if is_esc_pressed(event):
            from pacman.scenes.menu import MenuScene
            SceneManager().reset(MenuScene(self.game))

    def on_enter(self) -> None:
        self.game.sounds.gameover.play()

    def on_exit(self) -> None:
        self.game.sounds.gameover.stop()
