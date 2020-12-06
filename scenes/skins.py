import pygame as pg

from objects import ButtonController, Text
from objects.button.button import SkinButton, SceneButton
from scenes import base
from misc import Font, Maps


class Scene(base.Scene):
    def create_static_objects(self):
        self.__create_title()

    def __create_title(self) -> None:
        title = Text(self.game, 'SELECT SKIN', 25, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        self.static_object.append(title)

    def create_buttons(self) -> None:
        buttons = []

        colors = {
            0: ('YELLOW', (255, 255, 0)),
            1: ('RED', (255, 0, 0)),
            2: ('GREEN', (0, 255, 0)),
            3: ('BLUE', (0, 0, 255)),
        }

        for i in range(len(colors)):
            buttons.append(SkinButton(self.game, pg.Rect(0, 0, 180, 30),
                   text=colors[i][0],
                   value=colors[i][1],
                   center=(self.game.width // 2, 95+i*33),
                   text_size=Font.BUTTON_TEXT_SIZE))

        buttons.append(SceneButton(self.game, pg.Rect(0, 0, 180, 40),
                   text='MENU',
                   scene=(self.game.scenes.MENU, False),
                   center=(self.game.width // 2, 250),
                   text_size=Font.BUTTON_TEXT_SIZE))

        self.objects.append(ButtonController(self.game, buttons))
