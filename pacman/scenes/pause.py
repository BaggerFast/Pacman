import pygame as pg
from pacman.objects import ButtonController, Text
from pacman.scenes import base
from pacman.misc import Font, BUTTON_TRANSPERENT_COLORS


class PauseScene(base.Scene):
    def create_buttons(self) -> None:
        names = {
            0: ("CONTINUE", self.game.scenes.MAIN, False),
            1: ("SETTINGS", self.game.scenes.SETTINGS, True),
            2: ("RESTART", self.game.scenes.MAIN, True),
            3: ("MENU", self.game.scenes.MENU, False),
        }
        buttons = []
        for i in range(len(names)):
            buttons.append(
                self.SceneButton(
                    game=self.game,
                    geometry=pg.Rect(0, 0, 180, 40),
                    text=names[i][0],
                    scene=(names[i][1], names[i][2]),
                    center=(self.game.width // 2, 100 + 45 * i),
                    text_size=Font.BUTTON_TEXT_SIZE,
                    colors=BUTTON_TRANSPERENT_COLORS,
                )
            )
        self.objects.append(ButtonController(self.game, buttons))

    def create_title(self) -> None:
        self.__main_text = Text(self.game, "PAUSE", 40, font=Font.TITLE)
        self.__main_text.move_center(self.game.width // 2, 35)
        self.static_objects.append(self.__main_text)

    def additional_event_check(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.game.scenes.set(self.game.scenes.MAIN)
