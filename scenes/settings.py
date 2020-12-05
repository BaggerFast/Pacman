import pygame as pg
from objects import ButtonController, Text
from objects.button.button import SceneButton, SettingButtons
from scenes import base
from misc import Font


class Scene(base.Scene):
    def create_title(self) -> None:
        text = ["SETTING"]
        for i in range(len(text)):
            text[i] = Text(self.game, text[i], 40, font=Font.TITLE)
            text[i].move_center(self.game.width // 2, 30 + i * 40)
            self.static_object.append(text[i])

    def create_buttons(self) -> None:
        names = ['Sound off']
        self.buttons = []
        for i in range(len(names)):
            self.buttons.append(SettingButtons(
                game=self.game,
                geometry=pg.Rect(0, 0, 180, 35),
                text=names[i],
                center=(self.game.width // 2, 95+i*33),
                text_size=Font.BUTTON_TEXT_SIZE))
        self.buttons.append(SceneButton(self.game, pg.Rect(0, 0, 180, 40),
                                   text='MENU',
                                   scene=(self.game.scenes.MENU, False),
                                   center=(self.game.width // 2, 250),
                                   text_size=Font.BUTTON_TEXT_SIZE))
        self.objects.append(ButtonController(self.game, self.buttons))
