import pygame as pg

from misc.constants import Font
from misc.storage import SettingStorage
from .base import Scene
from ..buttons import SettingButton, ButtonManager, SelectButton, DifficultyButton
from ..objects import Text


class SettingsScene(Scene):
    __volume_position = 150
    __difficulty_pos = 210

    def create_static_objects(self):
        self.volume_text = Text(self.game, "VOLUME", 20)
        self.volume_text.move_center(self.game.width // 2, self.__volume_position)
        self.static_objects.append(self.volume_text)

        self.volume_value = Text(self.game, f'{SettingStorage().volume}%', 20)
        self.volume_value.move_center(self.game.width // 2, self.__volume_position + 30, )
        self.static_objects.append(self.volume_value)
        self.create_title()

    def create_title(self) -> None:
        text = ["SETTINGS"]
        for i in range(len(text)):
            text[i] = Text(self.game, text[i], 30, font=Font.TITLE)
            text[i].move_center(self.game.width // 2, 30 + i * 40)
            self.static_objects.append(text[i])

    def create_buttons(self) -> None:
        names = [
            ("SOUND", "MUTE"),
            ("FUN", "FUN"),
        ]
        self.buttons = []
        for i in range(len(names)):
            self.buttons.append(SettingButton(self.game, names[i][0], i, names[i][1]))
        self.buttons.append(
            SelectButton(
                game=self.game,
                geometry=pg.Rect(0, 0, 40, 35),
                text='-',
                center=(self.game.width // 2 - 60, self.__volume_position + 30),
                value=-5
            )
        )
        self.buttons.append(
            SelectButton(
                game=self.game,
                geometry=pg.Rect(0, 0, 40, 35),
                text='+',
                center=(self.game.width // 2 + 65, self.__volume_position + 30),
                value=5
            )
        )
        if self.prev_scene == self.game.scenes.MENU:
            self.buttons.append(
                DifficultyButton(
                    game=self.game,
                    geometry=pg.Rect(0, 0, 120, 35),
                    center=(self.game.width // 2, self.__difficulty_pos),
                    text_size=Font.BUTTON_TEXT_SIZE
                )
            )
        self.buttons.append(
            self.SceneButton(
                game=self.game,
                geometry=pg.Rect(0, 0, 180, 40),
                text='BACK',
                scene=(self.prev_scene, False),
                center=(self.game.width // 2, 250),
                text_size=Font.BUTTON_TEXT_SIZE
            )
        )

        self.objects.append(ButtonManager(self.game, self.buttons))

    def additional_event_check(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.game.scenes.set(self.prev_scene)
