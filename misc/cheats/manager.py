import pygame as pg
from .cheat import Cheat


class CheatManager:

    def __init__(self, cheats: list[Cheat]):
        self.cheats = cheats
        self.timer = pg.time.get_ticks()
        self.enter_code = ''
        self.previous_enter_code = ''

    # region Public

    # region Implementation of ILogical, IEventful

    def process_logic(self) -> None:
        self.__complete_cheat()
        self.__update_enter_code()

    def process_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key in range(pg.K_a, pg.K_z + 1):
            self.enter_code += chr(event.key).lower()

    # endregion

    # endregion

    # region Private

    def __update_timer(self) -> None:
        self.timer = pg.time.get_ticks()

    def __complete_cheat(self):
        for cheat in self.cheats:
            if cheat.cheat_code != self.enter_code:
                continue
            cheat()
            self.enter_code = ''
            return

    def __update_enter_code(self):
        if self.previous_enter_code == self.enter_code and pg.time.get_ticks() - self.timer >= 1000:
            self.enter_code = ''
            self.__update_timer()
        elif self.previous_enter_code != self.enter_code:
            self.__update_timer()
        self.previous_enter_code = self.enter_code

    # endregion
