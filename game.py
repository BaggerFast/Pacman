from random import choice

import pygame as pg
from PIL import Image, ImageFilter, ImageDraw

from misc import Color, HighScore, get_path, Score, Maps, UNLOCK_LEVELS, Sounds
from misc.SoundController import SoundController
from misc.storage import Storage
from scenes import *


class Game:
    class Settings:
        def __init__(self):
            self.MUTE = False
            self.FUN = False

    class Music:
        def __init__(self, game):
            self.pacman = SoundController(game, sound=Sounds.DEAD)
            self.click = SoundController(game, sound=Sounds.CLICK)
            self.intro = SoundController(game, channel=1, sound=pg.mixer.Sound(choice(Sounds.INTRO)))
            self.gameover = SoundController(game, channel=2, sound=Sounds.GAMEOVER)
            self.siren = SoundController(game, channel=3, sound=Sounds.SIREN)
            self.seed = SoundController(game, channel=4, sound=Sounds.SEED)
            self.fruit = SoundController(game, channel=4, sound=Sounds.FRUIT)


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
            self.SETTINGS = settings.Scene(game)
            self.__current = None

        @property
        def current(self):
            return self.__current

        def set(self, scene: base.Scene, reset: bool = False, surface: bool = False) -> None:
            """
            :param scene: NEXT scene (contains in game.scenes.*)
            :param reset: if reset == True will call on_reset() of NEXT scene (see Base.Scene)
            :param surface: if surface == True background of new scene equal CURRENT scene with BLUR
            IMPORTANT: it calls on_deactivate() on CURRENT scene and on_activate() on NEXT scene
            """
            if self.__current is not None and not surface:
                self.__current.on_deactivate()
            self.__current = scene
            if reset:
                self.__current.on_reset()
            self.__current.on_activate()

    __size = width, height = 224, 285
    __icon = pg.image.load(get_path('1', 'png', 'images', 'pacman', 'walk'))
    __FPS = 60
    __def_level_id = 0
    pg.display.set_caption('PACMAN')
    pg.display.set_icon(__icon)

    def __init__(self) -> None:
        self.__storage = Storage()
        self.unlocked_levels = Maps.keys() if UNLOCK_LEVELS else self.__storage.unlocked_levels
        self.level_id = int(self.__storage.last_level) if int(self.__storage.last_level) in self.unlocked_levels else self.__def_level_id
        self.screen = pg.display.set_mode(self.__size, pg.SCALED)
        self.score = Score()
        self.records = HighScore(self)
        self.settings = self.Settings()
        self.sounds = self.Music(self)
        self.scenes = self.Scenes(self)
        self.__clock = pg.time.Clock()
        self.__game_over = False
        self.timer = pg.time.get_ticks() / 1000
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
        exceptions = [self.scenes.PAUSE, self.scenes.GAMEOVER, self.scenes.ENDGAME]
        if not self.scenes.current in exceptions:
            self.screen.fill(Color.BLACK)
        else:
            blur_count = 10
            current_time = pg.time.get_ticks() / 1000
            surify = pg.image.tostring(self.scenes.MAIN.template, 'RGBA')
            impil = Image.frombytes('RGBA', self.__size, surify)
            piler = impil.filter(ImageFilter.GaussianBlur(radius=min((current_time - self.timer) * blur_count * 2, blur_count)))
            surface = pg.image.fromstring(
                piler.tobytes(), piler.size, piler.mode).convert()
            self.screen.blit(surface, (0, 0))

        self.scenes.current.process_draw()

        pg.display.flip()

    def main_loop(self) -> None:
        while not self.__game_over:
            self.__process_all_events()
            self.__process_all_logic()
            self.__process_all_draw()
            self.__clock.tick(self.__FPS)

    def exit_game(self) -> None:
        self.__storage.last_level = self.level_id
        if not UNLOCK_LEVELS:
            self.__storage.unlocked_levels = self.unlocked_levels
        self.__storage.save()
        self.__game_over = True

    def unlock_level(self, level_id: int = 0) -> None:
        """
        :param level_id:
        """
        if level_id in Maps.keys():
            if not UNLOCK_LEVELS and level_id not in self.unlocked_levels:
                self.unlocked_levels.append(level_id)
        else:
            raise Exception(f"id error. id: {level_id} doesn't exist")
