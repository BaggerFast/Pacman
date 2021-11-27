import pygame
from enum import IntEnum, auto


class EvenType(IntEnum):

    def _generate_next_value_(self, start, count, last_values):
        return pygame.USEREVENT + count + 1

    HealthInc = auto()
    HealthDec = auto()

    EatSeed = auto()
    EatGhost = auto()
    EatEnergizer = auto()

    Win = auto()
    GameOver = auto()

    StopFearMode = auto()

    GoUp = auto()
    GoDown = auto()
    GoLeft = auto()
    GoRight = auto()

    NextBtn = auto()
    PreviousBtn = auto()
    PressBtn = auto()
