import os
import json
import pygame as pg
from misc import Color, ROOT_DIR, HighScore, \
                 create_file_if_not_exist, get_image_path, Score
from scenes import LevelsScene, GameScene, GameoverScene, MenuScene, PauseScene, RecordsScene, CreditsScene, BaseScene


class Scenes:
    def __init__(self, game):
        self.SCENE_PAUSE = PauseScene(game)
        self.SCENE_MENU = MenuScene(game)
        self.SCENE_GAME = GameScene(game)
        self.SCENE_GAMEOVER = GameoverScene(game)
        self.SCENE_LEVELS = LevelsScene(game)
        self.SCENE_RECORDS = RecordsScene(game)
        self.SCENE_CREDITS = CreditsScene(game)


class Game:
    __size = width, height = 224, 285
    __last_level_filepath = os.path.join(ROOT_DIR, "saves", "cur_level.json")
    __icon = pg.image.load(get_image_path('1', 'pacman', 'walk'))
    __FPS = 60
    pg.display.set_caption('PACMAN')
    pg.display.set_icon(__icon)

    def __init__(self) -> None:
        self.level_name = self.__read_last_level()
        self.screen = pg.display.set_mode(self.__size, pg.SCALED)
        self.score = Score()
        self.records = HighScore(self)
        self.__scenes = Scenes(self)
        self.__current_scene = self.__scenes.SCENE_MENU
        self.__clock = pg.time.Clock()
        self.__game_over = False

    @property
    def scenes(self):
        return self.__scenes

    @property
    def current_scene(self):
        return self.__current_scene

    @staticmethod
    def __exit_button_pressed(event: pg.event.Event) -> bool:
        return event.type == pg.QUIT

    @staticmethod
    def __exit_hotkey_pressed(event: pg.event.Event) -> bool:
        return event.type == pg.KEYDOWN and event.mod & pg.KMOD_CTRL and event.key == pg.K_q

    def __process_exit_events(self, event: pg.event.Event) -> None:
        if Game.__exit_button_pressed(event) or Game.__exit_hotkey_pressed(event):
            self.exit_game()

    def __process_all_events(self) -> None:
        for event in pg.event.get():
            self.__process_exit_events(event)
            self.__current_scene.process_event(event)

    def __process_all_logic(self) -> None:
        self.__current_scene.process_logic()

    def __process_all_draw(self) -> None:
        self.screen.fill(Color.BLACK)
        self.__current_scene.process_draw()
        pg.display.flip()

    def main_loop(self) -> None:
        while not self.__game_over:
            self.__process_all_events()
            self.__process_all_logic()
            self.__process_all_draw()
            self.__clock.tick(self.__FPS)

    def set_scene(self, scene: BaseScene, reset: bool = False) -> None:
        """
        :param scene: NEXT scene (contains in game.scenes.*)
        :param reset: if reset == True will call on_reset() of NEXT scene (see BaseScene)

        IMPORTANT: it calls on_deactivate() on CURRENT scene and on_activate() on NEXT scene
        """
        self.__current_scene.on_deactivate()
        self.__current_scene = scene
        if reset:
            self.__current_scene.on_reset()
        self.__current_scene.on_activate()

    def __save_last_level(self) -> None:
        string = json.dumps({f"level_name": f"{self.level_name}"})
        with open(self.__last_level_filepath, "w") as file:
            file.write(string)

    def __read_last_level(self) -> str:
        create_file_if_not_exist(self.__last_level_filepath, json.dumps({"level_name": "level_1"}))
        with open(self.__last_level_filepath, "r") as file:
            return json.load(file)["level_name"]

    def exit_game(self) -> None:
        print('Bye bye')
        self.__save_last_level()
        self.__game_over = True
