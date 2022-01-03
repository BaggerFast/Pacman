import pygame as pg
from objects import Text
from misc import Font, LIGHT_BUTTON_COLORS
from objects.button import Button
from scenes.base import BaseScene


class PauseScene(BaseScene):

    def button_init(self) -> None:
        names = {
            "CONTINUE": self.game.scene_manager.pop,
            "SETTINGS": lambda: self.game.scene_manager.append(self.scenes.SETTINGS(self.game)),
            "RESTART": lambda: self.game.scene_manager.reset(self.scenes.MAIN(self.game)),
            "MENU": lambda: self.game.scene_manager.append(self.scenes.MENU(self.game)),
        }
        for i, (name, scene) in enumerate(names.items()):
            yield Button(
                game=self.game,
                rect=pg.Rect(0, 0, 180, 40),
                text=name,
                function=scene,
                center=(self.game.width // 2, 100+45*i),
                text_size=Font.BUTTON_TEXT_SIZE,
                colors=LIGHT_BUTTON_COLORS
            )

    def create_title(self) -> None:
        main_text = Text(self.game, 'PAUSE', 40, font=Font.TITLE)
        main_text.move_center(self.game.width // 2, 35)
        self.objects.append(main_text)
