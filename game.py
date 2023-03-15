from random import choice
from typing import List

import pygame as pg
from PIL import Image, ImageFilter

from data_core import Colors
from misc import Sounds
from misc.sound_controller import SoundController
from misc import (
    HighScore,
    Score,
    UNLOCK_LEVELS,
    get_list_path,
    UNLOCK_SKINS,
    FRUITS_COUNT,
    LevelLoader,
    Skins,
    Storage,
)
from objects import Map
from scenes import *


class Game:
    class Settings:
        def __init__(self, storage):
            self.MUTE = storage.settings.MUTE
            self.FUN = storage.settings.FUN
            self.VOLUME = storage.settings.VOLUME
            self.DIFFICULTY = storage.settings.DIFFICULTY

    class Music:
        def __init__(self, game):
            self.click = SoundController(game, sound_path=Sounds.CLICK)
            self.siren = SoundController(game, channel=3, sound_path=choice(Sounds.SIREN))
            self.fruit = SoundController(game, channel=4, sound_path=Sounds.FRUIT)
            self.ghost = SoundController(game, channel=4, sound_path=Sounds.GHOST)
            self.pellet = SoundController(game, channel=6, sound_path=Sounds.PELLET)
            self.menu = SoundController(game, channel=4, sound_path=Sounds.INTERMISSION)

            if game.settings.FUN:
                self.pacman = SoundController(game, sound_path=choice(Sounds.DEAD))
                self.seed = SoundController(game, channel=4, sound_path=Sounds.SEED_FUN)
                self.intro = SoundController(game, channel=1, sound_path=choice(Sounds.INTRO))
                self.gameover = SoundController(game, channel=2, sound_path=choice(Sounds.GAME_OVER))
            else:
                self.pacman = SoundController(game, sound_path=Sounds.DEAD[0])
                self.seed = SoundController(game, channel=4, sound_path=Sounds.SEED)
                self.intro = SoundController(
                    game,
                    channel=1,
                    sound_path=Sounds.INTRO[0] if not game.skins.current == game.skins.pokeball else Sounds.POC_INTRO,
                )
                self.gameover = SoundController(game, channel=2, sound_path=Sounds.GAME_OVER[0])

        def reload_sounds(self, game):
            self.siren = SoundController(game, channel=3, sound_path=choice(Sounds.SIREN))
            if game.settings.FUN:
                self.pacman = SoundController(game, sound_path=choice(Sounds.DEAD))
                self.seed = SoundController(game, channel=4, sound_path=Sounds.SEED_FUN)
                self.intro = SoundController(game, channel=1, sound_path=choice(Sounds.INTRO))
                self.gameover = SoundController(game, channel=2, sound_path=choice(Sounds.GAME_OVER))
            else:
                self.pacman = SoundController(game, sound_path=Sounds.DEAD[0])
                self.seed = SoundController(game, channel=4, sound_path=Sounds.SEED)
                self.intro = SoundController(
                    game,
                    channel=1,
                    sound_path=Sounds.INTRO[0] if not game.skins.current == game.skins.pokeball else Sounds.POC_INTRO,
                )
                self.gameover = SoundController(game, channel=2, sound_path=Sounds.GAME_OVER[0])

    class Scenes:
        def __init__(self, game):
            self.PAUSE = pause.Scene(game)
            self.MENU = menu.Scene(game)
            self.MAIN = main.Scene(game)
            self.GAMEOVER = gameover.Scene(game)
            self.LEVELS = levels.Scene(game)
            self.RECORDS = records.Scene(game)
            self.ENDGAME = endgame.Scene(game)
            self.SKINS = skins.Scene(game)
            self.SETTINGS = settings.Scene(game)
            self.__current = None

        @property
        def current(self):
            return self.__current

        def set(self, scene: base.Scene, reset: bool = False, surface: bool = False) -> None:
            scene.prev_scene = self.__current
            if self.__current is not None and not surface:
                self.__current.on_deactivate()
            self.__current = scene
            if reset:
                self.__current.on_reset()
            self.__current.on_activate()

    class Maps:
        def __init__(self, game):
            self.game = game
            self.levels = []
            self.count = 0
            self.cur_id = 0
            self.read_levels()
            self.__images = self.prerender_surfaces()

        @property
        def images(self):
            return self.__images

        @property
        def full_surface(self):
            self.__load_from_map(self.cur_id)
            return self.__map.prerender_map_surface()

        @staticmethod
        def level_name(level_id: int = 0):
            return f"level_{level_id + 1}"

        def __load_from_map(self, level_id: int = 0) -> None:
            self.__loader = LevelLoader(self.levels[level_id])
            self.__map_data = self.__loader.get_map_data()
            self.__map = Map(self.game, self.__map_data)

        def keys(self) -> List[int]:
            return [i for i in range(self.count)]

        def read_levels(self) -> None:
            self.levels = get_list_path("json", "maps")
            self.count = len(self.levels)

        def prerender_surfaces(self) -> List[pg.Surface]:
            images = []
            for level_id in range(self.count):
                self.__load_from_map(level_id)
                image = self.__map.prerender_map_image_scaled()
                images.append(image)
            return images

    __size = width, height = 224, 285

    __FPS = 60
    __def_level_id = 0
    __def_skin = "default"

    def __init__(self) -> None:
        self.__game_over = False
        self.maps = self.Maps(self)
        self.screen = pg.display.set_mode(self.__size, pg.SCALED)
        self.__clock = pg.time.Clock()
        self.timer = pg.time.get_ticks() / 1000
        self.time_out = 125
        self.animate_timer = 0
        self.skins = Skins(self)
        self.score = Score()

        self.read_from_storage()
        self.settings = self.Settings(self.__storage)

        self.sounds = self.Music(self)

        self.skins.current = (
            self.__storage.last_skin if self.__storage.last_skin in self.unlocked_skins else self.__def_skin
        )
        self.records = HighScore(self)
        self.scenes = self.Scenes(self)
        self.scenes.set(self.scenes.MENU)

    def read_from_storage(self):
        self.__storage = Storage(self)
        self.unlocked_levels = self.maps.keys() if UNLOCK_LEVELS else self.__storage.unlocked_levels
        self.maps.cur_id = (
            int(self.__storage.last_level_id)
            if int(self.__storage.last_level_id) in self.unlocked_levels
            else self.__def_level_id
        )
        self.unlocked_skins = self.skins.all_skins if UNLOCK_SKINS else self.__storage.unlocked_skins
        self.eaten_fruits = self.__storage.eaten_fruits
        self.highscores = self.__storage.highscores

    def save_to_storage(self):
        self.__storage.settings.MUTE = self.settings.MUTE
        self.__storage.settings.FUN = self.settings.FUN
        self.__storage.settings.VOLUME = self.settings.VOLUME
        self.__storage.settings.DIFFICULTY = self.settings.DIFFICULTY
        self.__storage.last_level_id = self.maps.cur_id
        self.__storage.last_skin = self.skins.current.name
        self.__storage.eaten_fruits = self.eaten_fruits
        if not UNLOCK_LEVELS:
            self.__storage.unlocked_levels = self.unlocked_levels
        if not UNLOCK_SKINS:
            self.__storage.unlocked_skins = self.unlocked_skins
        self.__storage.highscores = self.highscores
        self.__storage.save()

    @property
    def current_scene(self):
        return self.scenes.current

    @property
    def size(self):
        return self.__size

    # region Exit

    @staticmethod
    def __exit_hotkey_pressed(event: pg.event.Event) -> bool:
        return event.type == pg.KEYDOWN and event.mod & pg.KMOD_CTRL and event.key == pg.K_q

    def __process_exit_events(self, event: pg.event.Event) -> None:
        if event.type == pg.QUIT or Game.__exit_hotkey_pressed(event):
            self.exit_game()

    def exit_game(self) -> None:
        self.save_to_storage()
        self.__game_over = True
        print("Bye bye")

    # endregion

    # region Game Loop

    def __process_all_events(self) -> None:
        for event in pg.event.get():
            self.__process_exit_events(event)
            self.scenes.current.process_event(event)

    def __process_all_logic(self) -> None:
        self.scenes.current.process_logic()

    def __process_all_draw(self) -> None:
        exceptions = [self.scenes.PAUSE, self.scenes.GAMEOVER, self.scenes.ENDGAME]
        if self.scenes.current not in exceptions:
            self.screen.fill(Colors.BLACK)
        else:
            blur_count = 10
            current_time = pg.time.get_ticks() / 1000
            surify = pg.image.tostring(self.scenes.MAIN.template, "RGBA")
            impil = Image.frombytes("RGBA", self.__size, surify)
            piler = impil.filter(
                ImageFilter.GaussianBlur(radius=min((current_time - self.timer) * blur_count * 2, blur_count))
            )
            surface = pg.image.fromstring(piler.tobytes(), piler.size, piler.mode).convert()
            self.screen.blit(surface, (0, 0))
        self.scenes.current.process_draw()
        pg.display.flip()

    def main_loop(self) -> None:
        while not self.__game_over:
            self.__process_all_events()
            self.__process_all_logic()
            self.__process_all_draw()
            self.__clock.tick(self.__FPS)

    # endregion

    def unlock_level(self, level_id: int = 0) -> None:
        if level_id in self.maps.keys():
            if not UNLOCK_LEVELS and level_id not in self.unlocked_levels:
                self.unlocked_levels.append(level_id)
        else:
            raise Exception(f"id error. Map id: {level_id} doesn't exist")

    def unlock_skin(self, skin_name: str = 0) -> None:
        if skin_name in self.skins.all_skins:
            if not UNLOCK_SKINS and skin_name not in self.unlocked_skins:
                self.unlocked_skins.append(skin_name)
        else:
            raise Exception(f"Name error. Skin name: {skin_name} doesn't exist")

    def store_fruit(self, fruit_id: int = 0, value: int = 0) -> None:
        if fruit_id in range(FRUITS_COUNT):
            self.eaten_fruits[fruit_id] += value
        else:
            raise Exception(f"id error. Fruit id: {fruit_id} doesn't exist")
