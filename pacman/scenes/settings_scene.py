import pygame as pg

from misc.constants import Font
from misc.storage import SettingStorage
from .base_scene import Scene, BaseScene
from .manager import SceneManager
from ..buttons import ColorButton, ButtonManager, DifficultyButton, Button
from ..objects import Text


# todo finish refactor

class SettingsScene(BaseScene):
    __difficulty_pos = 210

    def _setup_logic(self) -> None:
        self.__volume_position = 150
        self._volume_indicator = Text(self.game, f'{SettingStorage().volume}%', 20).move_center(self.game.width // 2,
                                                                                                self.__volume_position + 30)

    def _create_objects(self) -> None:
        yield Text(self.game, 'SETTINGS', 30, font=Font.TITLE).move_center(self.game.width // 2, 30)
        yield Text(self.game, "VOLUME", 20).move_center(self.game.width // 2, self.__volume_position)
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

        buttons = []

        buttons.extend(
            [
                ColorButton(
                    game=self.game,
                    geometry=pg.Rect(0, 0, 180, 40),
                    text='SOUND',
                    status=SettingStorage().sound,
                    function=SettingStorage().swap_sound,
                    center=(self.game.width // 2, 75),
                ),
                ColorButton(
                    game=self.game,
                    geometry=pg.Rect(0, 0, 180, 40),
                    text='FUN MODE',
                    status=SettingStorage().fun,
                    function=SettingStorage().swap_fun,
                    center=(self.game.width // 2, 117),
                ),
                Button(
                    game=self.game,
                    geometry=pg.Rect(0, 0, 40, 35),
                    text='-',
                    function=down_volume,
                    center=(self.game.width // 2 - 60, self.__volume_position + 30),
                ),
                Button(
                    game=self.game,
                    geometry=pg.Rect(0, 0, 40, 35),
                    text='+',
                    function=up_volume,
                    center=(self.game.width // 2 + 65, self.__volume_position + 30),
                ),
                Button(
                    game=self.game,
                    geometry=pg.Rect(0, 0, 180, 40),
                    text='MENU',
                    function=SceneManager().pop,
                    center=(self.game.width // 2, 250)
                ),
            ]
        )

        return ButtonManager(self.game, buttons)
    # def additional_event_check(self, event: pg.event.Event) -> None:
    #     if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
    #         self.game.scenes.set(self.prev_scene)
