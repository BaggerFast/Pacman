from random import choice
from typing import List

import pygame as pg
from PIL import Image, ImageFilter

from pacman.data_core import Colors, PathManager, Dirs, Sounds, Config
from pacman.misc import Score, LevelLoader, Skins
from pacman.misc.serializers import StorageLoader, SettingsStorage, SkinStorage, LevelStorage
from pacman.misc.sound_controller import SoundController
from pacman.objects import Map, ImageObject
from pacman.scenes import (
    PauseScene,
    MenuScene,
    MainScene,
    GameOverScene,
    LevelsScene,
    RecordsScene,
    EndGameScene,
    SkinsScene,
    SettingsScene,
)
from pacman.scenes.base import Scene


class Game:
    class Music:
        def __init__(self, game):
            self.click = SoundController(sound_path=Sounds.CLICK)
            self.siren = SoundController(channel=3, sound_path=choice(Sounds.SIREN))
            self.fruit = SoundController(channel=4, sound_path=Sounds.FRUIT)
            self.ghost = SoundController(channel=4, sound_path=Sounds.GHOST)
            self.pellet = SoundController(channel=6, sound_path=Sounds.PELLET)
            self.menu = SoundController(channel=4, sound_path=Sounds.INTERMISSION)

            if SettingsStorage().fun:
                self.pacman = SoundController(sound_path=choice(Sounds.DEAD))
                self.seed = SoundController(channel=4, sound_path=Sounds.SEED_FUN)
                self.intro = SoundController(channel=1, sound_path=choice(Sounds.INTRO))
                self.gameover = SoundController(channel=2, sound_path=choice(Sounds.GAME_OVER))
            else:
                self.pacman = SoundController(sound_path=Sounds.DEAD[0])
                self.seed = SoundController(channel=4, sound_path=Sounds.SEED)
                self.intro = SoundController(
                    channel=1,
                    sound_path=(
                        Sounds.INTRO[0] if not SkinStorage().current == game.skins.pokeball else Sounds.POC_INTRO
                    ),
                )
                self.gameover = SoundController(channel=2, sound_path=Sounds.GAME_OVER[0])

        def reload_sounds(self, game):
            self.siren = SoundController(channel=3, sound_path=choice(Sounds.SIREN))
            if SettingsStorage().fun:
                self.pacman = SoundController(sound_path=choice(Sounds.DEAD))
                self.seed = SoundController(channel=4, sound_path=Sounds.SEED_FUN)
                self.intro = SoundController(channel=1, sound_path=choice(Sounds.INTRO))
                self.gameover = SoundController(channel=2, sound_path=choice(Sounds.GAME_OVER))
            else:
                self.pacman = SoundController(sound_path=Sounds.DEAD[0])
                self.seed = SoundController(channel=4, sound_path=Sounds.SEED)
                self.intro = SoundController(
                    channel=1,
                    sound_path=(
                        Sounds.INTRO[0] if not SkinStorage().current == game.skins.pokeball else Sounds.POC_INTRO
                    ),
                )
                self.gameover = SoundController(channel=2, sound_path=Sounds.GAME_OVER[0])

    class Scenes:
        def __init__(self, game):
            self.PAUSE = PauseScene(game)
            self.MENU = MenuScene(game)
            self.MAIN = MainScene(game)
            self.GAMEOVER = GameOverScene(game)
            self.LEVELS = LevelsScene(game)
            self.RECORDS = RecordsScene(game)
            self.ENDGAME = EndGameScene(game)
            self.SKINS = SkinsScene(game)
            self.SETTINGS = SettingsScene(game)
            self.__current = None

        @property
        def current(self):
            return self.__current

        def set(self, scene: Scene, reset: bool = False, surface: bool = False) -> None:
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
            self.read_levels()
            self.__images = self.prerender_surfaces()

        @property
        def images(self) -> List[ImageObject]:
            return self.__images

        @property
        def full_surface(self):
            self.__load_from_map(LevelStorage().current)
            return self.__map.prerender_map_surface()

        @staticmethod
        def level_name(level_id: int = 0) -> str:
            return f"Level {level_id + 1}"

        def __load_from_map(self, level_id: int = 0) -> None:
            self.__loader = LevelLoader(self.levels[level_id])
            self.__map_data = self.__loader.get_map_data()
            self.__map = Map(self.game, self.__map_data)

        def keys(self) -> List[int]:
            return [i for i in range(self.count)]

        def read_levels(self) -> None:
            self.levels = PathManager.get_list_path(f"{Dirs.ASSET}/maps", ext="json")
            self.count = len(self.levels)

        def prerender_surfaces(self) -> list[ImageObject]:
            images = []
            for level_id in range(self.count):
                self.__load_from_map(level_id)
                image = self.__map.prerender_map_image_scaled()
                images.append(image)
            return images

    def __init__(self) -> None:
        self.storage_loader = StorageLoader(PathManager.get_path("storage.json"))
        self.storage_loader.from_file()

        self.__game_over = False
        self.maps = self.Maps(self)
        self.screen = pg.display.set_mode(tuple(Config.RESOLUTION), pg.SCALED)
        self.__clock = pg.time.Clock()
        self.timer = pg.time.get_ticks() / 1000
        self.time_out = 125
        self.animate_timer = 0
        self.skins = Skins(self)
        self.score = Score()

        self.sounds = self.Music(self)

        self.skins.current = "default"
        self.scenes = self.Scenes(self)
        self.scenes.set(self.scenes.MENU)

    @property
    def current_scene(self):
        return self.scenes.current

    # region Exit

    @staticmethod
    def __exit_hotkey_pressed(event: pg.event.Event) -> bool:
        return event.type == pg.KEYDOWN and event.mod & pg.KMOD_CTRL and event.key == pg.K_q

    def __process_exit_events(self, event: pg.event.Event) -> None:
        if event.type == pg.QUIT or Game.__exit_hotkey_pressed(event):
            self.exit_game()

    def exit_game(self) -> None:
        self.storage_loader.to_file()
        self.__game_over = True
        print("Bye bye")

    # endregion

    # region Game Loop

    def __process_all_events(self) -> None:
        for event in pg.event.get():
            self.scenes.current.process_event(event)
            self.__process_exit_events(event)

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
            impil = Image.frombytes("RGBA", tuple(Config.RESOLUTION), surify)
            piler = impil.filter(
                ImageFilter.GaussianBlur(radius=min((current_time - self.timer) * blur_count * 2, blur_count))
            )
            surface = pg.image.fromstring(piler.tobytes(), piler.size, piler.mode).convert()
            self.screen.blit(surface, (0, 0))
        self.scenes.current.process_draw(self.screen)
        pg.display.flip()

    def main_loop(self) -> None:
        while not self.__game_over:
            self.__process_all_events()
            self.__process_all_logic()
            self.__process_all_draw()
            self.__clock.tick(Config.FPS)

    # endregion
