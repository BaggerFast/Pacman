import json
import os

import pygame as pg

from misc import Font, Maps, ROOT_DIR
from objects import ButtonController, Text
from objects.button import Button
from scenes import base


class Scene(base.Scene):
    __is_scroll_active = False
    __scroll = 0
    __counter = 0

    __storage_filepath = os.path.join(ROOT_DIR, "saves", "storage.json")

    class LvlButton(Button):
        def __init__(self, **args):
            self.value = args.pop("value")
            super(Scene.LvlButton, self).__init__(**args)


        def click(self):
            self.game.level_id = self.value
            self.game.records.update_records()
            self.game.scenes.set(self.game.scenes.MENU, reset=True)

    def create_static_objects(self):
        __counter = int(Maps.level_name(self.game.level_id)[-1:])
        self.__create_title()
        for i in range(self.game.level_id):
            self.__counter += 1
            self.__scroll -= 50

        if self.__scroll > 0:
            self.__scroll = 0
        if self.__scroll < -350:
            self.__scroll = -350

    def __create_title(self) -> None:
        title = Text(self.game, 'SELECT LEVEL', 25, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        self.static_object.append(title)

    def create_buttons(self) -> None:
        buttons = []
        for i in range(Maps.count):
            buttons.append(
                self.LvlButton(
                    game=self.game,
                    geometry=pg.Rect(0, 0, 180, 40),
                    value=i,
                    text='LEVEL' + str(i + 1),
                    center=(self.game.width // 2, self.button_y_cord(90 + 50 * i)),
                    text_size=Font.BUTTON_TEXT_SIZE,
                    active=i in self.game.unlocked_levels)
            )
        buttons.append(self.SceneButton(
            game=self.game,
            geometry=pg.Rect(0, 0, 180, 40),
            text='MENU',
            scene=(self.game.scenes.MENU, False),
            center=(self.game.width // 2, 250),
            text_size=Font.BUTTON_TEXT_SIZE))

        for index in range(len(buttons)):
            if str(self.game.level_id + 1) == buttons[index].text[-1:] \
                or str(self.game.level_id + 1) == buttons[index].text[-2:]:
                buttons[index].text = '» ' + buttons[index].text + ' «'

        self.__button_controller = ButtonController(self.game, buttons)
        self.objects.append(self.__button_controller)

    def button_y_cord(self, y):
        if 80 < self.__scroll + y < 290:
            return self.__scroll + y
        return 1000

    def unlocked(self) -> int:
        with open(self.__storage_filepath, "r") as file:
            json_dict = json.load(file)
            return json_dict["level_id"]

    def additional_event_check(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.game.scenes.set(self.game.scenes.MENU)
        elif event.type == pg.KEYDOWN and (event.key == pg.K_DOWN or event.key == pg.K_s) and self.__is_scroll_active:
            if self.__counter == self.unlocked() + 1:
                self.__counter = 0
            else:
                self.__counter += 1
                self.__scroll = self.__counter * -50
                if self.__scroll > 0:
                    self.__scroll = 0
                if self.__scroll < self.unlocked() * -50:
                    self.__scroll = self.unlocked() * -50

            self.game.scenes.set(self.game.scenes.LEVELS)
            for i in range(self.__counter + 1):
                self.__button_controller.select_next_button()

        elif event.type == pg.KEYDOWN and (event.key == pg.K_UP or event.key == pg.K_w) and self.__is_scroll_active:
            if self.__counter == 0:
                self.__counter = 10
            else:
                self.__counter -= 1
                self.__scroll = self.__counter * -50
                if self.__scroll > 0:
                    self.__scroll = 0
                if self.__scroll < self.unlocked() * -50:
                    self.__scroll = self.unlocked() * -50

            self.game.scenes.set(self.game.scenes.LEVELS)
            for i in range(self.__counter + 1):
                self.__button_controller.select_next_button()
        elif event.type == pg.KEYDOWN and (
            event.key == pg.K_UP or event.key == pg.K_DOWN or event.key == pg.K_w or event.key == pg.K_s) and not self.__is_scroll_active:
            for i in range(self.__counter + 1):
                self.__button_controller.select_next_button()
            self.__is_scroll_active = True
