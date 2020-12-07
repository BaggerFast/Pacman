import pygame as pg

from misc import Font, BUTTON_GREEN_COLORS, BUTTON_RED_COLORS
from objects import ButtonController, Text
from objects.button import Button
from scenes import base


class Scene(base.Scene):
    class SettingButton(Button):
        def __init__(self, game, name, i, var):
            flag_var = getattr(game.settings, var)
            super().__init__(
                game=game,
                geometry=pg.Rect(0, 0, 180, 35),
                text=name + (" ON" if flag_var else " OFF"),
                center=(game.width // 2, 95 + i * 40),
                text_size=Font.BUTTON_TEXT_SIZE,
                colors=BUTTON_GREEN_COLORS if flag_var else BUTTON_RED_COLORS,
            )
            self.name = name
            self.var = var

        def update(self, var):
            if var == "VOLUME":
                sounds = self.game.sounds.__dict__
                for sound in sounds.keys():
                    sounds[sound].update()

        def click(self):
            flag_var = not getattr(self.game.settings, self.var)
            setattr(self.game.settings, self.var, flag_var)
            if flag_var:
                self.text = self.name + " ON"
                self.colors = BUTTON_GREEN_COLORS
            else:
                self.text = self.name + " OFF"
                self.colors = BUTTON_RED_COLORS
            self.update(self.var)

    def create_title(self) -> None:
        text = ["SETTINGS"]
        for i in range(len(text)):
            text[i] = Text(self.game, text[i], 30, font=Font.TITLE)
            text[i].move_center(self.game.width // 2, 30 + i * 40)
            self.static_objects.append(text[i])

    def create_buttons(self) -> None:
        names = [
            ("SOUND", "VOLUME"),
            ("FUN", "FUN"),
        ]
        self.buttons = []
        for i in range(len(names)):
            self.buttons.append(self.SettingButton(self.game, names[i][0], i, names[i][1]))
        self.buttons.append(
            self.SceneButton(
                game=self.game,
                geometry=pg.Rect(0, 0, 180, 40),
                text='MENU',
                scene=(self.game.scenes.MENU, False),
                center=(self.game.width // 2, 250),
                text_size=Font.BUTTON_TEXT_SIZE
            )
        )
        self.objects.append(ButtonController(self.game, self.buttons))
