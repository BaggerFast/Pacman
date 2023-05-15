import pygame as pg
from pygame.event import Event
from pacman.data_core import Config
from pacman.events.events import EvenType
from pacman.events.utils import event_append
from pacman.misc import Font
from pacman.misc.util import is_esc_pressed
from pacman.objects import ButtonController, Text, Button
from pacman.scene_manager import SceneManager
from pacman.scenes.blur_scene import BlurScene


class PauseScene(BlurScene):
    def __stop_game(self) -> None:
        from pacman.scenes.menu import MenuScene

        event_append(EvenType.GET_SETTINGS)
        SceneManager().reset(MenuScene(self.game))

    def __restart_game(self) -> None:
        from pacman.scenes.main import MainScene

        event_append(EvenType.GET_SETTINGS)
        SceneManager().reset(MainScene(self.game))

    def _create_objects(self) -> None:
        super()._create_objects()

        from pacman.scenes.settings import SettingsScene

        names = [
            ("CONTINUE", SceneManager().pop),
            ("SETTINGS", lambda: SceneManager().append(SettingsScene(self.game))),
            ("RESTART", self.__restart_game),
            ("MENU", self.__stop_game),
        ]
        buttons = []
        for i, (txt, fn) in enumerate(names):
            buttons.append(
                Button(
                    game=self.game,
                    rect=pg.Rect(0, 0, 180, 40),
                    text=txt,
                    function=fn,
                    text_size=Font.BUTTON_TEXT_SIZE,
                ).move_center(Config.RESOLUTION.half_width, 100 + 45 * i)
            )
        self.objects += [
            ButtonController(buttons),
            Text("PAUSE", 40, font=Font.TITLE).move_center(Config.RESOLUTION.half_width, 35),
        ]

    def process_event(self, event: Event) -> None:
        super().process_event(event)
        if is_esc_pressed(event):
            SceneManager().pop()
