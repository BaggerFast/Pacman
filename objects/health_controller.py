import pygame as pg
from misc.constants import EvenType, event_append
from misc.interfaces import IDrawable, IEventful, ILogical
from objects.image import ImageObject


class HealthView(ImageObject):

    def __init__(self, image, pos: tuple[int, int], shift: int):
        ImageObject.__init__(self, image=image, pos=pos)
        self.image = pg.transform.flip(self.image, True, False)
        self.shift = shift
        self.hp_count = 0

    def process_draw(self, screen: pg.Surface) -> None:
        for i in range(self.hp_count):
            screen.blit(self.image, (self.rect.x + i * self.shift, self.rect.y))


class HealthLogic(IEventful):

    def __init__(self, hp_count: int = 3, max_hp: int = 5):
        if hp_count > max_hp or hp_count == 0:
            raise Exception
        self.__max_hp: int = max_hp
        self.__cur_hp: int = self.__check_limits(hp_count)
        # todo health_events usability
        self.__events = {
            EvenType.HealthInc: lambda: self.get_health(1),
            EvenType.HealthDec: lambda: self.get_damage(1),
        }

    @property
    def alive(self) -> bool:
        return self.__cur_hp > 0

    @property
    def count(self) -> int:
        return self.__cur_hp

    def get_damage(self, amount: int) -> None:
        if amount <= 0:
            raise Exception('damage must be positive')
        self.__cur_hp = self.__check_limits(self.__cur_hp - amount)

    def get_health(self, amount: int) -> None:
        if amount <= 0:
            raise Exception('heal must be positive')
        self.__cur_hp = self.__check_limits(self.__cur_hp + amount)

    def __check_limits(self, amount: int) -> int:
        return max(0, min(self.__max_hp, int(amount)))

    def process_event(self, event: pg.event.Event) -> None:
        if event.type in self.__events:
            self.__events[event.type]()


class HealthController(IDrawable, ILogical, IEventful):

    def __init__(self, game, hp_count: int = 3, max_hp: int = 5):
        self.game = game
        self.hp = HealthLogic(hp_count, max_hp)
        self.hp_view = HealthView(self.game.skins.current.walk.sheet[0][3], (5, 270), 20)

    def process_logic(self) -> None:
        # todo health alive usability
        self.hp_view.hp_count = self.hp.count
        cheat = self.game.cheats_var.INFINITY_LIVES
        if all([not cheat, not self.hp.alive, not self.game.sounds.pacman.is_busy()]):
            event_append(EvenType.GameOver)

    def process_event(self, event: pg.event.Event) -> None:
        self.hp.process_event(event)

    def process_draw(self, screen: pg.Surface) -> None:
        self.hp_view.process_draw(screen)
