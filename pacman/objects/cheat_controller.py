from pygame import KEYDOWN, K_a, K_z, time
from pygame.event import Event

from pacman.data_core.data_classes import Cheat
from pacman.data_core.enums import SoundCh
from pacman.data_core.interfaces import IEventful, ILogical
from pacman.sound import SoundController, Sounds


class CheatController(ILogical, IEventful):
    def __init__(self, cheats: list[Cheat]):
        self.__cheats = cheats
        self.__timer = time.get_ticks()
        self.__code = ""
        self.__previous_code = ""

    # region Public

    def update(self) -> None:
        self.__complete_cheat()
        self.__update_enter_code()

    def event_handler(self, event: Event) -> None:
        if event.type == KEYDOWN and event.key in range(K_a, K_z + 1):
            self.__code += chr(event.key).lower()

    # endregion

    # region Private

    def __update_timer(self) -> None:
        self.__timer = time.get_ticks()

    def __complete_cheat(self):
        for cheat in self.__cheats:
            if cheat.cheat_code not in self.__code:
                continue
            SoundController.play(SoundCh.SYSTEM, Sounds.CHEAT)
            cheat()
            self.__code = ""
            return

    def __update_enter_code(self):
        if self.__previous_code == self.__code and time.get_ticks() - self.__timer >= 1000:
            self.__code = ""
            self.__update_timer()
        elif self.__previous_code != self.__code:
            self.__update_timer()
        self.__previous_code = self.__code

    # endregion
