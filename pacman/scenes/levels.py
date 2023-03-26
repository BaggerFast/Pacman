import pygame as pg

from pacman.data_core import KbKeys, Colors
from pacman.misc import Font
from pacman.misc.serializers import LevelStorage
from pacman.objects import ButtonController, Text, ImageObject
from pacman.scenes import base


class LevelsScene(base.Scene):
    def create_static_objects(self):
        self.__create_title()

    def __create_title(self) -> None:
        title = Text("SELECT LEVEL", 25, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        self.static_objects.append(title)

    def create_buttons(self) -> None:
        buttons = []
        buttons.append(
            self.SceneButton(
                game=self.game,
                rect=pg.Rect(0, 0, 180, 40),
                text="MENU",
                scene=(self.game.scenes.MENU, False),
                text_size=Font.BUTTON_TEXT_SIZE,
            ).move_center(self.game.width // 2, 250)
        )
        self.__button_controller = ButtonController(buttons)
        self.objects.append(self.__button_controller)

    @property
    def current_level(self) -> int:
        return LevelStorage().current

    def create_objects(self) -> None:
        self.objects = []
        self.preview: ImageObject = self.game.maps.images[LevelStorage().current]
        self.preview.smoothscale(224 * 0.6, 248 * 0.6)
        self.preview.move_center(self.game.size[0] // 2, self.game.size[1] // 2)
        self.objects.append(self.preview)

        self.text = Text(f"Level: {self.current_level+1}/{LevelStorage().level_count}", 20).move_center(
            self.game.size[0] // 2, self.game.size[1] // 2
        )
        self.text2 = Text(f"L", 40, color=Colors.DARK_GRAY).move_center(
            self.game.size[0] // 6 - 10, self.game.size[1] // 2
        )
        self.text3 = Text(f"R", 40, color=Colors.DARK_GRAY).move_center(
            self.game.size[0] - (self.game.size[0] // 6 - 16), self.game.size[1] // 2
        )
        if self.current_level == 0:
            self.text2.color = Colors.BLACK
        if self.current_level == LevelStorage().level_count - 1:
            self.text3.color = Colors.BLACK
            self.text = Text(f"Level: {self.current_level + 1}", 20).move_center(
                self.game.size[0] // 2, self.game.size[1] // 2
            )
        elif self.current_level + 1 not in LevelStorage().unlocked:
            self.text3.color = Colors.BLACK

        self.objects.append(self.text)
        self.objects.append(self.text2)
        self.objects.append(self.text3)
        self.create_buttons()

    def additional_event_check(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.game.scenes.set(self.game.scenes.MENU)
        elif event.type == pg.KEYDOWN:
            if event.key in KbKeys.RIGHT and self.current_level != LevelStorage().level_count - 1:
                if self.current_level + 1 in LevelStorage().unlocked:
                    LevelStorage().set_next_level()
            elif event.key in KbKeys.LEFT and self.current_level != 0:
                LevelStorage().set_prev_level()
            self.preview: ImageObject = self.game.maps.images[self.current_level]
            self.preview.smoothscale(224 * 0.6, 248 * 0.6)
            self.preview.move_center(self.game.size[0] // 2, self.game.size[1] // 2)
            self.objects.append(self.preview)
            self.text3.color = Colors.DARK_GRAY
            self.text2.color = Colors.DARK_GRAY
            if self.current_level == 0:
                self.text2.color = Colors.BLACK
            if self.current_level == LevelStorage().level_count - 1:
                self.text3.color = Colors.BLACK
                self.text = Text(f"Level: {self.current_level + 1}", 20).move_center(
                    self.game.size[0] // 2, self.game.size[1] // 2
                )
            elif self.current_level + 1 not in LevelStorage().unlocked:
                self.text3.color = Colors.BLACK
            self.text = Text(f"Level: {self.current_level + 1}/{LevelStorage().level_count}", 20).move_center(
                self.game.size[0] // 2, self.game.size[1] // 2
            )
            self.objects.append(self.text)
