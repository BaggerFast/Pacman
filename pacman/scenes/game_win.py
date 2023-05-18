import pygame as pg
from pygame import Surface
from pygame.event import Event
from pacman.data_core import Cfg
from pacman.events.events import EvenType
from pacman.events.utils import event_append
from pacman.misc.constants import Font
from pacman.misc.serializers import LevelStorage
from pacman.misc.util import is_esc_pressed
from pacman.misic import Music
from pacman.objects import Text
from pacman.objects.buttons import Button, ButtonController
from pacman.scene_manager import SceneManager
from pacman.scenes.blur_scene import BlurScene


class GameWinScene(BlurScene):
    def __init__(self, game, blur_surface: Surface, score: int):
        super().__init__(game, blur_surface)
        self.score = score

    def _create_objects(self) -> None:
        super()._create_objects()
        LevelStorage().add_record(self.score)
        LevelStorage().unlock_next_level()
        self.objects += [
            Text("YOU", 40, font=Font.TITLE).move_center(Cfg.RESOLUTION.half_width, 30),
            Text("WON", 40, font=Font.TITLE).move_center(Cfg.RESOLUTION.half_width, 70),
            Text(f"Score: {self.score}", 20).move_center(Cfg.RESOLUTION.half_width, 135),
            Text(f"High score: {LevelStorage().get_highscore()}", 20).move_center(Cfg.RESOLUTION.half_width, 165),
        ]
        self.create_buttons()

    def create_buttons(self) -> None:
        from pacman.scenes.menu import MenuScene

        buttons = []

        if not LevelStorage().is_last_level():
            buttons.append(
                Button(
                    rect=pg.Rect(0, 0, 180, 35),
                    function=self.__next_level,
                    text="NEXT LEVEL",
                    text_size=Font.BUTTON_TEXT_SIZE,
                ).move_center(Cfg.RESOLUTION.half_width, 210)
            )
        else:
            buttons.append(
                Button(
                    rect=pg.Rect(0, 0, 180, 35),
                    text="EXIT",
                    function=lambda: SceneManager().reset(MenuScene(self.game)),
                    text_size=Font.BUTTON_TEXT_SIZE,
                ).move_center(Cfg.RESOLUTION.half_width, 210)
            )
        buttons.append(
            Button(
                rect=pg.Rect(0, 0, 180, 35),
                text="MENU",
                function=lambda: SceneManager().reset(MenuScene(self.game)),
                text_size=Font.BUTTON_TEXT_SIZE,
            ).move_center(Cfg.RESOLUTION.half_width, 250)
        )
        self.objects.append(ButtonController(buttons))

    def __next_level(self):
        from pacman.scenes.main import MainScene

        LevelStorage().set_next_level()
        SceneManager().reset(MainScene(self.game))

    def process_event(self, event: Event) -> None:
        super().process_event(event)
        if is_esc_pressed(event):
            from pacman.scenes.menu import MenuScene

            SceneManager().reset(MenuScene(self.game))

    def on_enter(self) -> None:
        Music().gameover.play()

    def on_exit(self) -> None:
        event_append(EvenType.SET_SETTINGS)
        Music().gameover.stop()
