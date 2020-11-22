import pygame


from objects.button import ButtonController, Button
from scenes.base import BaseScene
from objects.text import Text
from misc.constants import Color

class LevelsScene(BaseScene):
    def create_objects(self) -> None:
        self.create_title()
        self.create_buttons()

    def create_title(self) -> None:
        title = Text(self.game, 'Level select', 40, color=Color.WHITE)
        title.move_center(self.game.width // 2, 30)
        self.objects.append(title)

    def create_buttons(self) -> None:
        buttons = [
            Button(self.game, pygame.Rect(0, 0, 180, 45),
                   self.level1, 'Level 1',
                   center=(self.game.width // 2, 100)),
            Button(self.game, pygame.Rect(0, 0, 180, 45),
                   self.level2, 'Level 2',
                   center=(self.game.width // 2, 163)),
            Button(self.game, pygame.Rect(0, 0, 180, 45),
                   self.level3, 'Level 3',
                   center=(self.game.width // 2, 226))
        ]

        self.button_controller = ButtonController(self.game, buttons)
        self.objects.append(self.button_controller)

    def level1(self) -> None:
        pass

    def level2(self) -> None:
        pass

    def level3(self) -> None:
        pass
