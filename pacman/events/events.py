from enum import IntEnum, auto

from pygame import USEREVENT


class EvenType(IntEnum):
    def _generate_next_value_(self, start, count, last_values):
        return USEREVENT + count + 1

    WIN = auto()
    LOSE = auto()
    EXIT = auto()
    SET_SETTINGS = auto()
    GET_SETTINGS = auto()
