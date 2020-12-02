import pygame as pg
from objects import ButtonController, Button, Text
from objects.button.button import SceneButton
from scenes import base
from misc import Font


class Scene(base.Scene):
    def create_objects(self) -> None:
        self.__create_title()

    def __create_buttons(self) -> None:
        names = {
            0: ("CONTINUE", self.game.scenes.MAIN, False),
            1: ("RESTART", self.game.scenes.MAIN, True),
            2: ("MENU", self.game.scenes.MENU, False),
        }
        buttons = []
        for i in range(len(names)):
            buttons.append(SceneButton(self.game, pg.Rect(0, 0, 180, 45),
                text=names[i][0],
                scene=(names[i][1], names[i][2]),
                center=(self.game.width // 2, 100+61*i),
                text_size=Font.BUTTON_TEXT_SIZE))
        self.button_controller = ButtonController(self.game, buttons)
        self.objects.append(self.button_controller)

    def __create_title(self) -> None:
        self.__main_text = Text(self.game, 'PAUSE', 40, font=Font.TITLE)
        self.__main_text.move_center(self.game.width // 2, 35)
        self.objects.append(self.__main_text)

    def process_event(self, event: pg.event.Event) -> None:
        super().process_event(event)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.game.scenes.set(self.game.scenes.MAIN)

    def on_activate(self) -> None:
        self.objects = []
        self.create_objects()
        self.__create_buttons()
