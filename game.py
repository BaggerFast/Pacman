import pygame as pg
from misc import Color, HighScore, get_image_path, Score
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

    __size = width, height = 224, 285
    __icon = pg.image.load(get_image_path('1', 'pacman', 'walk'))
    __FPS = 60
    pg.display.set_caption('PACMAN')
    pg.display.set_icon(__icon)

    def __init__(self) -> None:
        self.__storage = Storage()
        self.level_name = self.__storage.last_level
        self.screen = pg.display.set_mode(self.__size, pg.SCALED)
        self.score = Score()
        self.records = HighScore(self)
        self.scenes = self.Scenes(self)
        self.__current_scene = self.scenes.MENU
        self.__clock = pg.time.Clock()
        self.__game_over = False

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

    def set_scene(self, scene: base.Scene, reset: bool = False) -> None:
        """
        :param scene: NEXT scene (contains in game.scenes.*)
        :param reset: if reset == True will call on_reset() of NEXT scene (see Base.Scene)

        IMPORTANT: it calls on_deactivate() on CURRENT scene and on_activate() on NEXT scene
        """
        self.__current_scene.on_deactivate()
        self.__current_scene = scene
        if reset:
            self.__current_scene.on_reset()
        self.__current_scene.on_activate()

    def exit_game(self) -> None:
        print('Bye bye')
        self.__storage.last_level = self.level_name
        self.__storage.save()
        self.__game_over = True
