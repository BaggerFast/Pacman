import pygame as pg

from pacman.data_core import Config
from pacman.data_core.game_objects import GameObjects
from pacman.misc import Font, BUTTON_GREEN_COLORS, BUTTON_RED_COLORS
from pacman.misc.serializers import SettingsStorage
from pacman.objects import ButtonController, Text
from pacman.objects.button import Button
from pacman.scenes import base


class SettingsScene(base.Scene):
    class DifficultyButton(Button):
        __dificulties = {0: "easy", 1: "medium", 2: "hard"}

        def __init__(self, **args):
            super().__init__(**args)
            self.value = SettingsStorage().difficulty
            self.update_text()

        def click(self) -> None:
            self.game.sounds.click.play()
            self.value = (self.value + 1) % len(self.__dificulties)
            self.update_text()
            self.select()
            SettingsStorage().difficulty = self.value

        def update_text(self):
            self.text = self.__dificulties[self.value]

    class SettingButton(Button):
        def __init__(self, game, name, i, var):
            flag_var = getattr(SettingsStorage(), var)
            super().__init__(
                game=game,
                rect=pg.Rect(0, 0, 180, 35),
                text=name + (" ON" if flag_var else " OFF"),
                text_size=Font.BUTTON_TEXT_SIZE,
                colors=BUTTON_GREEN_COLORS if flag_var else BUTTON_RED_COLORS,
            )
            self.move_center(Config.RESOLUTION.half_width, 75 + i * 40)
            self.name = name
            self.var = var

        def click(self):
            self.game.sounds.click.play()
            flag_var = not getattr(SettingsStorage(), self.var)
            setattr(SettingsStorage(), self.var, flag_var)
            for sound in self.game.sounds.__dict__.keys():
                self.game.sounds.__dict__[sound].update()
            if flag_var:
                self.text = self.name + " ON"
                self.colors = BUTTON_GREEN_COLORS
            else:
                self.text = self.name + " OFF"
                self.colors = BUTTON_RED_COLORS

    __volume_position = 150
    __difficulty_pos = 210

    def create_objects(self) -> None:
        self.objects = GameObjects()
        self.objects.append(Text("SETTINGS", 30, font=Font.TITLE).move_center(Config.RESOLUTION.half_width, 30))
        self.objects.append(Text("VOLUME", 20).move_center(Config.RESOLUTION.half_width, self.__volume_position))
        self.create_buttons()
        self.volume_value = Text(f"{SettingsStorage().volume}%", 20)
        self.volume_value.move_center(
            Config.RESOLUTION.half_width,
            self.__volume_position + 30,
        )
        self.objects.append(self.volume_value)

    def click_sound(self, step):
        SettingsStorage().set_volume(SettingsStorage().volume + step)
        self.game.scenes.current.volume_value.text = f"{SettingsStorage().volume}%"
        for sound in self.game.sounds.__dict__.keys():
            self.game.sounds.__dict__[sound].update()

    def create_buttons(self) -> None:
        names = [
            ("SOUND", "mute"),
            ("FUN", "fun"),
        ]
        self.buttons = []
        for i in range(len(names)):
            self.buttons.append(self.SettingButton(self.game, names[i][0], i, names[i][1]))
        self.buttons.append(
            Button(
                game=self.game,
                rect=pg.Rect(0, 0, 40, 35),
                text="-",
                function=lambda: self.click_sound(-5),
            ).move_center(Config.RESOLUTION.half_width - 60, self.__volume_position + 30)
        )
        self.buttons.append(
            Button(
                game=self.game,
                rect=pg.Rect(0, 0, 40, 35),
                text="+",
                function=lambda: self.click_sound(5),
            ).move_center(Config.RESOLUTION.half_width + 65, self.__volume_position + 30)
        )
        if self.prev_scene == self.game.scenes.MENU:
            self.buttons.append(
                self.DifficultyButton(
                    game=self.game,
                    rect=pg.Rect(0, 0, 120, 35),
                    text_size=Font.BUTTON_TEXT_SIZE,
                ).move_center(Config.RESOLUTION.half_width, self.__difficulty_pos)
            )
        self.buttons.append(
            Button(
                game=self.game,
                rect=pg.Rect(0, 0, 180, 40),
                text="BACK",
                function=lambda: self.click_btn(self.prev_scene, False),
                text_size=Font.BUTTON_TEXT_SIZE,
            ).move_center(Config.RESOLUTION.half_width, 250)
        )

        self.objects.append(ButtonController(self.buttons))

    def additional_event_check(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.game.scenes.set(self.prev_scene)
