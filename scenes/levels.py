import pygame as pg


from objects.button import ButtonController, Button
from scenes.base import BaseScene
from objects.text import Text
from misc.constants import Color, Font
from scenes.main import GameScene


class LevelsScene(BaseScene):
    def create_objects(self) -> None:
        self.create_title()
        self.create_buttons()

    def create_title(self) -> None:
        title = Text(self.game, 'SELECT LEVEL', 25, color=Color.WHITE, font=Font.FILENAME)
        title.move_center(self.game.width // 2, 30)
        self.objects.append(title)

    def create_buttons(self) -> None:
        buttons = [
            Button(self.game, pg.Rect(0, 0, 180, 45),
                   self.level1, 'LEVEL 1',
                   center=(self.game.width // 2, 100),
                   text_size=Font.BUTTON_TEXT_SIZE),
            Button(self.game, pg.Rect(0, 0, 180, 45),
                   self.level2, 'LEVEL 2',
                   center=(self.game.width // 2, 163),
                   text_size=Font.BUTTON_TEXT_SIZE),
            Button(self.game, pg.Rect(0, 0, 180, 45),
                   self.level3, 'LEVEL 3',
                   center=(self.game.width // 2, 226),
                   text_size=Font.BUTTON_TEXT_SIZE)
        ]

        self.button_controller = ButtonController(self.game, buttons)
        self.objects.append(self.button_controller)

    def additional_event_check(self, event: pg.event.Event) -> None:
        if self.game.scenes[self.game.current_scene_name] == self:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.game.set_scene('SCENE_MENU')

    def set_level(self, name="level_1") -> None:
        """
        :param name: level_+id (e.g. level_1)
        """
        self.game.level_name = name
        self.game.scenes["SCENE_GAME"] = GameScene(self.game)
        self.game.records.update_records()
        self.game.set_scene('SCENE_MENU')

    def level1(self) -> None:
        self.set_level("level_1")

    def level2(self) -> None:
        self.set_level("level_2")

    def level3(self) -> None:
        pass
