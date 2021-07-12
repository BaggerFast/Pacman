import pygame
from enum import IntEnum, auto


class EvenType(IntEnum):
    def _generate_next_value_(name, start, count, last_values):
        return pygame.USEREVENT + count + 1

    HealthInc = auto()
    HealthDec = auto()
    Win = auto()
    GameOver = auto()
