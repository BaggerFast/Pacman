from typing import List

import pygame as pg
from pygame.event import Event

from pacman.data_core import Cfg, Dirs, GameObjects, PathUtil
from pacman.events.events import EvenType
from pacman.misc import LevelLoader
from pacman.misc.serializers import LevelStorage, StorageLoader
from pacman.misic import Music
from pacman.objects import ImageObject, Map
from pacman.scene_manager import SceneManager
from pacman.scenes.menu import MenuScene


class Game:
    class Maps:
        def __init__(self):
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

        def __load_from_map(self, level_id: int = 0) -> None:
            self.__loader = LevelLoader(self.levels[level_id])
            self.__map_data = self.__loader.map
            self.__map = Map(self.__map_data)

        def read_levels(self) -> None:
            self.levels = sorted(PathUtil.get_list(f"{Dirs.ASSET}/maps"))
            self.count = len(self.levels)

        def prerender_surfaces(self) -> list[ImageObject]:
            images = []
            for level_id in range(self.count):
                self.__load_from_map(level_id)
                image = self.__map.prerender_map_image_scaled()
                images.append(image)
            return images

    def __init__(self) -> None:
        self.storage_loader = StorageLoader(PathUtil.get("storage.json"))
        self.storage_loader.from_file()

        self.maps = self.Maps()
        self._screen = pg.display.set_mode(tuple(Cfg.RESOLUTION), pg.SCALED)
        self.__clock = pg.time.Clock()
        self.time_out = 125
        self.animate_timer = 0

        self.objects = GameObjects()
        self.objects.append(self.storage_loader)

        SceneManager().reset(MenuScene(self))

    # region Exit

    @staticmethod
    def __exit_hotkey_pressed(event: Event) -> bool:
        return event.type == pg.KEYDOWN and event.mod & pg.KMOD_CTRL and event.key == pg.K_q

    def __process_exit_events(self, event: Event) -> None:
        if event.type in (pg.QUIT, EvenType.EXIT) or Game.__exit_hotkey_pressed(event):
            self.exit_game()

    def exit_game(self) -> None:
        self.storage_loader.to_file()
        print("Bye bye")
        exit()

    # endregion

    # region Game Loop

    def __process_all_events(self) -> None:
        for event in pg.event.get():
            Music().event_handler(event)
            SceneManager().current.process_event(event)
            self.objects.event_handler(event)
            self.__process_exit_events(event)

    def __process_all_logic(self) -> None:
        SceneManager().current.process_logic()

    def __process_all_draw(self) -> None:
        self._screen.blit(SceneManager().current.draw(), (0, 0))
        pg.display.flip()

    def main_loop(self) -> None:
        while True:
            self.__process_all_events()
            self.__process_all_logic()
            self.__process_all_draw()
            self.__clock.tick(Cfg.FPS)

    # endregion
