import pygame as pg

from objects import ButtonController, Button, Text
from objects.button.button import SceneButton
from scenes import base
from misc import Font


class Scene(base.Scene):
    def create_objects(self) -> None:
        self.__create_title()
        self.__create_indicator()

    def __create_title(self) -> None:
        title = Text(self.game, 'PACMAN', 36, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        self.objects.append(title)

    def __create_indicator(self) -> None:
        self.__indicator = Text(self.game, self.game.level_name.replace('_', ' '),
                                15, font=Font.TITLE)
        self.__indicator.move_center(self.game.width // 2, 60)
        self.objects.append(self.__indicator)

    def __create_buttons(self) -> None:
        names = {
            0: ("PLAY", self.game.scenes.MAIN, True),
            1: ("LEVELS", self.game.scenes.LEVELS, False),
            2: ("RECORDS", self.game.scenes.RECORDS, False),
            3: ("CREDITS", self.game.scenes.CREDITS, False),
            4: ("EXIT", self.game.exit_game, None)
        }
        buttons = []
        for i in range(len(names)):
            buttons.append(SceneButton(self.game, pg.Rect(0, 0, 180, 35),
                   text=names[i][0],
                   scene=(names[i][1], names[i][2]),
                   center=(self.game.width // 2, 95+i*40),
                   text_size=Font.BUTTON_TEXT_SIZE))
        self.__button_controller = ButtonController(self.game, buttons)
        self.objects.append(self.__button_controller)

    def __level_indicator(self) -> None:
        self.__indicator.text = self.game.level_name.replace('_', ' ')

    def on_activate(self) -> None:
        self.objects = []
        self.create_objects()
        self.__create_buttons()




