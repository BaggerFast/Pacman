import pygame as pg
from misc import Color, HighScore, get_path, Score, UNLOCK_LEVELS, List, get_list_path, UNLOCK_SKINS, FRUITS_COUNT
from misc.storage import Storage
from scenes import *


class Game:
    class Scenes:
        def __init__(self, game):
            self.PAUSE = pause.Scene(game)
            self.MENU = menu.Scene(game)
            self.MAIN = main.Scene(game)
            self.GAMEOVER = gameover.Scene(game)
            self.LEVELS = levels.Scene(game)
            self.RECORDS = records.Scene(game)
            self.CREDITS = credits.Scene(game)
            self.ENDGAME = endgame.Scene(game)
            self.__current = None

        @property
        def current(self):
            return self.__current

        def set(self, scene: base.Scene, reset: bool = False) -> None:
            """
            :param scene: NEXT scene (contains in game.scenes.*)
            :param reset: if reset == True will call on_reset() of NEXT scene (see Base.Scene)

            IMPORTANT: it calls on_deactivate() on CURRENT scene and on_activate() on NEXT scene
            """
            if self.__current is not None:
                self.__current.on_deactivate()
            self.__current = scene
            if reset:
                self.__current.on_reset()
            self.__current.on_activate()

    class Maps:
        def __init__(self):
            self.levels = []
            self.count = 0
            self.read_levels()

        @staticmethod
        def level_name(level_id: int = 0):
            return f"level_{level_id + 1}"

        def keys(self) -> List[int]:
            return [i for i in range(self.count)]

        def read_levels(self):
            self.levels = get_list_path("json", "maps")
            self.count = len(self.levels)

    __size = width, height = 224, 285
    __icon = pg.image.load(get_path('1', 'png', 'images', 'pacman', 'default', 'walk'))
    __FPS = 60
    __def_level_id = 0
    __def_skin = "default"
    __all_skins = ["default", "chrome", "half_life"]
    pg.display.set_caption('PACMAN')
    pg.display.set_icon(__icon)

    def __init__(self) -> None:
        self.maps = self.Maps()

        self.__storage = Storage()
        self.unlocked_levels = self.maps.keys() if UNLOCK_LEVELS else self.__storage.unlocked_levels
        self.level_id = int(self.__storage.last_level_id) if int(
            self.__storage.last_level_id) in self.unlocked_levels else self.__def_level_id
        self.unlocked_skins = self.__all_skins if UNLOCK_SKINS else self.__storage.unlocked_levels
        self.skin = self.__storage.last_skin if self.__storage.last_skin in self.unlocked_skins else self.__def_skin
        self.eaten_fruits = self.__storage.eaten_fruits

        self.screen = pg.display.set_mode(self.__size, pg.SCALED)
        self.score = Score()
        self.records = HighScore(self)
        self.scenes = self.Scenes(self)
        self.__clock = pg.time.Clock()
        self.__game_over = False
        self.time_out = 125
        self.animate_timer = 0
        self.scenes.set(self.scenes.MENU)

    @property
    def current_scene(self):
        return self.scenes.current

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
            self.scenes.current.process_event(event)

    def __process_all_logic(self) -> None:
        self.scenes.current.process_logic()

    def __process_all_draw(self) -> None:
        self.screen.fill(Color.BLACK)
        self.scenes.current.process_draw()
        pg.display.flip()

    def main_loop(self) -> None:
        while not self.__game_over:
            self.__process_all_events()
            self.__process_all_logic()
            self.__process_all_draw()
            self.__clock.tick(self.__FPS)

    def exit_game(self) -> None:
        print('Bye bye')
        self.__storage.last_level_id = self.level_id
        self.__storage.last_skin = self.skin
        self.__storage.eaten_fruits = self.eaten_fruits
        if not UNLOCK_LEVELS:
            self.__storage.unlocked_levels = self.unlocked_levels
        if not UNLOCK_SKINS:
            self.__storage.unlocked_skins = self.unlocked_skins
        self.__game_over = True

    def unlock_level(self, level_id: int = 0) -> None:
        """
        :param level_id: level id
        """
        if level_id in self.maps.keys():
            if not UNLOCK_LEVELS and level_id not in self.unlocked_levels:
                self.unlocked_levels.append(level_id)
        else:
            raise Exception(f"id error. Map id: {level_id} doesn't exist")

    def unlock_skin(self, skin_name: str = 0) -> None:
        """
        :param skin_name: skin name
        """
        if skin_name in self.__all_skins:
            if not UNLOCK_SKINS and skin_name not in self.unlocked_skins:
                self.unlocked_skins.append(skin_name)
        else:
            raise Exception(f"Name error. Skin name: {skin_name} doesn't exist")

    def store_fruit(self, fruit_id: int = 0, value: int = 0) -> None:
        """
        :param fruit_id: fruit id
        :param value: count of fruits
        """
        if fruit_id in range(FRUITS_COUNT):
            self.eaten_fruits[fruit_id] = value
        else:
            raise Exception(f"id error. Fruit id: {fruit_id} doesn't exist")
