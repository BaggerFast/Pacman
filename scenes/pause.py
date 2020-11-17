import pygame
from objects.button import Button
from objects.text import Text
from scenes.base import BaseScene
from misc.constants import Color, BUTTON_DEFAULT_COLORS


class PauseScene(BaseScene):

    def create_objects(self) -> None:

        # Создание и обработка текста
        self.main_text = Text(self.game, 'PAUSE', 40, color=Color.WHITE)
        self.main_text.move_center(self.game.width // 2, 35)
        self.objects.append(self.main_text)

        # Создание и обработка кнопок
        self.continue_button = Button(
            self.game, pygame.Rect(0, 0, 180, 45),
            self.continue_game, 'CONTINUE', **BUTTON_DEFAULT_COLORS
        )
        self.continue_button.move_center(self.game.width // 2, 100)
        self.objects.append(self.continue_button)

        self.restart_button = Button(
            self.game, pygame.Rect(0, 0, 180, 45),
            self.restart_game, 'RESTART', **BUTTON_DEFAULT_COLORS
        )
        self.restart_button.move_center(self.game.width // 2, 161)
        self.objects.append(self.restart_button)

        self.menu_button = Button(
            self.game, pygame.Rect(0, 0, 180, 45),
            self.start_menu, 'MAIN MENU', **BUTTON_DEFAULT_COLORS
        )
        self.menu_button.move_center(self.game.width // 2, 224)
        self.objects.append(self.menu_button)

    def additional_event_check(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.continue_game()

    def restart_game(self):
        self.game.set_scene(self.game.SCENE_GAME, resume=False)

    def continue_game(self):
        self.game.set_scene(self.game.SCENE_GAME, resume=True)

    def start_menu(self):
        self.game.set_scene(self.game.SCENE_MENU)