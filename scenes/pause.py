import pygame
from objects.button import ButtonContainer, Button
from objects.text import Text
from scenes.base import BaseScene
from misc.constants import Color


class PauseScene(BaseScene):

    def create_objects(self) -> None:

        self.current_button = -1

        # Создание и обработка текста
        self.main_text = Text(self.game, 'PAUSE', 40, color=Color.WHITE)
        self.main_text.move_center(self.game.width // 2, 35)
        self.objects.append(self.main_text)

        # Создание и обработка кнопок
        self.continue_button = Button(self.game, pygame.Rect(0, 0, 180, 45),
                                      self.continue_game, 'CONTINUE', center=(self.game.width // 2, 100))
        self.restart_button = Button(self.game, pygame.Rect(0, 0, 180, 45),
                                     self.restart_game, 'RESTART', center=(self.game.width // 2, 161))
        self.menu_button = Button(self.game, pygame.Rect(0, 0, 180, 45),
                                  self.start_menu, 'MAIN MENU', center=(self.game.width // 2, 224))

        self.objects.append(self.continue_button)
        self.objects.append(self.restart_button)
        self.objects.append(self.menu_button)

        self.buttons = [
            self.continue_button,
            self.restart_button,
            self.menu_button
        ]
        self.control = ButtonContainer(self.game, self.buttons)

    def additional_event_check(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.continue_game()

        if event.key == pygame.K_w or event.key == pygame.K_UP:
            self.control.unset_previous_button(self.current_button)
            self.current_button -= 1
            if self.current_button < 0:
                self.current_button = 2
            self.control.set_current_button(self.current_button)
        if event.key == pygame.K_s or event.key == pygame.K_DOWN:
            self.control.unset_previous_button(self.current_button)
            self.current_button += 1
            if self.current_button > 2:
                self.current_button = 0
            self.control.set_current_button(self.current_button)
        if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
            self.buttons[self.current_button].on_click()

        self.control.mouse_action()

    def restart_game(self):
        self.game.set_scene(self.game.SCENE_GAME, resume=False)

    def continue_game(self):
        self.game.set_scene(self.game.SCENE_GAME, resume=True)

    def start_menu(self):
        self.game.set_scene(self.game.SCENE_MENU)

    def process_event(self, event: pygame.event.Event) -> None:
        self.continue_button.process_event(event)
        self.restart_button.process_event(event)
        self.menu_button.process_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.continue_game()

