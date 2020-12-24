import pygame as pg
from objects import ButtonController, Text
from scenes import base
from misc import Font, LIGHT_BUTTON_COLORS
from scenes.menu import rand_color


class Scene(base.Scene):
    def create_buttons(self) -> None:
        names = [
            ("CONTINUE", self.game.scenes.MAIN.Continue),
            ("SETTINGS", self.game.scenes.SETTINGS),
            ("RESTART", self.game.scenes.MAIN),
            ("MENU", self.game.scenes.MENU),
        ]
        buttons = []
        for i in range(len(names)):
            buttons.append(self.SceneButton(
                game=self.game,
                geometry=pg.Rect(0, 0, 180, 40),
                text=names[i][0],
                scene=names[i][1],
                center=(self.game.width // 2, 100+45*i),
                text_size=Font.BUTTON_TEXT_SIZE,
                colors=LIGHT_BUTTON_COLORS
            ))
        self.objects.append(ButtonController(self.game, buttons))

    def create_title(self) -> None:
        self.__main_text = Text(self.game, 'PAUSE', 40, font=Font.TITLE)
        self.__main_text.move_center(self.game.width // 2, 35)
        self.static_objects.append(self.__main_text)

    def additional_event_check(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.game.scenes.set(self.game.scenes.MAIN)

    def on_deactivate(self) -> None:
        self.game.pred = True
        self.game.map_color = rand_color()
