from pygame import KEYDOWN, KMOD_CTRL, QUIT, SCALED, K_q, display, event, time
from pygame.event import Event

from pacman.data_core import Cfg, EvenType, PathUtl
from pacman.misc import GameObjects
from pacman.objects import KbEvent
from pacman.scenes import SceneManager
from pacman.scenes.menu_scene import MenuScene
from pacman.sound import SoundController, Sounds
from pacman.storage import StorageLoader


class Game:
    def __init__(self) -> None:
        self.__objects = GameObjects()

        self.__screen = display.set_mode(tuple(Cfg.RESOLUTION), SCALED)
        self.__clock = time.Clock()

        self.__storage_loader = StorageLoader(PathUtl.get("storage.json"))

        self.__storage_loader.from_file()
        SoundController.update_volume()

        self.__objects += [self.__storage_loader, KbEvent()]

        SceneManager().reset(MenuScene())

    # region Exit

    @staticmethod
    def __exit_hotkey_pressed(e: Event) -> bool:
        return e.type == KEYDOWN and e.mod & KMOD_CTRL and e.key == K_q

    def __process_exit_events(self, e: Event) -> None:
        if e.type in (QUIT, EvenType.EXIT) or Game.__exit_hotkey_pressed(e):
            self.exit_game()

    def exit_game(self) -> None:
        self.__storage_loader.to_file()
        print("Bye bye")
        exit()

    # endregion

    # region Game Loop

    def __process_all_events(self) -> None:
        for e in event.get():
            self.__objects.event_handler(e)
            Sounds.event_handler(e)
            SceneManager().current.process_event(e)
            self.__process_exit_events(e)

    def __process_all_logic(self) -> None:
        SceneManager().current.process_logic()

    def __process_all_draw(self) -> None:
        self.__screen.blit(SceneManager().current.draw(), (0, 0))
        display.flip()

    def main_loop(self) -> None:
        while True:
            self.__process_all_events()
            self.__process_all_logic()
            self.__process_all_draw()
            self.__clock.tick(Cfg.FPS)

    # endregion
