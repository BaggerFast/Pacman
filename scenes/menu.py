import pygame as pg

from objects import ButtonController, Button, Text
from scenes import base
from misc import Color, Font


class Scene(base.Scene):
    def __init__(self, game):
        super().__init__(game)

    def create_objects(self) -> None:
        self.__create_title()
        self.__create_buttons()
        self.__create_indicator()

    def __create_title(self) -> None:
        title = Text(self.game, 'PACMAN', 36, color=Color.WHITE, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        self.objects.append(title)

    def __create_indicator(self) -> None:
        self.__indicator = Text(self.game, self.game.level_name.replace('_', ' '),
                                15, color=Color.WHITE, font=Font.TITLE)
        self.__indicator.move_center(self.game.width // 2, 60)
        self.objects.append(self.__indicator)

    def __create_buttons(self) -> None:
        buttons = [
            Button(self.game, pg.Rect(0, 0, 180, 35),
                   self.__start_game, 'PLAY',
                   center=(self.game.width // 2, 95),
                   text_size=Font.BUTTON_TEXT_SIZE),
            Button(self.game, pg.Rect(0, 0, 180, 35),
                   self.__start_levels, 'LEVELS',
                   center=(self.game.width // 2, 135),
                   text_size=Font.BUTTON_TEXT_SIZE),
            Button(self.game, pg.Rect(0, 0, 180, 35),
                   self.__start_records, 'RECORDS',
                   center=(self.game.width // 2, 175),
                   text_size=Font.BUTTON_TEXT_SIZE),
            Button(self.game, pg.Rect(0, 0, 180, 35),
                   self.__start_titres, 'CREDITS',
                   center=(self.game.width // 2, 215),
                   text_size=Font.BUTTON_TEXT_SIZE),
            Button(self.game, pg.Rect(0, 0, 180, 35),
                   self.game.exit_game, 'EXIT',
                   center=(self.game.width // 2, 255),
                   text_size=Font.BUTTON_TEXT_SIZE)
        ]
        self.__button_controller = ButtonController(self.game, buttons)
        self.objects.append(self.__button_controller)

    def __level_indicator(self) -> None:
        self.__indicator.update_text(self.game.level_name.replace('_', ' '))

    def on_activate(self) -> None:
        self.__level_indicator()
        self.__button_controller.reset_state()

    def __start_game(self) -> None:
        self.game.set_scene(self.game.scenes.MAIN, reset=True)

    def __start_records(self) -> None:
        self.game.scenes.RECORDS.create_text_labels()
        self.game.set_scene(self.game.scenes.RECORDS)

    def __start_titres(self) -> None:
        self.game.set_scene(self.game.scenes.CREDITS)

    def __start_levels(self) -> None:
        self.game.set_scene(self.game.scenes.LEVELS)
