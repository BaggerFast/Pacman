from copy import copy
import pygame as pg

from misc.constants import Font
from pacman.objects import Text
from .base_scene import Scene, BaseScene
from .manager import SceneManager
from ..buttons import ButtonManager, Button


class LevelScene(BaseScene):

    def _create_objects(self) -> None:
        yield Text('SELECT LEVEL', 25, font=Font.TITLE).move_center(self.game.width // 2, 30)
        yield self.__get_btn_manager()

    def __get_btn_manager(self):
        buttons = []

        buttons.append(
            Button(
                geometry=pg.Rect(0, 0, 180, 40),
                text='MENU',
                function=SceneManager().pop,
                center=(self.game.width // 2, 250)
            )
        )

        return ButtonManager(buttons)
