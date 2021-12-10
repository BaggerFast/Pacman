import pygame as pg
from misc import Font, BUTTON_GREEN_COLORS, BUTTON_RED_COLORS
from objects import Text
from objects.button import SettingButton, SelectButton, DifficultyButton, Button
from scenes.base import BaseScene


class SettingsScene(BaseScene):

    __volume_position = 150
    __difficulty_pos = 210

    def create_static_objects(self) -> None:

        volume_text = Text(self.game, "VOLUME", 20)
        volume_text.move_center(self.game.width // 2, self.__volume_position)

        self.volume_value = Text(self.game, f"{self.game.settings.VOLUME} %", 20)
        self.volume_value.move_center(self.game.width // 2, self.__volume_position + 30, )

        self.static_objects += [volume_text, self.volume_value, self.create_title()]

    def create_title(self) -> Text:
        text = Text(self.game, "SETTINGS", 30, font=Font.TITLE)
        text.move_center(self.game.width // 2, 30)
        return text

    def button_init(self) -> None:
        yield SettingButton(
            game=self.game,
            rect=pg.Rect(0, 0, 180, 35),
            text=f"SOUND {'ON' if self.game.settings.SOUND else 'OFF'}",
            center=(self.game.width // 2, 75),
            text_size=Font.BUTTON_TEXT_SIZE,
            colors=BUTTON_GREEN_COLORS if self.game.settings.SOUND else BUTTON_RED_COLORS,
            var="SOUND",
            name="SOUND")

        yield SettingButton(
            game=self.game,
            rect=pg.Rect(0, 0, 180, 35),
            text=f"FUN {'ON' if self.game.settings.FUN else 'OFF'}",
            center=(self.game.width // 2, 75 + 40),
            text_size=Font.BUTTON_TEXT_SIZE,
            colors=BUTTON_GREEN_COLORS if self.game.settings.FUN else BUTTON_RED_COLORS,
            var="FUN",
            name="FUN",
            active=self.prev_scene == self.game.scenes.MENU
        )

        yield SelectButton(
            game=self.game,
            rect=pg.Rect(0, 0, 40, 35),
            text='-',
            center=(self.game.width // 2 - 60, self.__volume_position + 30),
            value=-5
        )
        yield SelectButton(
            game=self.game,
            rect=pg.Rect(0, 0, 40, 35),
            text='+',
            center=(self.game.width // 2 + 65, self.__volume_position + 30),
            value=5,
        )

        yield DifficultyButton(
            game=self.game,
            rect=pg.Rect(0, 0, 120, 35),
            center=(self.game.width // 2, self.__difficulty_pos),
            text_size=Font.BUTTON_TEXT_SIZE,
            active=self.prev_scene == self.game.scenes.MENU,
            text=''
        )

        yield Button(
            game=self.game,
            rect=pg.Rect(0, 0, 180, 40),
            text='BACK',
            function=self.prev_scene,
            center=(self.game.width // 2, 250),
            text_size=Font.BUTTON_TEXT_SIZE
        )

    def additional_event_check(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.prev_scene()

    def __call__(self, *args, **kwargs):
        self.game.scenes.set(self, reset=True)
