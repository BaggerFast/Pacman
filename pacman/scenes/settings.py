import pygame as pg
from pygame.event import Event

from pacman.data_core import Cfg
from pacman.misc import Font, BUTTON_GREEN_COLORS, BUTTON_RED_COLORS
from pacman.misc.serializers import SettingsStorage
from pacman.misc.util import is_esc_pressed
from pacman.objects import ButtonController, Text
from pacman.objects.buttons import Button
from pacman.scene_manager import SceneManager
from pacman.scenes.base_scene import BaseScene


class SettingsScene(BaseScene):
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
            self.move_center(Cfg.RESOLUTION.half_width, 75 + i * 40)
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
    __dificulties = {0: "easy", 1: "medium", 2: "hard"}

    def _create_objects(self) -> None:
        self.difficult_button = Button(
            game=self.game,
            rect=pg.Rect(0, 0, 120, 35),
            function=self.click_difficult,
            text_size=Font.BUTTON_TEXT_SIZE,
            text=self.__dificulties[SettingsStorage().difficulty],
        ).move_center(Cfg.RESOLUTION.half_width, self.__difficulty_pos)
        self.create_buttons()
        self.volume_value = Text(f"{SettingsStorage().volume}%", 20).move_center(
            Cfg.RESOLUTION.half_width,
            self.__volume_position + 30,
        )
        self.objects += [
            Text("SETTINGS", 30, font=Font.TITLE).move_center(Cfg.RESOLUTION.half_width, 30),
            Text("VOLUME", 20).move_center(Cfg.RESOLUTION.half_width, self.__volume_position),
            self.volume_value,
        ]

    def click_sound(self, step):
        SettingsStorage().set_volume(SettingsStorage().volume + step)
        self.volume_value.text = f"{SettingsStorage().volume}%"
        for sound in self.game.sounds.__dict__.keys():
            self.game.sounds.__dict__[sound].update()

    def click_difficult(self) -> None:
        SettingsStorage().difficulty = (SettingsStorage().difficulty + 1) % len(self.__dificulties)
        self.difficult_button.text = self.__dificulties[SettingsStorage().difficulty]

    def create_buttons(self) -> None:
        names = [
            ("SOUND", "mute"),
            ("FUN", "fun"),
        ]
        self.buttons = []
        for i in range(len(names)):
            self.buttons.append(self.SettingButton(self.game, names[i][0], i, names[i][1]))
        self.buttons += [
            Button(
                game=self.game,
                rect=pg.Rect(0, 0, 40, 35),
                text="-",
                function=lambda: self.click_sound(-5),
            ).move_center(Cfg.RESOLUTION.half_width - 60, self.__volume_position + 30),
            Button(
                game=self.game,
                rect=pg.Rect(0, 0, 40, 35),
                text="+",
                function=lambda: self.click_sound(5),
            ).move_center(Cfg.RESOLUTION.half_width + 65, self.__volume_position + 30),
            self.difficult_button,
            Button(
                game=self.game,
                rect=pg.Rect(0, 0, 180, 40),
                text="BACK",
                function=SceneManager().pop,
                text_size=Font.BUTTON_TEXT_SIZE,
            ).move_center(Cfg.RESOLUTION.half_width, 250),
        ]
        self.objects.append(ButtonController(self.buttons))

    def process_event(self, event: Event) -> None:
        super().process_event(event)
        if is_esc_pressed(event):
            SceneManager().pop()
