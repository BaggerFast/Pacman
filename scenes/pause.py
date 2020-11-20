import pygame
from objects.button import ButtonController, Button
from objects.text import Text
from scenes.base import BaseScene
from misc.constants import Color


class PauseScene(BaseScene):

    def create_objects(self) -> None:
        self.create_title()
        self.create_buttons()

    def create_buttons(self) -> None:
        buttons = [
            Button(self.game, pygame.Rect(0, 0, 180, 45),
                   self.continue_game, 'CONTINUE',
                   center=(self.game.width // 2, 100)),
            Button(self.game, pygame.Rect(0, 0, 180, 45),
                   self.restart_game, 'RESTART',
                   center=(self.game.width // 2, 161)),
            Button(self.game, pygame.Rect(0, 0, 180, 45),
                   self.start_menu, 'MAIN MENU',
                   center=(self.game.width // 2, 224)),
        ]
        self.button_controller = ButtonController(self.game, buttons)
        self.objects.append(self.button_controller)

    def create_title(self) -> None:
        self.main_text = Text(self.game, 'PAUSE', 40, color=Color.WHITE)
        self.main_text.move_center(self.game.width // 2, 35)
        self.objects.append(self.main_text)

    def restart_game(self) -> None:
        self.game.set_scene(self.game.SCENE_GAME, resume=False)

    def continue_game(self) -> None:
        self.game.set_scene(self.game.SCENE_GAME, resume=True)

    def start_menu(self) -> None:
        self.game.set_scene(self.game.SCENE_MENU)

    def process_event(self, event: pygame.event.Event) -> None:
        super().process_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.continue_game()

    def on_activate(self) -> None:
        self.button_controller.reset_state()
