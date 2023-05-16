from enum import Enum, auto


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

# region ListEnum


class DifficultEnum(Enum):
    EASY = 0
    MEDIUM = auto()
    HARD = auto()


class RotateEnum(Enum):
    RIGHT = 0
    DOWN = auto()
    LEFT = auto()
    UP = auto()


# endregion
