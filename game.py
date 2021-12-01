import sys
from random import choice
from typing import List

import pygame as pg
from PIL import Image, ImageFilter
from misc import Sounds, ControlCheats
from misc.cheat_codes import Cheat
from misc.constants.skin_names import SkinsNames
from misc.sound_controller import SoundController
from misc import Color, HighScore, get_path, get_list_path, LevelLoader, Skins, Storage
from misc.constants.variables import *
from objects.map import rand_color, Map
from scenes import *
from scenes.base import BaseScene


class Game:
    map_color = rand_color()

    class Cheats:
        def __init__(self, game):
            self.UNLOCK_SKINS = UNLOCK_SKINS
            self.UNLOCK_LEVELS = UNLOCK_LEVELS
            self.INFINITY_LIVES = INFINITY_LIVES
            self.GHOSTS_COLLISION = GHOSTS_COLLISION
            self.cheat_storage = {
                'UNLOCK_SKINS': lambda: self.unlock_skins(),
                'UNLOCK_LEVELS': lambda: self.unlock_levels()
            }
            self.game: Game = game

        def unlock_skins(self):
            self.game.unlocked_skins = self.game.skins.all_skins if self.game.cheats_var.UNLOCK_SKINS else self.game.storage.unlocked_skins
            if self.game.scenes.current == self.game.scenes.SKINS:
                self.game.scenes.current.create_objects()

        def unlock_levels(self):
            self.game.unlocked_levels = self.game.maps.keys() if self.game.cheats_var.UNLOCK_LEVELS else self.game.storage.unlocked_levels
            if self.game.scenes.current == self.game.scenes.LEVELS:
                self.game.scenes.current.create_objects()

        def update(self, key_code):
            if hasattr(self, key_code):
                setattr(self, key_code, not getattr(self, key_code))
            if key_code in self.cheat_storage:
                self.cheat_storage[key_code]()

    class Settings:
        def __init__(self, storage):
            self.SOUND = storage.settings.SOUND
            self.FUN = storage.settings.FUN
            self.VOLUME = storage.settings.VOLUME
            self.DIFFICULTY = storage.settings.DIFFICULTY

        def change_volume(self, num: int):
            self.VOLUME = max(self.VOLUME + num, 0)
            self.VOLUME = min(self.VOLUME, 100)

    class Music:
        def __init__(self, game):
            self.game = game
            self.reload_sounds()

        def base_preset(self):
            self.click = SoundController(self.game, Sounds.Ch.menu, Sounds.CLICK)
            self.menu = SoundController(self.game, Sounds.Ch.menu, Sounds.INTERMISSION)
            self.credits = SoundController(self.game, Sounds.Ch.menu, choice(Sounds.CREDITS))
            self.siren = SoundController(self.game, Sounds.Ch.siren, choice(Sounds.SIREN))
            self.pellet = SoundController(self.game, Sounds.Ch.pellet, Sounds.PELLET)
            self.ghost = SoundController(self.game, Sounds.Ch.ghost, Sounds.GHOST)
            self.fruit = SoundController(self.game, Sounds.Ch.fruit, Sounds.FRUIT)
            self.cheat = SoundController(self.game, Sounds.Ch.menu, Sounds.CHEAT)

        def preset_for_fun(self):
            if self.fun:
                self.pacman = SoundController(self.game, Sounds.Ch.pacman,
                                              choice([path for path in Sounds.DEAD[1:]]))
                self.seed = SoundController(self.game, Sounds.Ch.seed, Sounds.SEED_FUN)
                self.intro = SoundController(self.game, Sounds.Ch.intro,
                                             choice([path for path in Sounds.INTRO[1:]]))
                self.gameover = SoundController(self.game, Sounds.Ch.game_over,
                                                choice([path for path in Sounds.GAMEOVER[1:]]))
            else:
                self.pacman = SoundController(self.game, Sounds.Ch.pacman, Sounds.DEAD[0])
                self.gameover = SoundController(self.game, Sounds.Ch.game_over, Sounds.GAMEOVER[0])
                self.seed = SoundController(self.game, Sounds.Ch.seed, Sounds.SEED)
                self.intro = SoundController(self.game, Sounds.Ch.intro, Sounds.INTRO[0])

        def reload_sounds(self):
            self.fun = self.game.settings.FUN
            self.preset_for_fun()
            self.base_preset()
            if self.fun:
                return
            self.game.skins.current.sound_preset()

    class Scenes:
        def __init__(self, game):
            self.PAUSE = PauseScene(game)
            self.MENU = MenuScene(game)
            self.MAIN = MainScene(game)
            self.GAMEOVER = GameOverScene(game, 0)
            self.LEVELS = LevelsScene(game)
            self.RECORDS = RecordsScene(game)
            self.CREDITS = CreditsScene(game)
            self.ENDGAME = EndScene(game, 0)
            self.SKINS = SkinsScene(game)
            self.SETTINGS = SettingsScene(game)
            self.__game = game
            self.__current = None

        @property
        def current(self):
            return self.__current

        def set(self, scene: BaseScene, reset: bool = False) -> None:
            """
            :param scene: NEXT scene (contains in game.scenes.*)
            :param reset: if reset == True will call on_reset() of NEXT scene (see Base.Scene)
            :param loading: displays "Loading..." until scene will be loaded
            IMPORTANT: it calls on_deactivate() on CURRENT scene and on_activate() on NEXT scene
            """
            if scene != self.MENU:
                self.__game.scenes.MENU.first_run = False
            scene.prev_scene = self.__current
            if self.__current is not None:
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
            self.__images = list(self.prerender_surfaces())

        @property
        def images(self):
            return self.__images

        @property
        def full_surface(self):
            self.__load_from_map(self.cur_id)
            return self.__map.prerender_map_surface()

        @property
        def level_name(self):
            return f'level {self.cur_id + 1}'

        def __load_from_map(self, level_id: int = 0) -> None:
            self.__loader = LevelLoader(self.levels[level_id])
            self.__map_data = self.__loader.get_map_data()
            self.__map = Map(self.game, self.__map_data)

        def keys(self) -> List[int]:
            return [i for i in range(self.count)]

        def read_levels(self) -> None:
            self.levels = get_list_path("maps", ext='json')
            self.count = len(self.levels)

        def prerender_surfaces(self):
            for level_id in range(self.count):
                self.__load_from_map(level_id)
                yield self.__map.prerender_map_image_scaled()

    __resolution = width, height = 224, 285
    __FPS: int = 60
    __def_level_id = 0

    pg.display.set_caption('PACMAN')
    pg.display.set_icon(pg.transform.scale(pg.image.load(get_path('images/ico.png')), (256, 256)))

    def __init__(self) -> None:
        self.maps = self.Maps(self)
        self.screen = pg.display.set_mode(self.__resolution, pg.SCALED)
        self.__clock = pg.time.Clock()
        self.__game_over: bool = False
        self.timer = pg.time.get_ticks() / 1000
        self.time_out: int = 125
        self.animate_timer: int = 0
        self.pred: bool = False

        self.skins = Skins(self)

        self.cheats_var = self.Cheats(self)
        Sounds.load_sounds()
        self.read_from_storage()

        self.cheats = ControlCheats(
            [
                Cheat(self, 'skins', lambda: self.cheats_var.update("UNLOCK_SKINS")),
                Cheat(self, 'maps', lambda: self.cheats_var.update("UNLOCK_LEVELS")),
                Cheat(self, 'lives', lambda: self.cheats_var.update("INFINITY_LIVES")),
                Cheat(self, 'collision', lambda: self.cheats_var.update("GHOSTS_COLLISION"))
            ], self
        )

        self.sounds = self.Music(self)
        self.skins.current = self.storage.last_skin if self.storage.last_skin in self.unlocked_skins else SkinsNames.default
        self.records = HighScore(self)
        self.scenes = self.Scenes(self)
        self.scenes.set(self.scenes.MENU)

    def read_from_storage(self):
        self.storage = Storage(self)
        self.settings = self.Settings(self.storage)
        self.unlocked_levels = self.maps.keys() if self.cheats_var.UNLOCK_LEVELS else self.storage.unlocked_levels
        self.maps.cur_id = int(self.storage.last_level_id) if int(
            self.storage.last_level_id) in self.unlocked_levels else self.__def_level_id
        self.unlocked_skins = self.skins.all_skins if self.cheats_var.UNLOCK_SKINS else self.storage.unlocked_skins
        self.eaten_fruits = self.storage.eaten_fruits
        self.highscores = self.storage.highscores

    def save_to_storage(self):
        self.storage.settings.SOUND = self.settings.SOUND
        self.storage.settings.FUN = self.settings.FUN
        self.storage.settings.VOLUME = self.settings.VOLUME
        self.storage.settings.DIFFICULTY = self.settings.DIFFICULTY
        self.storage.last_level_id = self.maps.cur_id
        self.storage.last_skin = self.skins.current.name
        self.storage.eaten_fruits = self.eaten_fruits

        self.storage.unlocked_levels = self.unlocked_levels if not self.cheats_var.UNLOCK_LEVELS else self.storage.unlocked_levels
        self.storage.unlocked_skins = self.unlocked_skins if not self.cheats_var.UNLOCK_SKINS else self.storage.unlocked_skins

        self.storage.highscores = self.highscores
        self.storage.save()

    @property
    def difficulty(self):
        return self.settings.DIFFICULTY + 1

    @property
    def current_scene(self):
        return self.scenes.current

    @property
    def size(self):
        return self.__resolution

    @staticmethod
    def __exit_button_pressed(event: pg.event.Event) -> bool:
        return event.type == pg.QUIT

    @staticmethod
    def __exit_hotkey_pressed(event: pg.event.Event) -> bool:
        return event.type == pg.KEYDOWN and event.mod & pg.KMOD_CTRL and event.key == pg.K_q

    def __process_exit_events(self, event: pg.event.Event) -> None:
        if self.__exit_button_pressed(event) or self.__exit_hotkey_pressed(event):
            self.exit_game()

    def __process_all_events(self) -> None:
        for event in pg.event.get():
            self.cheats.process_event(event)
            self.__process_exit_events(event)
            self.scenes.current.process_event(event)

    def __process_all_logic(self) -> None:
        self.cheats.process_logic()
        self.scenes.current.process_logic()
        if self.current_scene != self.scenes.MAIN:
            for ghost in self.scenes.MAIN.ghosts:
                ghost.timer = pg.time.get_ticks() - (pg.time.get_ticks() - ghost.old_timer)
                ghost.ai_timer = pg.time.get_ticks() - (pg.time.get_ticks() - ghost.old_ai_timer)
        else:
            for ghost in self.scenes.MAIN.ghosts:
                ghost.old_timer = pg.time.get_ticks()
                ghost.old_ai_timer = pg.time.get_ticks()

    def __process_all_draw(self) -> None:
        blur_count = 0
        current_time = pg.time.get_ticks() / 1000

        animations = [self.scenes.MAIN]
        exceptions = [self.scenes.PAUSE, self.scenes.GAMEOVER, self.scenes.ENDGAME]

        blur_count = self.__additional_draw(animations, blur_count, current_time, exceptions)

        if self.scenes.current in animations:
            self.screen.fill(Color.BLACK)

        self.scenes.current.process_draw(blur_count)
        pg.display.flip()

    def __additional_draw(self, animations, blur_count, current_time, exceptions):
        if self.scenes.current not in exceptions and self.scenes.current not in animations and self.scenes.current != self.scenes.MENU:
            self.screen.fill(Color.BLACK)
        elif self.scenes.current in exceptions:
            blur_count = self.__exceptions_draw()
        elif self.scenes.current in animations and not self.pred:
            blur_count = self.__animations_draw(current_time)
        elif self.scenes.current == self.scenes.MENU and self.scenes.MENU.first_run:
            blur_count = self.__predraw_draw(current_time)
        return blur_count

    def __animations_draw(self, current_time):
        blur_count = 10
        coef = (self.timer - current_time) * 2 + blur_count / 3
        blur_count = max(coef, 0)
        return blur_count

    def __predraw_draw(self, current_time):
        blur_count = 10
        self.screen.fill(Color.BLACK)
        coef = (self.timer - current_time) * 2 + blur_count / 3
        blur_count = max(coef, 0)
        if not blur_count:
            self.scenes.MENU.first_run = False
        return blur_count

    def __exceptions_draw(self):
        blur_count = 10
        current_time = pg.time.get_ticks() / 1000
        surify = pg.image.tostring(self.scenes.MAIN.template, 'RGBA')
        impil = Image.frombytes('RGBA', self.__resolution, surify)
        piler = impil.filter(
            ImageFilter.GaussianBlur(radius=min((current_time - self.timer) * blur_count * 2, blur_count)))
        surface = pg.image.fromstring(
            piler.tobytes(), piler.size, piler.mode).convert()
        self.screen.blit(surface, (0, 0))
        blur_count = 0
        return blur_count

    def main_loop(self) -> None:
        while not self.__game_over:
            self.__process_all_events()
            self.__process_all_logic()
            self.__process_all_draw()
            self.__clock.tick(self.__FPS)

    def exit_game(self) -> None:
        self.save_to_storage()
        print('Bye bye')
        sys.exit(0)

    def unlock_level(self, level_id: int = 0) -> None:
        """
        :param level_id: level id
        """
        if level_id in self.maps.keys():
            if not self.cheats_var.UNLOCK_LEVELS and level_id not in self.unlocked_levels:
                self.unlocked_levels.append(level_id)
        else:
            raise Exception(f"id error. Map id: {level_id} doesn't exist")

    def unlock_skin(self, skin_name: str = 0) -> None:
        """
        :param skin_name: skin name
        """
        if skin_name in self.skins.all_skins:
            if not self.cheats_var.UNLOCK_SKINS and skin_name not in self.unlocked_skins:
                self.unlocked_skins.append(skin_name)
        else:
            raise Exception(f"Name error. Skin name: {skin_name} doesn't exist")

    def store_fruit(self, fruit_id: int = 0, value: int = 0) -> None:
        """
        :param fruit_id: fruit id
        :param value: count of fruits
        """
        if fruit_id in range(FRUITS_COUNT):
            self.eaten_fruits[fruit_id] += value
        else:
            raise Exception(f"id error. Fruit id: {fruit_id} doesn't exist")
