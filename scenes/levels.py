import pygame as pg

from misc import Font
from objects import ButtonController, Button, Text
from scenes import base


class Scene(base.Scene):
    def create_objects(self) -> None:
        self.objects = []
        self.__create_title()
        self.__create_buttons()

    def __create_title(self) -> None:
        title = Text(self.game, 'SELECT LEVEL', 25, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        self.objects.append(title)

    def __create_buttons(self) -> None:
        buttons = [
            Button(self.game, pg.Rect(0, 0, 180, 40),
                   self.__level1, 'LEVEL 1',
                   center=(self.game.width // 2, 90),
                   text_size=Font.BUTTON_TEXT_SIZE,
                   active=0 in self.game.unlocked_levels),
            Button(self.game, pg.Rect(0, 0, 180, 40),
                   self.__level2, 'LEVEL 2',
                   center=(self.game.width // 2, 140),
                   text_size=Font.BUTTON_TEXT_SIZE,
                   active=1 in self.game.unlocked_levels),
            Button(self.game, pg.Rect(0, 0, 180, 40),
                   self.__level3, 'LEVEL 3',
                   center=(self.game.width // 2, 190),
                   text_size=Font.BUTTON_TEXT_SIZE,
                   active=2 in self.game.unlocked_levels),
            Button(self.game, pg.Rect(0, 0, 180, 40),
                   self.__start_menu, 'MENU',
                   center=(self.game.width // 2, 250),
                   text_size=Font.BUTTON_TEXT_SIZE)
        ]
        for index in range(len(buttons)):
            if str(self.game.level_id + 1) == buttons[index].text[-1:]:
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
        self.game.scenes.set(self.game.scenes.MENU)

    def additional_event_check(self, event: pg.event.Event) -> None:
        if self.game.current_scene == self:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.game.scenes.set(self.game.scenes.MENU)

    def set_level(self, level_id: int = 0) -> None:
        """
        :param level_id: level_+id (e.g. level_1)
        """
        self.game.level_id = level_id
        self.game.records.update_records()
        self.game.scenes.set(self.game.scenes.MENU, reset=True)

    def __level1(self) -> None:
        self.set_level(0)

    def __level2(self) -> None:
        self.set_level(1)

    def __level3(self) -> None:
        self.set_level(2)
