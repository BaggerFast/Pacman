import pygame

from constants import Color
from scenes.final import FinalScene
from scenes.main import MainScene
from scenes.menu import MenuScene


class Game:
    size = width, height = 800, 600
    MENU_SCENE_INDEX = 0
    MAIN_SCENE_INDEX = 1
    GAMEOVER_SCENE_INDEX = 2
    current_scene_index = MENU_SCENE_INDEX

    def __init__(self):
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        self.scenes = [MenuScene(self), MainScene(self), FinalScene(self)]
        self.game_over = False

    @staticmethod
    def exit_button_pressed(event):
        return event.type == pygame.QUIT

    @staticmethod
    def exit_hotkey_pressed(event):
        return event.type == pygame.KEYDOWN and event.mod & pygame.KMOD_CTRL and event.key == pygame.K_q

    def process_exit_events(self, event):
        if Game.exit_button_pressed(event) or Game.exit_hotkey_pressed(event):
            self.exit_game()

    def process_all_events(self):
        for event in pygame.event.get():
            self.process_exit_events(event)
            self.scenes[self.current_scene_index].process_event(event)

    def process_all_logic(self):
        self.scenes[self.current_scene_index].process_logic()

    def process_all_draw(self):
        self.screen.fill(Color.BLACK)
        self.scenes[self.current_scene_index].process_draw()
        pygame.display.flip()

    def main_loop(self):
        while not self.game_over:
            self.process_all_events()
            self.process_all_logic()
            self.process_all_draw()
            pygame.time.wait(10)

    def set_scene(self, index, resume=False):
        if not resume:
            self.scenes[self.current_scene_index].on_deactivate()
        self.current_scene_index = index
        if not resume:
            self.scenes[self.current_scene_index].on_activate()

    def exit_game(self):
        print('Bye bye')
        self.game_over = True
