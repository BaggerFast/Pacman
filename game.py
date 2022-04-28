import sys
import pygame as pg
from random import choice
from misc import LevelLoader, ControlCheats, PathManager
from misc.cheat_codes import Cheat
from misc.constants import Color
from misc.constants.classes import Sounds
from misc.constants.skin_names import SkinsNames
from misc.skins import Skins
from misc.sound_controller import SoundController

from serializers import StorageSerializer, SettingsSerializer, SkinSerializer, SerializerLoader, LevelSerializer

from objects.map import Map
from objects.objects import Objects

from scenes import SceneManager, MenuScene, BaseScene


class Game:
    # region Initialize pygame
    pg.display.init()
    pg.font.init()
    pg.mixer.init()
    # endregion

    # region Window title and icon
    pg.display.set_caption('PACMAN')
    pg.display.set_icon(pg.transform.scale(pg.image.load(PathManager.get_image_path('ico.png')), (256, 256)))
    # endregion

    class Cheats:

        UNLOCK_SKINS = False
        UNLOCK_LEVELS = False
        INFINITY_LIVES = False
        GHOSTS_COLLISION = False

        def __init__(self):
            self.__configure_args()

        def __configure_args(self):
            for arg in sys.argv[1:]:
                arg = arg.upper()
                if hasattr(self, arg):
                    setattr(self, arg, True)

        # def unlock_skins(self):
        #     self.game.unlocked_skins = self.game.skins.all_skins if self.game.cheats_var.UNLOCK_SKINS \
        #         else self.game.storage.unlocked_skins
        #     if isinstance(self.game.scene_manager.current, scenes.SkinsScene):
        #         ...
        #         # self.game.scene_manager.current._create_objects()
        #
        # def unlock_levels(self):
        #     self.game.unlocked_levels = self.game.maps.keys() if self.game.cheats_var.UNLOCK_LEVELS \
        #         else self.game.storage.unlocked_levels
        #     if isinstance(self.game.scene_manager.current, scenes.LevelsScene):
        #         ...
        #         # self.game.scene_manager.current._create_objects()

    class Music:

        def __init__(self, game):
            self.game = game
            self.reload_sounds()

        def base_preset(self):
            self.click = SoundController(self.game, Sounds.Ch.menu, Sounds.CLICK)
            self.menu = SoundController(self.game, Sounds.Ch.menu, Sounds.INTERMISSION)
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
            self.fun = SettingsSerializer().FUN
            self.preset_for_fun()
            self.base_preset()
            if self.fun:
                return
            self.game.skins.current.sound_preset()

    class Maps:

        def __init__(self):
            self.levels: list = PathManager.get_list_path("maps", ext='json')
            self.images = list(self.prerender_surfaces())

        def __len__(self):
            return len(self.levels)

        def __str__(self):
            return f'Level: {LevelSerializer().current + 1}'

        @property
        def full_surface(self):
            self.__load_from_map(LevelSerializer().current)
            return self.__map.prerender_map_surface()

        def __load_from_map(self, level_id: int = 0) -> None:
            self.__loader = LevelLoader(self.levels[level_id])
            self.__map_data = self.__loader.get_map_data()
            self.__map = Map(self.__map_data)

        def prerender_surfaces(self):
            for level_id in range(len(self.levels)):
                self.__load_from_map(level_id)
                yield self.__map.prerender_map_image_scaled()

    __resolution = width, height = 224, 285
    screen = pg.display.set_mode(__resolution, pg.SCALED)
    __FPS: int = 60
    __def_level_id = 0
    __game_over = False

    def __init__(self):
        self.maps = self.Maps()
        self.__clock = pg.time.Clock()
        self.time_out: int = 125
        self.animate_timer: int = 0
        self.storage = StorageSerializer(self)

        self.storage_loader = SerializerLoader(self.storage)
        self.storage_loader.load_from_file()

        self.skins = Skins(self)
        self.cheats_var = self.Cheats()
        self.__read_from_storage()

        self.scene_manager = SceneManager()

        self.__cheats = ControlCheats([
            Cheat(self, 'skins', self.cheats_var.UNLOCK_SKINS),
            Cheat(self, 'maps', self.cheats_var.UNLOCK_LEVELS),
            Cheat(self, 'lives', self.cheats_var.INFINITY_LIVES),
            Cheat(self, 'collision', self.cheats_var.GHOSTS_COLLISION)
        ])

        self.sounds = self.Music(self)

        self.skins.current = self.storage.skins.current if self.storage.skins.current in self.storage.skins.unlocked \
            else SkinsNames.default

        self.scene_manager.reset(MenuScene(self))

        self.obj = Objects(self.scene_manager, self.__cheats)

    # region Public

    def main_loop(self) -> None:
        while not self.__game_over:
            self.__process_all_events()
            self.__process_all_logic()
            self.__process_all_draw()
            self.__clock.tick(self.__FPS)
        self.storage_loader.save_to_file()

    def exit_game(self) -> None:
        self.__game_over = True

    # todo levels ans skins
    def unlock_level(self, level_id: int = 0) -> None:
        """
        :param level_id: level id
        """
        if level_id not in range(len(self.maps)):
            raise Exception(f"id error. Map id: {level_id} doesn't exist")
        if not self.cheats_var.UNLOCK_LEVELS:
            try:
                self.unlocked_levels[level_id]
            except IndexError:
                self.unlocked_levels.append([])

    # todo skins
    def unlock_skin(self, skin_name: str = 0) -> None:
        """
        :param skin_name: skin name
        """
        if skin_name in self.skins.all_skins:
            if not self.cheats_var.UNLOCK_SKINS and skin_name not in self.storage.skins.unlocked:
                self.storage.skins.unlocked.append(skin_name)
        else:
            raise Exception(f"Name error. Skin name: {skin_name} doesn't exist")

    def store_fruit(self, fruit_id: int = 0, value: int = 0) -> None:
        """
        :param fruit_id: fruit id
        :param value: count of fruits
        """
        self.storage.eaten_fruits[fruit_id] += value

    @property
    def difficulty(self) -> int:
        return self.storage.settings.DIFFICULTY + 1

    @property
    def current_scene(self) -> BaseScene:
        return self.scene_manager.current

    @property
    def resolution(self) -> tuple:
        return self.__resolution

    # endregion

    # region Private

    def __read_from_storage(self) -> None:
        self.unlocked_levels = self.storage.levels.unlocked
        self.maps.cur_id = self.storage.levels.current

    def __process_exit_events(self, event: pg.event.Event) -> None:
        ctr_q = event.type == pg.KEYDOWN and event.mod & pg.KMOD_CTRL and event.key == pg.K_q

        if event.type == pg.QUIT or ctr_q:
            self.exit_game()

    def __process_all_events(self) -> None:
        for event in pg.event.get():
            self.obj.process_event(event)
            self.__process_exit_events(event)

    def __process_all_logic(self) -> None:
        self.obj.process_logic()

    def __process_all_draw(self) -> None:
        self.screen.fill(Color.BLACK)
        self.obj.process_draw(self.screen)
        pg.display.flip()

    # endregion
