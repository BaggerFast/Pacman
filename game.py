import os
import json
import pygame as pg
from misc import Color, ROOT_DIR, HighScore, \
                 create_file_if_not_exist, get_image_path, Score
from scenes import LevelsScene, GameScene, GameoverScene, MenuScene, PauseScene, RecordsScene, CreditsScene


class Game:
    __size = width, height = 224, 285
    current_scene_name = 'SCENE_MENU'
    __last_level_filepath = os.path.join(ROOT_DIR, "saves", "cur_level.json")
    pg.display.set_caption('PACMAN')
    __icon = pg.image.load(get_image_path('1', 'pacman', 'walk'))
    pg.display.set_icon(__icon)

    def __init__(self) -> None:
        self.level_name = self.__read_last_level()
        self.screen = pg.display.set_mode(self.__size, pg.SCALED)
        self.score = Score()
        self.records = HighScore(self)
        self.__delay = 15
        self.scenes = {
            "SCENE_PAUSE": PauseScene(self),
            "SCENE_MENU": MenuScene(self),
            "SCENE_GAME": GameScene(self),
            "SCENE_GAMEOVER": GameoverScene(self),
            "SCENE_LEVELS": LevelsScene(self),
            "SCENE_RECORDS": RecordsScene(self),
            "SCENE_CREDITS": CreditsScene(self),
        }

        self.__game_over = False

    @staticmethod
    def __exit_button_pressed(event: pg.event.Event) -> bool:
        return event.type == pg.QUIT

    @staticmethod
    def __exit_hotkey_pressed(event: pg.event.Event) -> bool:
        return event.type == pg.KEYDOWN and event.mod & pg.KMOD_CTRL and event.key == pg.K_q

    def __process_exit_events(self, event: pg.event.Event) -> None:
        if Game.__exit_button_pressed(event) or Game.__exit_hotkey_pressed(event):
            self.__exit_game()

    def __process_all_events(self) -> None:
        for event in pg.event.get():
            self.__process_exit_events(event)
            self.scenes[self.current_scene_name].process_event(event)

    def __process_all_logic(self) -> None:
        self.scenes[self.current_scene_name].process_logic()

    def __process_all_draw(self) -> None:
        self.screen.fill(Color.BLACK)
        self.scenes[self.current_scene_name].process_draw()
        pg.display.flip()

    def main_loop(self) -> None:
        while not self.__game_over:
            self.__process_all_events()
            self.__process_all_logic()
            self.__process_all_draw()
            pg.time.wait(self.__delay)

    def set_scene(self, name: str, reset: bool = False) -> None:
        """
        :param name: name of NEXT scene
        :param reset: if reset == True will call on_reset() of NEXT scene (see BaseScene)
        IMPORTANT: it calls on_deactivate() on CURRENT scene and on_activate() on NEXT scene
        """
        self.scenes[self.current_scene_name].on_deactivate()
        self.current_scene_name = name
        if reset:
            self.scenes[self.current_scene_name].on_reset()
        self.scenes[self.current_scene_name].on_activate()

    def __save_last_level(self):
        string = json.dumps({f"level_name": f"{self.level_name}"})
        with open(self.__last_level_filepath, "w") as file:
            file.write(string)

    def __read_last_level(self) -> str:
        create_file_if_not_exist(self.__last_level_filepath, json.dumps({"level_name": "level_1"}))
        with open(self.__last_level_filepath, "r") as file:
            return json.load(file)["level_name"]

    def __exit_game(self) -> None:
        print('Bye bye')
        self.__game_over = True

    def __del__(self):
        self.__save_last_level()
