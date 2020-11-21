import pygame as pg
from misc.constants import Color
from misc.health import Health
from misc.highscore import HighScore
from misc.score import Score
from scenes.main import GameScene
from scenes.menu import MenuScene
from scenes.pause import PauseScene
from scenes.records import RecordsScene
from scenes.titers import TitersScene


class Game:
    size = width, height = 224, 285
    SCENE_MENU = 0
    SCENE_GAME = 1
    SCENE_PAUSE = 2
    SCENE_RECORDS = 3
    current_scene_index = SCENE_MENU

    def __init__(self) -> None:
        self.screen = pg.display.set_mode(self.size, pg.SCALED)
        self.lives = Health(lives=3, max_lives=3)
        self.score = Score()
        self.records = HighScore()
        self.delay = 15
        self.clock = pg.time.Clock()
        self.scenes = [
            MenuScene(self),
            GameScene(self),
            PauseScene(self),
            RecordsScene(self),
            TitersScene(self),
        ]

        self.game_over = False

    @staticmethod
    def exit_button_pressed(event: pg.event.Event) -> bool:
        return event.type == pg.QUIT

    @staticmethod
    def exit_hotkey_pressed(event: pg.event.Event) -> bool:
        return event.type == pg.KEYDOWN and event.mod & pg.KMOD_CTRL and event.key == pg.K_q

    def process_exit_events(self, event: pg.event.Event) -> None:
        if Game.exit_button_pressed(event) or Game.exit_hotkey_pressed(event):
            self.exit_game()

    def resize_scenes(self) -> None:
        for scene in self.scenes:
            scene.on_window_resize()

    def process_resize_event(self, event: pg.event.Event) -> None:
        if event.type != pg.VIDEORESIZE:
            return
        self.SIZE = self.WIDTH, self.HEIGHT = event.w, event.h
        self.screen = pg.display.set_mode(self.SIZE, pg.RESIZABLE)
        self.resize_scenes()

    def process_all_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE: self.set_scene(4)
            self.process_exit_events(event)
            self.process_resize_event(event)
            self.scenes[self.current_scene_index].process_event(event)

    def process_all_logic(self) -> None:
        self.scenes[self.current_scene_index].process_logic()

    def process_all_draw(self) -> None:
        self.screen.fill(Color.BLACK)
        self.scenes[self.current_scene_index].process_draw()
        pg.display.flip()

    def main_loop(self) -> None:
        while not self.game_over:
            self.process_all_events()
            self.process_all_logic()
            self.process_all_draw()
            pg.time.wait(self.delay)

    def set_scene(self, index: int, resume: bool = False) -> None:
        if not resume:
            self.scenes[self.current_scene_index].on_deactivate()
        self.current_scene_index = index
        if not resume:
            self.scenes[self.current_scene_index].on_activate()

    def exit_game(self) -> None:
        print('Bye bye')
        self.game_over = True
