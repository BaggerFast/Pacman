import pygame as pg
from loguru import logger
from pacman.misc.interfaces import ILogical, IEventful


class Cheat(ILogical):

    def __init__(self, game, code, func):
        self.cheat_code = code
        self.function = func
        self.game = game

    def process_logic(self) -> None:
        logger.info(f'Active cheat: {self.cheat_code.lower()}')
        self.game.sounds.cheat.play()
        self.function()


class ControlCheats(ILogical, IEventful):

    def __init__(self, cheats: list[Cheat]):
        self.cheats: list[Cheat] = cheats
        self.timer = pg.time.get_ticks()
        self.enter_code: str = ''
        self.previous_enter_code: str = ''

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
            cheat.process_logic()
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
