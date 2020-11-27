import pygame as pg

from misc import Color, Font
from objects import ButtonController, Button, Text
from scenes import BaseScene
from scenes.main import GameScene


class LevelsScene(BaseScene):
    def create_objects(self) -> None:
        self.__create_title()
        self.__create_buttons()

    def __create_title(self) -> None:
        title = Text(self.game, 'SELECT LEVEL', 25, color=Color.WHITE, font=Font.FILENAME)
        title.move_center(self.game.width // 2, 30)
        self.objects.append(title)

    def __create_buttons(self) -> None:
        buttons = [
            Button(self.game, pg.Rect(0, 0, 180, 40),
                   self.__level1, 'LEVEL 1',
                   center=(self.game.width // 2, 90),
                   text_size=Font.BUTTON_TEXT_SIZE),
            Button(self.game, pg.Rect(0, 0, 180, 40),
                   self.__level2, 'LEVEL 2',
                   center=(self.game.width // 2, 140),
                   text_size=Font.BUTTON_TEXT_SIZE),
            Button(self.game, pg.Rect(0, 0, 180, 40),
                   self.__level3, 'LEVEL 3',
                   center=(self.game.width // 2, 190),
                   text_size=Font.BUTTON_TEXT_SIZE),
            Button(self.game, pg.Rect(0, 0, 180, 40),
                   self.__start_menu, 'MENU',
                   center=(self.game.width // 2, 250),
                   text_size=Font.BUTTON_TEXT_SIZE)
        ]
        for index in range(len(buttons)):
            if self.game.level_name == buttons[index].text.lower().replace(' ', '_'):
                buttons[index] = Button(self.game, pg.Rect(0, 0, 180, 40),
                   buttons[index].function, '» ' + buttons[index].text + ' «',
                   center=(buttons[index].rect.centerx, buttons[index].rect.centery),
                   text_size=Font.BUTTON_TEXT_SIZE)
        self.__button_controller = ButtonController(self.game, buttons)
        self.objects.append(self.__button_controller)

    def on_activate(self) -> None:
        self.create_objects()
        self.__button_controller.reset_state()

    def __start_menu(self) -> None:
        self.game.set_scene(self.game.scenes.SCENE_MENU)

    def additional_event_check(self, event: pg.event.Event) -> None:
        if self.game.current_scene == self:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.game.set_scene(self.game.scenes.SCENE_MENU)

    def __set_level(self, name="level_1") -> None:
        """
        :param name: level_+id (e.g. level_1)
        """
        self.game.level_name = name
        self.game.scenes.SCENE_GAME.recreate(self.game)
        self.game.records.update_records()
        self.game.set_scene(self.game.scenes.SCENE_MENU)

    def __level1(self) -> None:
        self.__set_level("level_1")

    def __level2(self) -> None:
        self.__set_level("level_2")

    def __level3(self) -> None:
        pass
