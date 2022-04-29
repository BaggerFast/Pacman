import pygame as pg
from misc.constants import EvenType, SkinsNames, event_append, Font
from misc.interfaces import IDrawable, IEventful
from objects.text import Text
from serializers import SettingsSerializer, SkinSerializer


class Score(IDrawable, IEventful):
    base_pos = (5, 270)
    shift = 20

    def __init__(self):
        self.__value = 0
        self.fear_mode = False
        self.fear_count = 0
        self.text = Text(f'{self.__value}', Font.MAIN_SCENE_SIZE, rect=pg.Rect(10, 8, 20, 20))

        self.__events = {
            EvenType.EAT_SEED: lambda: self + 10 * SettingsSerializer().difficulty,
            EvenType.EAT_ENERGIZER: self.__eat_energizer,
            EvenType.EAT_GHOST: self.__eat_ghost,
            EvenType.STOP_FEAR_MODE: self.__deactivate_fear_mode,
        }

    def __int__(self):
        return self.__value

    def __add__(self, value):
        self.__value += value
        return self

    def __iadd__(self, value):
        return self + value

    def __str__(self) -> str:
        return str(self.__value)

    # region Public

    # region Implementation of IDrawable, IEventful

    def process_draw(self, screen: pg.Surface) -> None:
        self.text.text = f'{self.__value} {"Mb" if SkinSerializer().current == SkinsNames.CHROME else ""}'
        self.text.process_draw(screen)

    def process_event(self, event: pg.event.Event) -> None:
        if event.type in self.__events:
            self.__events[event.type]()

    # endregion

    @property
    def score(self):
        return self.__value

    def eat_fruit(self, bonus) -> None:
        self + bonus * SettingsSerializer().difficulty

    # endregion

    # region Private

    def __eat_energizer(self):
        self.fear_mode = True
        event_append(EvenType.FRIGHTENED_MODE)

    def __deactivate_fear_mode(self) -> None:
        self.fear_mode = False
        self.fear_count = 0

    def __eat_ghost(self) -> None:
        self + ((200 * SettingsSerializer().difficulty ** 2) * 2 ** self.fear_count)
        self.fear_count += 1

    # endregion
