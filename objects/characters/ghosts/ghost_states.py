from enum import IntEnum, auto


class GhostState(IntEnum):
    """
    Chase - преследование
    Scatter - разбегание
    Frightened - страх
    """
    scatter = auto()
    eaten = auto()
    frightened = auto()
    chase = auto()

