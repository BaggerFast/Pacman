from enum import Enum, auto

# region States


class BtnStateEnum(Enum):
    INITIAL = 0
    HOVER = auto()
    CLICK = auto()


class GhostStateEnum(Enum):
    CHASE = 0
    SCATTER = auto()
    FRIGHTENED = auto()
    EATEN = auto()


# endregion

# region ListEnum


class DifficultEnum(Enum):
    EASY = 0
    MEDIUM = auto()
    HARD = auto()


class SkinEnum(Enum):
    EDGE = auto()
    CHROME = auto()
    DEFAULT = auto()
    WINDOWS = auto()
    POKEBALL = auto()
    HALF_LIFE = auto()


# endregion