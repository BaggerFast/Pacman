import sys
from random import choice
from typing import List
import pygame as pg
import scenes
from misc import HighScore, get_list_path, LevelLoader, Storage, ControlCheats
from misc.cheat_codes import Cheat
from misc.constants import Color, FRUITS_COUNT
from misc.constants.classes import Sounds
from misc.constants.skin_names import SkinsNames
from misc.path import bool_venv_var, get_image_path
from misc.skins import Skins
from misc.sound_controller import SoundController
from objects.map import rand_color, Map


class Game:

    pg.display.init()
    pg.font.init()
    pg.mixer.init()

    map_color = rand_color()

    class Cheats:

        class Adapter:

            def __init__(self, active):
                self.active = active

            def __call__(self, *args, **kwargs):
                self.active = not self.active

            def __bool__(self):
                return self.active

        def __init__(self, game):
            self.UNLOCK_SKINS = self.Adapter(bool_venv_var('skins'))
            self.UNLOCK_LEVELS = self.Adapter(bool_venv_var('levels'))
            self.INFINITY_LIVES = self.Adapter(bool_venv_var('lives'))
            self.GHOSTS_COLLISION = self.Adapter(bool_venv_var('collision'))
            self.game: Game = game

        def unlock_skins(self):
            self.game.unlocked_skins = self.game.skins.all_skins if self.game.cheats_var.UNLOCK_SKINS else self.game.storage.unlocked_skins
            if isinstance(self.game.scene_manager.current, scenes.SkinsScene):
                self.game.scene_manager.current.create_objects()

        def unlock_levels(self):
            self.game.unlocked_levels = self.game.maps.keys() if self.game.cheats_var.UNLOCK_LEVELS else self.game.storage.unlocked_levels
            if isinstance(self.game.scene_manager.current, scenes.LevelsScene):
                self.game.scene_manager.current.create_objects()

        def update(self, key_code):
            if hasattr(self, key_code):
                setattr(self, key_code, not getattr(self, key_code))
            # if key_code in self.cheat_storage:
            #     self.cheat_storage[key_code]()

    class Settings:

        def __init__(self, storage):
            self.SOUND = storage.settings.SOUND
            self.FUN = storage.settings.FUN
            self.VOLUME = storage.settings.VOLUME
            self.DIFFICULTY = storage.settings.DIFFICULTY

        def change_volume(self, num: int):
            self.VOLUME = max(self.VOLUME + num, 0)
            self.VOLUME = min(self.VOLUME, 100)

        def change_difficulty(self):
            self.DIFFICULTY = (self.DIFFICULTY + 1) % 3

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
            self.ghost = SoundController(self.game, Sounds.Ch.eatable, Sounds.GHOST)
            self.fruit = SoundController(self.game, Sounds.Ch.eatable, Sounds.FRUIT)
            self.cheat = SoundController(self.game, Sounds.Ch.menu, Sounds.CHEAT)

        def preset_for_fun(self):
            if self.fun:
                self.pacman = SoundController(self.game, Sounds.Ch.pacman,
                                              choice([path for path in Sounds.DEAD[1:]]))
                self.seed = SoundController(self.game, Sounds.Ch.eatable, Sounds.SEED_FUN)
                self.intro = SoundController(self.game, Sounds.Ch.intro,
                                             choice([path for path in Sounds.INTRO[1:]]))
                self.gameover = SoundController(self.game, Sounds.Ch.game_over,
                                                choice([path for path in Sounds.GAMEOVER[1:]]))
            else:
                self.pacman = SoundController(self.game, Sounds.Ch.pacman, Sounds.DEAD[0])
                self.gameover = SoundController(self.game, Sounds.Ch.game_over, Sounds.GAMEOVER[0])
                self.seed = SoundController(self.game, Sounds.Ch.eatable, Sounds.SEED)
                self.intro = SoundController(self.game, Sounds.Ch.intro, Sounds.INTRO[0])

        def reload_sounds(self):
            self.fun = self.game.settings.FUN
            self.preset_for_fun()
            self.base_preset()
            if self.fun:
                return
            self.game.skins.current.sound_preset()

    class Maps:

        def __init__(self, game):
            self.game = game
            self.cur_id = 0
            self.levels: list = get_list_path("maps", ext='json')
            self.images = list(self.prerender_surfaces())

        def __len__(self):
            return len(self.levels)

        @property
        def full_surface(self):
            self.__load_from_map(self.cur_id)
            return self.__map.prerender_map_surface()

        def is_last_level(self) -> bool:
            return self.cur_id + 1 < len(self)

        @property
        def level_name(self):
            return f'level {self.cur_id + 1}'

        def __load_from_map(self, level_id: int = 0) -> None:
            self.__loader = LevelLoader(self.levels[level_id])
            self.__map_data = self.__loader.get_map_data()
            self.__map = Map(self.game.map_color, self.__map_data)

        def keys(self) -> List[int]:
            return list(range(len(self)))

        def prerender_surfaces(self):
            for level_id in range(len(self.levels)):
                self.__load_from_map(level_id)
                yield self.__map.prerender_map_image_scaled()

    __resolution = width, height = 224, 285
    __FPS: int = 60
    __def_level_id = 0
    screen = pg.display.set_mode(__resolution, pg.SCALED)

    pg.display.set_caption('PACMAN')
    pg.display.set_icon(pg.transform.scale(pg.image.load(get_image_path('ico.png')), (256, 256)))

    def __init__(self):
        self.maps = self.Maps(self)
        self.__clock = pg.time.Clock()
        self.time_out: int = 125
        self.animate_timer: int = 0
        self.pred: bool = False
        self.storage = Storage(self)
        self.skins = Skins(self)
        self.cheats_var = self.Cheats(self)
        self.__read_from_storage()

        self.scene_manager = scenes.SceneManager()

        self.__cheats = ControlCheats([
            Cheat(self, 'skins', self.cheats_var.UNLOCK_SKINS),
            Cheat(self, 'maps', self.cheats_var.UNLOCK_LEVELS),
            Cheat(self, 'lives', self.cheats_var.INFINITY_LIVES),
            Cheat(self, 'collision', self.cheats_var.GHOSTS_COLLISION)
        ])

        self.sounds = self.Music(self)

        self.skins.current = self.storage.last_skin if self.storage.last_skin in self.unlocked_skins else SkinsNames.default
        self.records = HighScore(self)

        self.scene_manager.reset(scenes.MenuScene(self))

    def __read_from_storage(self):
        self.settings = self.Settings(self.storage)
        self.unlocked_levels = self.maps.keys() if self.cheats_var.UNLOCK_LEVELS else self.storage.unlocked_levels
        self.maps.cur_id = self.storage.last_level_id if self.storage.last_level_id in self.unlocked_levels else \
            self.__def_level_id
        self.unlocked_skins = self.skins.all_skins if self.cheats_var.UNLOCK_SKINS else self.storage.unlocked_skins
        self.eaten_fruits = self.storage.eaten_fruits
        self.highscores = self.storage.highscores

    @property
    def difficulty(self) -> int:
        return self.settings.DIFFICULTY + 1

    @property
    def current_scene(self) -> scenes.BaseScene:
        return self.scene_manager.current

    @property
    def resolution(self) -> tuple:
        return self.__resolution

    def __process_exit_events(self, event: pg.event.Event) -> None:
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.mod & pg.KMOD_CTRL and event.key == pg.K_q):
            self.exit_game()

    def __process_all_events(self) -> None:
        for event in pg.event.get():
            self.__cheats.process_event(event)
            self.__process_exit_events(event)
            self.scene_manager.process_event(event)

    def __process_all_logic(self) -> None:
        self.__cheats.process_logic()
        self.scene_manager.process_logic()

    def __process_all_draw(self) -> None:
        self.screen.fill(Color.BLACK)
        self.scene_manager.process_draw(self.screen)
        pg.display.flip()

    def main_loop(self) -> None:
        while True:
            self.__process_all_events()
            self.__process_all_logic()
            self.__process_all_draw()
            self.__clock.tick(self.__FPS)

    def exit_game(self) -> None:
        self.storage.save()
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
