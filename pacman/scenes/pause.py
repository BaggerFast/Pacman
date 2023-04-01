import pygame as pg

from pacman.data_core import Config
from pacman.objects import ButtonController, Text, Button
from pacman.scenes import base
from pacman.misc import Font


class PauseScene(base.Scene):
    def create_buttons(self) -> None:
        names = {
            0: ("CONTINUE", lambda: self.click_btn(self.game.scenes.MAIN, False)),
            1: ("SETTINGS", lambda: self.click_btn(self.game.scenes.SETTINGS, True)),
            2: ("RESTART", lambda: self.click_btn(self.game.scenes.MAIN, True)),
            3: ("MENU", lambda: self.click_btn(self.game.scenes.MENU, False)),
        }
        buttons = []
        for i in range(len(names)):
            buttons.append(
                Button(
                    game=self.game,
                    rect=pg.Rect(0, 0, 180, 40),
                    text=names[i][0],
                    function=names[i][1],
                    text_size=Font.BUTTON_TEXT_SIZE,
                ).move_center(Config.RESOLUTION.half_width, 100 + 45 * i)
            )
        self.objects.append(ButtonController(buttons))

    def create_title(self) -> None:
        self.__main_text = Text("PAUSE", 40, font=Font.TITLE)
        self.__main_text.move_center(Config.RESOLUTION.half_width, 35)
        self.static_objects.append(self.__main_text)

    def additional_event_check(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.game.scenes.set(self.game.scenes.MAIN)
