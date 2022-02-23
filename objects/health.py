import pygame as pg

from misc import EvenType, event_append
from misc.interfaces import IGenericObject
from objects import ImageObject


class Health(ImageObject, IGenericObject):
    base_pos = (5, 270)
    shift = 20

    def __init__(self, game, lives: int = 3, max_lives: int = 5):
        if lives > max_lives or lives == 0:
            raise Exception
        ImageObject.__init__(self, game, image=game.skins.current.walk.sheet[0][3], pos=self.base_pos)
        self.__max_lives: int = max_lives
        self.__lives: int = self.__check_limits(lives)
        self.__image = pg.transform.flip(self.image, True, False)
        # todo health_events usability
        self.__events = {
            EvenType.HealthInc: lambda: self + 1,
            EvenType.HealthDec: lambda: self - 1,
        }

    @property
    def count(self):
        return self.__lives

    def __add__(self, value: int):
        self.__lives = self.__check_limits(self.__lives + value)
        return self

    def __sub__(self, value: int):
        self.__lives = self.__check_limits(self.__lives - value)
        return self

    def __iadd__(self, value: int):
        return self + value

    def __isub__(self, value: int):
        return self - value

    def __check_limits(self, value) -> int:
        return max(0, min(self.__max_lives, int(value)))

    def process_draw(self) -> None:
        self.game.screen.blits((self.image, (self.rect.x + i * self.shift, self.rect.y)) for i in range(self.__lives))

    def process_event(self, event: pg.event.Event) -> None:
        if event.type in self.__events:
            self.__events[event.type]()

    def process_logic(self) -> None:
        # todo health alive usability
        cheat = self.game.cheats_var.INFINITY_LIVES
        if all([not cheat, not self.alive, not self.game.sounds.pacman.is_busy()]):
            event_append(EvenType.GameOver)

    @property
    def alive(self) -> bool:
        return self.__lives > 0

