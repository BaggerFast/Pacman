import pygame as pg

from objects import ButtonController, Text
from objects import ButtonController, Text
from objects.button.button import SceneButton
from scenes import base
from misc import Font, Maps
from misc import Font


class Scene(base.Scene):
    def create_objects(self) -> None:
        super().create_objects()
        self.__create_indicator()

    def create_title(self) -> None:
        title = Text(self.game, 'PACMAN', 36, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        self.static_object.append(title)

    def __create_indicator(self) -> None:
        self.__indicator = Text(self.game, Maps.level_name(self.game.level_id).replace('_', ' '), 15, font=Font.TITLE)
        self.__indicator.move_center(self.game.width // 2, 60)
        self.objects.append(self.__indicator)

    def create_buttons(self) -> None:
        names = {
            0: ("PLAY", self.game.scenes.MAIN, True),
            1: ("LEVELS", self.game.scenes.LEVELS, False),
            2: ("SETTINGS", self.game.scenes.SETTINGS, False),
            3: ("RECORDS", self.game.scenes.RECORDS, False),
            4: ("CREDITS", self.game.scenes.CREDITS, False),
            5: ("EXIT", self.game.exit_game, None)
        }
        buttons = []
        for i in range(len(names)):
            buttons.append(
                self.SceneButton(
                    game=self.game,
                    geometry=pg.Rect(0, 0, 180, 30),
                    text=names[i][0],
                    scene=(names[i][1], names[i][2]),
                    center=(self.game.width // 2, 95 + i * 33),
                    text_size=Font.BUTTON_TEXT_SIZE
                )
            )
        self.objects.append(ButtonController(self.game, buttons))
