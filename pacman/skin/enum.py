from enum import Enum

from .skin import Skin


class SkinEnum(Enum):
    DEFAULT = Skin("default", {})
    EDGE = Skin("edge", {0: 12, 1: 5})
    POKEBALL = Skin("pokeball", {2: 12, 3: 5})
    WINDOWS = Skin("windows", {3: 12, 4: 5})
    VALVE = Skin("valve", {4: 12, 5: 5})
    CHROME = Skin("chrome", {5: 12, 6: 5})
    STALKER = Skin("stalker", {5: 15, 6: 15})
