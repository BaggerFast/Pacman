import pygame as pg

from misc import Font, BUTTON_GREEN_COLORS, BUTTON_RED_COLORS
from objects import ButtonController, Text
from objects.button import Button
from scenes import base


class Scene(base.Scene):

    class SettingButton(Button):
        def __init__(self, game, name, i):
            super(Scene.SettingButton, self).__init__(
                game=game,
                geometry=pg.Rect(0, 0, 180, 35),
                text=name + (" OFF" if game.settings.MUTE else " ON "),
                center=(game.width // 2, 95 + i * 33),
                text_size=Font.BUTTON_TEXT_SIZE,
                colors=BUTTON_RED_COLORS if game.settings.MUTE else BUTTON_GREEN_COLORS
            )
            self.name = name

        def click(self):
            self.game.settings.MUTE = not self.game.settings.MUTE
            if self.game.settings.MUTE:
                self.text = self.name + " OFF"
                self.colors = BUTTON_RED_COLORS
            else:
                self.text = self.name + " ON "
                self.colors = BUTTON_GREEN_COLORS
            a = self.game.sounds.__dict__
            for key in a.keys():
                a[key].update_volume()

    def create_title(self) -> None:
        text = ["SETTING"]
        for i in range(len(text)):
            text[i] = Text(self.game, text[i], 40, font=Font.TITLE)
            text[i].move_center(self.game.width // 2, 30 + i * 40)
            self.static_object.append(text[i])

    def create_buttons(self) -> None:
        names = ['Sound']
        self.buttons = []
        for i in range(len(names)):
            self.buttons.append(self.SettingButton(self.game, names[i], i))
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
