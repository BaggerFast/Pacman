import pygame as pg

from misc.constants import Font
from misc.storage import SettingStorage
from .base_scene import BaseScene
from .manager import SceneManager
from ..buttons import ColorButton, ButtonManager, Button
from ..objects import Text


# todo finish refactor

class SettingsScene(BaseScene):

    def _setup_logic(self) -> None:
        self.__volume_position = 150
        self._volume_indicator = Text(f'{SettingStorage().volume}%', 20).move_center(self.game.width // 2,
                                                                                     self.__volume_position + 30)

    def _create_objects(self) -> None:
        yield Text('SETTINGS', 30, font=Font.TITLE).move_center(self.game.width // 2, 30)
        yield Text("VOLUME", 20).move_center(self.game.width // 2, self.__volume_position)
        yield self._volume_indicator
        yield self.__get_btn_manager()

    def update(self):
        self._volume_indicator.text = f'{SettingStorage().volume}%'
        super().update()

    def __get_btn_manager(self):
        def up_volume():
            SettingStorage().volume += 5

        def down_volume():
            SettingStorage().volume -= 5

        buttons = [
            ColorButton(
                geometry=pg.Rect(0, 0, 180, 40),
                text='SOUND',
                status=SettingStorage().sound,
                function=SettingStorage().swap_sound,
                center=(self.game.width // 2, 75),
            ),
            ColorButton(
                geometry=pg.Rect(0, 0, 180, 40),
                text='FUN MODE',
                status=SettingStorage().fun,
                function=SettingStorage().swap_fun,
                center=(self.game.width // 2, 117),
            ),
            Button(
                geometry=pg.Rect(0, 0, 40, 35),
                text='-',
                function=down_volume,
                center=(self.game.width // 2 - 60, self.__volume_position + 30),
            ),
            Button(
                geometry=pg.Rect(0, 0, 40, 35),
                text='+',
                function=up_volume,
                center=(self.game.width // 2 + 65, self.__volume_position + 30),
            ),
            Button(
                geometry=pg.Rect(0, 0, 180, 40),
                text='MENU',
                function=SceneManager().pop,
                center=(self.game.width // 2, 250)
            ),
        ]

        return ButtonManager(buttons)
    # def additional_event_check(self, event: pg.event.Event) -> None:
    #     if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
    #         self.game.scenes.set(self.prev_scene)
