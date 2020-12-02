import pygame as pg

from misc import Color, Font, get_path
from objects import Button, ButtonController, ImageObject, Text
from objects.button.button import SceneButton
from scenes import base


class Scene(base.Scene):
    def create_objects(self) -> None:
        self.__create_title()
        self.__create_error_label()
        self.__create_text_labels()
        self.__create_medals()

    def __create_text_labels(self) -> None:
        self.game.records.update_records()
        self.medals_text = []
        text_colors = [Color.GOLD, Color.SILVER, Color.BRONZE, Color.WHITE, Color.WHITE]
        y = 4
        for i in range(5):
            self.medals_text.append(Text(self.game, str(self.game.records.data[y]), 30, pg.Rect(60, 55+35*i, 0, 0), text_colors[i]))
            y -= 1

    def __create_medals(self) -> None:
        self.__medals = []
        for i in range(5):
            self.__medals.append(ImageObject(self.game, get_path(str(i), 'png', 'images', 'medal'), (16, 55+35*i)))
            self.__medals[i].scale(35, 35)

    def __create_buttons(self) -> None:
        self.back_button = SceneButton(self.game, pg.Rect(0, 0, 180, 40),
                                  text='MENU',
                                  scene=(self.game.scenes.MENU, False),
                                  center=(self.game.width // 2, 250),
                                  text_size=Font.BUTTON_TEXT_SIZE)
        self.__button_controller = ButtonController(self.game, [self.back_button])
        self.objects.append(self.__button_controller)

    def __create_title(self) -> None:
        title = Text(self.game, 'RECORDS', 32, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        self.objects.append(title)

    def __create_error_label(self) -> None:
        self.__error_text = Text(self.game, 'NO RECORDS', 24, color=Color.RED)
        self.__error_text.move_center(self.game.width // 2, 100)

    def __start_menu(self) -> None:
        self.game.scenes.set(self.game.scenes.MENU)

    def on_activate(self) -> None:
        self.game.scenes.RECORDS.__create_text_labels()
        self.__create_buttons()
        self.__button_controller.reset_state()

    def process_draw(self) -> None:
        super().process_draw()

        if self.game.records.data[4] == 0:
            self.__error_text.process_draw()

        y = 4
        for i in range(5):
            if self.game.records.data[y] != 0:
                self.medals_text[i].process_draw()
                self.__medals[i].process_draw()
            y -= 1

    def additional_event_check(self, event: pg.event.Event) -> None:
        if self.game.current_scene == self:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.game.scenes.set(self.game.scenes.MENU)
