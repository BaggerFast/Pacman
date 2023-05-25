from enum import Enum, auto

from pygame import mixer
from pygame.mixer import Channel

# region States


class PacmanState(Enum):
    IDLING = 0
    MOVING = auto()
    DEATH = auto()


class BtnStateEnum(Enum):
    INITIAL = 0
    HOVER = auto()
    CLICK = auto()


class GhostStateEnum(Enum):
    CHASE = 0
    SCATTER = auto()
    FRIGHTENED = auto()
    EATEN = auto()
    HIDDEN = auto()
    INDOOR = auto()


class FruitStateEnum:
    ACTIVE = 0
    DISABLED = auto()
    EATEN = auto()


class GameStateEnum(Enum):
    INTRO = 0
    ACTION = auto()


# endregion

# region List


class DifficultEnum(Enum):
    CHILD = 0
    NORMAL = auto()
    HARDCORE = auto()


class RotateEnum(Enum):
    RIGHT = 0
    DOWN = auto()
    LEFT = auto()
    UP = auto()


class SoundCh(Enum):
    mixer.init()
    SYSTEM = Channel(0)
    BACKGROUND = Channel(1)
    PLAYER = Channel(2)


# endregion
