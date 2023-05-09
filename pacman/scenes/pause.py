import pygame as pg
from pygame.event import Event
from pacman.data_core import Config
from pacman.misc import Font
from pacman.misc.util import is_esc_pressed
from pacman.objects import ButtonController, Text, Button
from pacman.scene_manager import SceneManager
from pacman.scenes.base_scene import BaseScene


class PauseScene(BaseScene):
    def _create_objects(self) -> None:
        from pacman.scenes.main import MainScene
        from pacman.scenes.menu import MenuScene
        from pacman.scenes.settings import SettingsScene

        names = [
            ("CONTINUE", SceneManager().pop),
            ("SETTINGS", lambda: SceneManager().append(SettingsScene(self.game))),
            ("RESTART", lambda: SceneManager().reset(MainScene(self.game))),
            ("MENU", lambda: SceneManager().append(MenuScene(self.game))),
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
