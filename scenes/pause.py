import pygame as pg

from misc.constants.classes import MenuPreset
from objects import Text
from misc import Font, LIGHT_BUTTON_COLORS
from objects.buttons import Button
from scenes.base import BaseScene


class PauseScene(BaseScene):

    def button_init(self) -> None:
        names = [
            MenuPreset("CONTINUE", self.scene_manager.pop),
            MenuPreset("SETTINGS", lambda: self.scene_manager.append(self.scenes.SETTINGS(self.game))),
            MenuPreset("RESTART", lambda: self.scene_manager.reset(self.scenes.MAIN(self.game))),
            MenuPreset("MENU", lambda: self.scene_manager.append(self.scenes.MENU(self.game))),
        ]
        for i, menu_preset in enumerate(names):
            yield Button(
                game=self.game,
                rect=pg.Rect(0, 0, 180, 40),
                text=menu_preset.header,
                function=menu_preset.function,
                center=(self.game.width // 2, 100+45*i),
                text_size=Font.BUTTON_TEXT_SIZE,
                colors=LIGHT_BUTTON_COLORS
            )

    def create_title(self) -> None:
        main_text = Text('PAUSE', 40, font=Font.TITLE)
        main_text.move_center(self.game.width // 2, 35)
        self.objects.append(main_text)
