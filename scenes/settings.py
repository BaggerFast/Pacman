import pygame as pg

from misc import Font, BUTTON_GREEN_COLORS, BUTTON_RED_COLORS
from objects import ButtonController, Text
from objects.button import Button
from scenes import base


class Scene(base.Scene):
    class DifficultyButton(Button):

        __dificulties = [
            "easy",
            "medium",
            "hard"
        ]

        def __init__(self, **args):
            super().__init__(**args)
            self.value = self.game.settings.DIFFICULTY
            self.update_text()

        def click(self) -> None:
            self.value += 1
            if self.value > 2:
                self.value = 0
            self.update_text()
            self.select()
            self.game.settings.DIFFICULTY = self.value

        def update_text(self):
            self.text = self.__dificulties[self.value]

    class SelectButton(Button):
        def __init__(self, **args):
            self.value = args.pop("value")
            super().__init__(**args)

        def click(self) -> None:
            self.select()
            self.game.settings.VOLUME += self.value
            self.game.settings.VOLUME = max(self.game.settings.VOLUME, 0)
            self.game.settings.VOLUME = min(self.game.settings.VOLUME, 100)
            self.game.scenes.current.volume_value.text = str(self.game.settings.VOLUME) + "%"
            for sound in self.game.sounds.__dict__.keys():
                self.game.sounds.__dict__[sound].update()

    class SettingButton(Button):
        def __init__(self, **args):
            self.name = args.pop("name")
            self.var = args.pop("var")
            super().__init__(**args)

        def update(self, var):
            if var == "SOUND" or var == "FUN":
                sounds = self.game.sounds.__dict__
                for sound in sounds.keys():
                    sounds[sound].update()

        def click(self):
            self.update(self.var)
            self.select()
            flag_var = not getattr(self.game.settings, self.var)
            setattr(self.game.settings, self.var, flag_var)
            if flag_var:
                self.text = self.name + " ON"
                self.colors = BUTTON_GREEN_COLORS
            else:
                self.text = self.name + " OFF"
                self.colors = BUTTON_RED_COLORS

    __volume_position = 150
    __difficulty_pos = 210

    def create_static_objects(self):
        self.volume_text = Text(self.game, "VOLUME", 20)
        self.volume_text.move_center(self.game.width // 2, self.__volume_position)
        self.static_objects.append(self.volume_text)

        self.volume_value = Text(self.game, str(self.game.settings.VOLUME) + "%", 20)
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

        names = {
            "SOUND": "SOUND",
            "FUN": "FUN"
        }
        self.buttons = []

        self.buttons.append(
            self.SettingButton(
                game=self.game,
                geometry=pg.Rect(0, 0, 180, 35),
                text=names["SOUND"] + (" ON" if self.game.settings.SOUND else " OFF"),
                center=(self.game.width // 2, 75),
                text_size=Font.BUTTON_TEXT_SIZE,
                colors=BUTTON_GREEN_COLORS if self.game.settings.SOUND else BUTTON_RED_COLORS,
                var=names["SOUND"],
                name="SOUND"
            )
        )
        self.buttons.append(
            self.SettingButton(
                game=self.game,
                geometry=pg.Rect(0, 0, 180, 35),
                text=names["FUN"] + (" ON" if self.game.settings.FUN else " OFF"),
                center=(self.game.width // 2, 75 + 40),
                text_size=Font.BUTTON_TEXT_SIZE,
                colors=BUTTON_GREEN_COLORS if self.game.settings.FUN else BUTTON_RED_COLORS,
                var=names["FUN"],
                name="FUN",
                active=self.prev_scene == self.game.scenes.MENU
            )
        )
        self.buttons.append(
            self.SelectButton(
                game=self.game,
                geometry=pg.Rect(0, 0, 40, 35),
                text='-',
                center=(self.game.width // 2 - 60, self.__volume_position + 30),
                value=-5
            )
        )
        self.buttons.append(
            self.SelectButton(
                game=self.game,
                geometry=pg.Rect(0, 0, 40, 35),
                text='+',
                center=(self.game.width // 2 + 65, self.__volume_position + 30),
                value=5
            )
        )
        self.buttons.append(
            self.DifficultyButton(
                game=self.game,
                geometry=pg.Rect(0, 0, 120, 35),
                center=(self.game.width // 2, self.__difficulty_pos),
                text_size=Font.BUTTON_TEXT_SIZE,
                active=self.prev_scene == self.game.scenes.MENU
            )
        )
        self.buttons.append(
            self.SceneButton(
                game=self.game,
                geometry=pg.Rect(0, 0, 180, 40),
                text='BACK',
                scene=self.prev_scene,
                center=(self.game.width // 2, 250),
                text_size=Font.BUTTON_TEXT_SIZE
            )
        )

        self.objects.append(ButtonController(self.game, self.buttons))

    def additional_event_check(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.game.scenes.set(self.prev_scene)

    def __call__(self, *args, **kwargs):
        self.game.scenes.set(self,True)
