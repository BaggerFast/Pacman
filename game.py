import os
import json
import pygame as pg
from misc.constants import Color, ROOT_DIR, MAPS_COUNT
from misc.highscore import HighScore
from misc.path import create_file_if_not_exist
from misc.score import Score
from scenes.levels import LevelsScene
from scenes.main import GameScene
from scenes.menu import MenuScene
from scenes.pause import PauseScene
from scenes.records import RecordsScene
from scenes.credits import CreditsScene


class Game:
    size = width, height = 224, 285
    current_scene_name = 'SCENE_MENU'
    last_level_filepath = os.path.join(ROOT_DIR, "saves", "cur_level.json")

    def __init__(self) -> None:
        """
        Dict names:
            SCENE_PAUSE: PauseScene
            SCENE_MENU: MenuScene
            SCENE_GAME: GameScene
            SCENE_LEVELS: LevelsScene
            SCENE_RECORDS: RecordsScene
            SCENE_CREDITS: TitersScene
        """

        self.level_name = self.read_last_level()
        self.levels_count = MAPS_COUNT
        self.screen = pg.display.set_mode(self.size, pg.SCALED)
        self.score = Score()
        self.records = HighScore(self)
        self.delay = 15
        self.scenes = {
            "SCENE_PAUSE": PauseScene(self),
            "SCENE_MENU": MenuScene(self),
            "SCENE_GAME": GameScene(self),
            "SCENE_LEVELS": LevelsScene(self),
            "SCENE_RECORDS": RecordsScene(self),
            "SCENE_CREDITS": CreditsScene(self),
        }

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
        for scene in self.scenes.values():
            scene.on_window_resize()

    def process_resize_event(self, event: pg.event.Event) -> None:
        if event.type != pg.VIDEORESIZE:
            return
        self.SIZE = self.WIDTH, self.HEIGHT = event.w, event.h
        self.screen = pg.display.set_mode(self.SIZE, pg.RESIZABLE)
        self.resize_scenes()

    def process_all_events(self) -> None:
        for event in pg.event.get():
            self.process_exit_events(event)
            self.process_resize_event(event)
            self.scenes[self.current_scene_name].process_event(event)

    def process_all_logic(self) -> None:
        self.scenes[self.current_scene_name].process_logic()

    def process_all_draw(self) -> None:
        self.screen.fill(Color.BLACK)
        self.scenes[self.current_scene_name].process_draw()
        pg.display.flip()

    def main_loop(self) -> None:
        while not self.game_over:
            self.process_all_events()
            self.process_all_logic()
            self.process_all_draw()
            pg.time.wait(self.delay)

    def set_scene(self, name: str, resume: bool = False) -> None:
        """
        Dict names:
            SCENE_PAUSE: PauseScene
            SCENE_MENU: MenuScene
            SCENE_GAME: GameScene
            SCENE_LEVELS: LevelsScene
            SCENE_RECORDS: RecordsScene
            SCENE_CREDITS: TitersScene
        """
        if not resume:
            self.scenes[self.current_scene_name].on_deactivate()
        self.current_scene_name = name
        if not resume:
            self.scenes[self.current_scene_name].on_activate()

    def save_last_level(self):
        string = json.dumps({f"level_name": f"{self.level_name}"})
        with open(self.last_level_filepath, "w") as file:
            file.write(string)

    def read_last_level(self) -> str:
        create_file_if_not_exist(self.last_level_filepath, json.dumps({"level_name": "level_1"}))
        with open(self.last_level_filepath, "r") as file:
            return json.load(file)["level_name"]

    def exit_game(self) -> None:
        print('Bye bye')
        self.game_over = True

    def __del__(self):
        self.save_last_level()
