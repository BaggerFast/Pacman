from enum import Enum, auto


class BtnStateEnum(Enum):
    INITIAL = 0
    HOVER = auto()
    CLICK = auto()


class DifficultEnum(Enum):
    EASY = 0
    MEDIUM = auto()
    HARD = auto()
