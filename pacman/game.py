import pygame as pg

from misc import PathManager, LevelLoader, Score
from misc.constants import Sounds, Color
from misc.misc import load_image
from misc.scene_manager import SceneManager
from misc.skins.manager import Skins
from misc.sound_manager import Sound
from misc.storage import SettingStorage, MainStorage
from pacman.objects import Map
from pacman.scenes import *
from settings import FPS


class Game:
    # region Pygame init

    pg.display.init()
    pg.font.init()
    pg.mixer.init()

    # endregion

    # region Set icon

    pg.display.set_caption('PACMAN')
    pg.display.set_icon(pg.transform.scale(load_image('ico.png'), (256, 256)))

    # endregion

    class Music:

        def __init__(self):
            self.click = Sound(sound=Sounds.CLICK)
            # self.siren = Sound(channel=3, sound=Sounds.SIREN)
            self.fruit = Sound(channel=4, sound=Sounds.FRUIT)
            self.ghost = Sound(channel=4, sound=Sounds.GHOST)
            self.pellet = Sound(channel=6, sound=Sounds.PELLET)
            self.menu = Sound(channel=4, sound=Sounds.INTERMISSION)

            if SettingStorage().fun:
                # self.pacman = Sound(sound=choice(Sounds.DEAD))
                self.seed = Sound(channel=4, sound=Sounds.SEED_FUN)
                # self.intro = Sound(channel=1, sound=choice(Sounds.INTRO))
                # self.gameover = Sound(channel=2, sound=choice(Sounds.GAMEOVER))
            else:
                # self.pacman = Sound(sound=Sounds.DEAD[0])
                self.seed = Sound(channel=4, sound=Sounds.SEED)
                self.intro = Sound(channel=1, sound=Sounds.POC_INTRO)
                # self.gameover = Sound(channel=2, sound=Sounds.GAMEOVER[0])

        def reload_sounds(self, game):
            # self.siren = Sound(channel=3, sound=choice(Sounds.SIREN))
            if SettingStorage().fun:
                # self.pacman = Sound(sound=choice(Sounds.DEAD))
                self.seed = Sound(channel=4, sound=Sounds.SEED_FUN)
                # self.intro = Sound(channel=1, sound=choice(Sounds.INTRO))
                # self.gameover = Sound(channel=2, sound=choice(Sounds.GAMEOVER))
            else:
                # self.pacman = Sound(sound=Sounds.DEAD[0])
                self.seed = Sound(channel=4, sound=Sounds.SEED)
                # self.intro = Sound(channel=1, sound=Sounds.INTRO[0])
                # self.gameover = Sound(channel=2, sound=Sounds.GAMEOVER[0])

    # todo delete scenes from game

    class Scenes:

        def __init__(self):
            self.PAUSE = PauseScene
            self.MENU = MenuScene
            self.MAIN = MainScene
            self.GAMEOVER = GameLoseScene
            self.LEVELS = LevelScene
            self.RECORDS = RecordsScene
            self.ENDGAME = GameWinScene
            self.SKINS = SkinScene
            self.SETTINGS = SettingsScene
            self.__current = None

        @property
        def current(self):
            return self.__current

        def set(self, scene, reset: bool = False, surface: bool = False) -> None:
            """
            :param scene: NEXT scene (contains in game.scenes.*)
            :param reset: if reset == True will call on_reset() of NEXT scene (see Base.Scene)
            :param surface: if surface == True background of new scene equal CURRENT scene with BLUR
            IMPORTANT: it calls on_deactivate() on CURRENT scene and on_activate() on NEXT scene
            """
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

        def keys(self) -> list[int]:
            return [i for i in range(self.count)]

        def read_levels(self) -> None:
            self.levels = PathManager.get_list("maps", ext='json')
            self.count = len(self.levels)

        def prerender_surfaces(self) -> list[pg.Surface]:
            images = []
            for level_id in range(self.count):
                self.__load_from_map(level_id)
                image = self.__map.prerender_map_image_scaled()
                images.append(image)
            return images

    __size = width, height = 224, 285

    def __init__(self) -> None:
        self.screen = pg.display.set_mode(self.__size, pg.SCALED)
        self.__clock = pg.time.Clock()
        self.__game_over = False

        self.maps = self.Maps(self)

        self.timer = pg.time.get_ticks() / 1000
        self.time_out = 125
        self.animate_timer = 4

        self.scenes = self.Scenes()
        self.skins = Skins(self)
        self.score = Score()

        MainStorage().deserialize_from_file()
        self.sounds = self.Music()
        # self.skins.current = self.__storage.last_skin if self.__storage.last_skin in self.unlocked_skins else self.__def_skin
        # self.records = HighScore(self)

        SceneManager().append(MenuScene(self))

    @property
    def current_scene(self):
        return SceneManager().current

    @property
    def size(self):
        return self.__size

    def __process_exit_events(self, event: pg.event.Event) -> None:
        exit_hotkey = event.type == pg.KEYDOWN and event.mod & pg.KMOD_CTRL and event.key == pg.K_q
        if event.type == pg.QUIT or exit_hotkey:
            self.exit_game()

    def __process_all_events(self) -> None:
        for event in pg.event.get():
            self.__process_exit_events(event)
            SceneManager().current.process_event(event)

    def __process_all_logic(self) -> None:
        SceneManager().current.process_logic()

    def __process_all_draw(self) -> None:
        exceptions = [PauseScene, GameLoseScene, GameWinScene]
        if SceneManager().current not in exceptions:
            self.screen.fill(Color.BLACK)
        else:
            blur_count = 10
            current_time = pg.time.get_ticks() / 1000
            # surify = pg.image.tostring(self.scenes.MAIN.template, 'RGBA')
            # impil = Image.frombytes('RGBA', self.__size, surify)
            # piler = impil.filter(
            #     ImageFilter.GaussianBlur(radius=min((current_time - self.timer) * blur_count * 2, blur_count)))
            # surface = pg.image.fromstring(piler.tobytes(), piler.size, piler.mode).convert()

            # self.screen.blit(surface, (0, 0))
        SceneManager().current.process_draw()

        pg.display.flip()

    def main_loop(self) -> None:
        while not self.__game_over:
            self.__process_all_events()
            self.__process_all_logic()
            self.__process_all_draw()
            self.__clock.tick(FPS)

    def exit_game(self) -> None:
        MainStorage().serialize_to_file()
        self.__game_over = True

    # region REMOVE

    # todo unlock

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
        :param skin_name: skins name
        """
        if skin_name in self.skins.all_skins:
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
            self.eaten_fruits[fruit_id] += value
        else:
            raise Exception(f"id error. Fruit id: {fruit_id} doesn't exist")

    # endregion
