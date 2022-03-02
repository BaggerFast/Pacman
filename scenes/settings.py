import pygame as pg
import scenes
from misc.constants import BUTTON_GREEN_COLORS, BUTTON_RED_COLORS, Font
from objects import Text
from objects.buttons import SettingButton, SelectButton, DifficultyButton, Button


class SettingsScene(scenes.BaseScene):

    __volume_position = 150
    __difficulty_pos = 210

    # region Realization of methods
    def _create_objects(self) -> None:
        super()._create_objects()
        volume_text = Text("VOLUME", 20)
        volume_text.move_center(self.game.width // 2, self.__volume_position)

        volume_value = Text(f"{self.game.settings.VOLUME} %", 20)
        volume_value.move_center(self.game.width // 2, self.__volume_position + 30, )

        self.objects += [volume_text, volume_value, self.title]

    @property
    def title(self) -> Text:
        text = Text("SETTINGS", 30, font=Font.TITLE)
        text.move_center(self.game.width // 2, 30)
        return text

    def _button_init(self) -> None:
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
            active=True
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
            active=True,
            text=''
        )

        yield Button(
            game=self.game,
            rect=pg.Rect(0, 0, 180, 40),
            text='BACK',
            function=self._scene_manager.pop,
            center=(self.game.width // 2, 250),
            text_size=Font.BUTTON_TEXT_SIZE
        )
    # endregion
