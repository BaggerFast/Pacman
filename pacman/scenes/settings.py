import pygame as pg

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
            self.value += 1
            if self.value > 2:
                self.value = 0
            self.update_text()
            self.select()
            SettingsStorage().difficulty = self.value

        def update_text(self):
            self.text = self.__dificulties[self.value]

    class SelectButton(Button):
        def __init__(self, **args):
            self.value = args.pop("value")
            super().__init__(**args)

        def click(self) -> None:
            SettingsStorage().set_volume(SettingsStorage().volume + self.value)
            self.game.sounds.click.play()
            self.game.scenes.current.volume_value.text = f"{SettingsStorage().volume}%"
            for sound in self.game.sounds.__dict__.keys():
                self.game.sounds.__dict__[sound].update()

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
            self.move_center(game.width // 2, 75 + i * 40)
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

    def create_static_objects(self):
        self.volume_text = Text("VOLUME", 20)
        self.volume_text.move_center(self.game.width // 2, self.__volume_position)
        self.static_objects.append(self.volume_text)

        self.volume_value = Text(f"{SettingsStorage().volume}%", 20)
        self.volume_value.move_center(
            self.game.width // 2,
            self.__volume_position + 30,
        )
        self.static_objects.append(self.volume_value)
        self.create_title()

    def create_title(self) -> None:
        text = ["SETTINGS"]
        for i in range(len(text)):
            text[i] = Text(text[i], 30, font=Font.TITLE)
            text[i].move_center(self.game.width // 2, 30 + i * 40)
            self.static_objects.append(text[i])

    def create_buttons(self) -> None:
        names = [
            ("SOUND", "mute"),
            ("FUN", "fun"),
        ]
        self.buttons = []
        for i in range(len(names)):
            self.buttons.append(self.SettingButton(self.game, names[i][0], i, names[i][1]))
        self.buttons.append(
            self.SelectButton(
                game=self.game,
                rect=pg.Rect(0, 0, 40, 35),
                text="-",
                value=-5,
            ).move_center(self.game.width // 2 - 60, self.__volume_position + 30)
        )
        self.buttons.append(
            self.SelectButton(
                game=self.game,
                rect=pg.Rect(0, 0, 40, 35),
                text="+",
                value=5,
            ).move_center(self.game.width // 2 + 65, self.__volume_position + 30)
        )
        if self.prev_scene == self.game.scenes.MENU:
            self.buttons.append(
                self.DifficultyButton(
                    game=self.game,
                    rect=pg.Rect(0, 0, 120, 35),
                    text_size=Font.BUTTON_TEXT_SIZE,
                ).move_center(self.game.width // 2, self.__difficulty_pos)
            )
        self.buttons.append(
            self.SceneButton(
                game=self.game,
                rect=pg.Rect(0, 0, 180, 40),
                text="BACK",
                scene=(self.prev_scene, False),
                text_size=Font.BUTTON_TEXT_SIZE,
            ).move_center(self.game.width // 2, 250)
        )

        self.objects.append(ButtonController(self.buttons))

    def additional_event_check(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.game.scenes.set(self.prev_scene)
