import pygame as pg
from pacman import scenes
from pacman.misc.constants import LIGHT_BUTTON_COLORS
from pacman.misc.constants.classes import MenuPreset, Font
from pacman.objects import Text
from pacman.objects.buttons import Button
from pacman.scenes.base import BaseScene


class PauseScene(BaseScene):

    # region Private

    # region Implementation of BaseScene

    def _button_init(self) -> None:
        names = [
            MenuPreset("CONTINUE", self._scene_manager.pop),
            MenuPreset("SETTINGS", lambda: self._scene_manager.append(scenes.SettingsScene(self.game))),
            MenuPreset("RESTART", lambda: self._scene_manager.reset(scenes.MainScene(self.game))),
            MenuPreset("MENU", lambda: self._scene_manager.append(scenes.MenuScene(self.game))),
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

    def _create_title(self) -> None:
        main_text = Text('PAUSE', 40, font=Font.TITLE)
        main_text.move_center(self.game.width // 2, 35)
        self.objects.append(main_text)

    # endregion

    # endregion
