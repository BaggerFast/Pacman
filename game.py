import pygame

from misc.constants import Color
from misc.highscore import HighScore
from scenes.levels import LevelsScene
from scenes.main import GameScene
from scenes.menu import MenuScene
from scenes.pause import PauseScene
from scenes.records import RecordsScene


class Game:
    size = width, height = 224, 285
    SCENE_MENU = 0
    SCENE_GAME = 1
    SCENE_PAUSE = 2
    SCENE_RECORDS = 3
    SCENE_LEVELS = 4
    current_scene_index = SCENE_MENU

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode(self.size, pygame.SCALED)
        self.lives = 3
        self.score = 0
        self.records = HighScore()

        self.scenes = [
            MenuScene(self),
            GameScene(self),
            PauseScene(self),
            RecordsScene(self),
            LevelsScene(self),
        ]

        self.game_over = False

    @staticmethod
    def exit_button_pressed(event: pygame.event.Event) -> bool:
        return event.type == pygame.QUIT

    @staticmethod
    def exit_hotkey_pressed(event: pygame.event.Event) -> bool:
        return event.type == pygame.KEYDOWN and event.mod & pygame.KMOD_CTRL and event.key == pygame.K_q

    def process_exit_events(self, event: pygame.event.Event) -> None:
        if Game.exit_button_pressed(event) or Game.exit_hotkey_pressed(event):
            self.exit_game()

    def resize_scenes(self) -> None:
        for scene in self.scenes:
            scene.on_window_resize()

    def process_resize_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.VIDEORESIZE:
            return
        self.SIZE = self.WIDTH, self.HEIGHT = event.w, event.h
        self.screen = pygame.display.set_mode(self.SIZE, pygame.RESIZABLE)
        self.resize_scenes()

    def process_all_events(self) -> None:
        for event in pygame.event.get():
            self.process_exit_events(event)
            self.process_resize_event(event)
            self.scenes[self.current_scene_index].process_event(event)

    def process_all_logic(self) -> None:
        self.scenes[self.current_scene_index].process_logic()

    def process_all_draw(self) -> None:
        self.screen.fill(Color.BLACK)
        self.scenes[self.current_scene_index].process_draw()
        pygame.display.flip()

    def main_loop(self) -> None:
        while not self.game_over:
            self.process_all_events()
            self.process_all_logic()
            self.process_all_draw()
            pygame.time.wait(10)

    def set_scene(self, index: int, resume: bool = False) -> None:
        if not resume:
            self.scenes[self.current_scene_index].on_deactivate()
        self.current_scene_index = index
        if not resume:
            self.scenes[self.current_scene_index].on_activate()

    def exit_game(self) -> None:
        print('Bye bye')
        self.game_over = True
