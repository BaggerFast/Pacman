import pygame as pg

from misc import Font, Maps
from objects import ButtonController, Button, Text
from objects.button.button import LvlButton
from scenes import base


class Scene(base.Scene):
    def create_objects(self) -> None:
        self.__create_title()
        self.__create_buttons()

    def __create_title(self) -> None:
        title = Text(self.game, 'SELECT LEVEL', 25, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        self.objects.append(title)

    def __create_buttons(self) -> None:
        buttons = []
        for i in range(Maps.count):
            buttons.append(
                LvlButton(
                   game=self.game,
                   geometry=pg.Rect(0, 0, 180, 40),
                   value=i,
                   text='LEVEL' + str(i+1),
                   center=(self.game.width // 2, 90+50*i),
                   text_size=Font.BUTTON_TEXT_SIZE,
                   active="level_1" in self.game.unlocked_levels)
            )

        buttons.append(Button(self.game, pg.Rect(0, 0, 180, 40),
                   self.__start_menu, 'MENU',
                   center=(self.game.width // 2, 250),
                   text_size=Font.BUTTON_TEXT_SIZE))

        for index in range(len(buttons)):
            if str(self.game.level_id + 1) == buttons[index].text[-1:]:
                buttons[index] = Button(self.game, pg.Rect(0, 0, 180, 40),
                                        buttons[index].function, '» ' + buttons[index].text + ' «',
                                        center=(buttons[index].rect.centerx, buttons[index].rect.centery),
                                        text_size=Font.BUTTON_TEXT_SIZE)
        self.__button_controller = ButtonController(self.game, buttons)
        self.objects.append(self.__button_controller)

    def on_activate(self) -> None:
        self.objects = []
        self.create_objects()
        self.create_objects()
        self.__button_controller.reset_state()

    def __start_menu(self) -> None:
        self.game.scenes.set(self.game.scenes.MENU)

    def additional_event_check(self, event: pg.event.Event) -> None:
        if self.game.current_scene == self:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.game.scenes.set(self.game.scenes.MENU)

