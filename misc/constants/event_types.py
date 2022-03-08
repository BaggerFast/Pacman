from enum import IntEnum, auto
import pygame as pg


class EvenType(IntEnum):

    def _generate_next_value_(self, start, count, last_values):
        return pg.USEREVENT + count + 1

    HealthInc = auto()
    HealthDec = auto()

    EatSeed = auto()
    EatGhost = auto()
    EatEnergizer = auto()

    Win = auto()
    GameOver = auto()

    StopFearMode = auto()
    FrightenedMode = auto()


def event_append(event: int):
    pg.event.post(pg.event.Event(event))
