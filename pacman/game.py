import pygame as pg
from pygame.event import Event

from pacman.data_core import Cfg, EvenType, PathUtl
from pacman.misc import GameObjects
from pacman.scenes import SceneManager
from pacman.scenes.menu_scene import MenuScene
from pacman.sound import SoundController
from pacman.storage import LevelStorage, SkinStorage, StorageLoader


class Game:
    def __init__(self) -> None:
        self.objects = GameObjects()

        self.__screen = pg.display.set_mode(tuple(Cfg.RESOLUTION), pg.SCALED)
        self.__clock = pg.time.Clock()

        self.storage_loader = StorageLoader(PathUtl.get("storage.json"))
        self.storage_loader.from_file()

        self.objects.append(self.storage_loader)

        SceneManager().reset(MenuScene())

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
            self.objects.event_handler(event)
            SoundController().event_handler(event)
            SceneManager().current.process_event(event)
            self.__process_exit_events(event)

    def __process_all_logic(self) -> None:
        SceneManager().current.process_logic()

    def __process_all_draw(self) -> None:
        self.__screen.blit(SceneManager().current.draw(), (0, 0))
        pg.display.flip()

    def main_loop(self) -> None:
        while True:
            self.__process_all_events()
            self.__process_all_logic()
            self.__process_all_draw()
            self.__clock.tick(Cfg.FPS)

    # endregion
