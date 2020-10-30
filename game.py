import pygame

from constants import Color
from scenes import MainScene, MenuScene, FinalScene, PauseScene
from scenes.overlay import OverlayScene


class Game:
    SIZE = WIDTH, HEIGHT = 800, 600
    MENU_SCENE_INDEX = 0
    MAIN_SCENE_INDEX = 1
    GAMEOVER_SCENE_INDEX = 2
    PAUSE_SCENE_INDEX = 3
    current_scene_index = MENU_SCENE_INDEX
    USE_FPS_OVERLAY = False

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode(self.SIZE, pygame.RESIZABLE)
        self.scenes = [MenuScene(self), MainScene(self), FinalScene(self), PauseScene(self)]
        if self.USE_FPS_OVERLAY:
            self.overlay = OverlayScene(self)
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
        if self.USE_FPS_OVERLAY:
            self.overlay.on_window_resize()

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
            if self.USE_FPS_OVERLAY:
                self.overlay.process_event(event)

    def process_all_logic(self) -> None:
        self.scenes[self.current_scene_index].process_logic()
        if self.USE_FPS_OVERLAY:
            self.overlay.process_logic()

    def process_all_draw(self) -> None:
        self.screen.fill(Color.BLACK)
        self.scenes[self.current_scene_index].process_draw()
        if self.USE_FPS_OVERLAY:
            self.overlay.process_draw()
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
