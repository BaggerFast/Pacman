from enum import IntEnum, auto
import pygame as pg


class EvenType(IntEnum):

    def _generate_next_value_(self, start, count, last_values):
        return pg.USEREVENT + count + 1

    HEALTH_INC = auto()
    HEALTH_DEC = auto()

    EAT_SEED = auto()
    EAT_GHOST = auto()
    EAT_ENERGIZER = auto()

    WIN = auto()
    GAME_OVER = auto()

    STOP_FEAR_MODE = auto()
    FRIGHTENED_MODE = auto()


def event_append(event: int):
    pg.event.post(pg.event.Event(event))
