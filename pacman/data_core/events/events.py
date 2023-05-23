from enum import IntEnum, auto

from pygame import USEREVENT


class EvenType(IntEnum):
    def _generate_next_value_(self, start, count, last_values):
        return USEREVENT + count + 1

    # Game states
    WIN = auto()
    LOSE = auto()
    EXIT = auto()

    # objects
    GHOST_FRIGHTENED = auto()

    # settings
    UPDATE_SOUND = auto()
    SET_SETTINGS = auto()
    GET_SETTINGS = auto()
    UNLOCK_SAVES = auto()

    # keyboard
    RIGHT_BTN = auto()
    LEFT_BTN = auto()
    UP_BTN = auto()
    DONW_BTN = auto()
    ENTER_BTN = auto()
