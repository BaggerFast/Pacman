import pygame as pg
from misc.constants import Font
from .base_scene import BaseScene
from .manager import SceneManager
from .util import MenuPreset
from ..buttons import ButtonManager, Button
from ..buttons.util import BTN_TRANSPERENT_COLORS
from ..objects import Text


# todo finish refactor

class PauseScene(BaseScene):

    def _create_objects(self) -> None:
        yield Text('PAUSE', 40, font=Font.TITLE).move_center(self.game.width // 2, 35)
        yield self.__get_btn_manager()

    def __get_btn_manager(self):
        from . import MenuScene, MainScene, SettingsScene
        sc = SceneManager()
        data = [
            MenuPreset("CONTINUE", sc.pop),
            MenuPreset("SETTINGS", lambda: sc.append(SettingsScene(self.game))),
            MenuPreset("RESTART", lambda: sc.reset(MainScene(self.game))),
            MenuPreset("MENU", lambda: sc.reset(MenuScene(self.game))),
        ]
        buttons = [
            Button(
                geometry=pg.Rect(0, 0, 180, 40),
                text=name,
                function=func,
                center=(self.game.width // 2, 100 + 45 * i),
                colors=BTN_TRANSPERENT_COLORS
            )
            for i, (name, func) in enumerate(data)
        ]
        return ButtonManager(buttons)
