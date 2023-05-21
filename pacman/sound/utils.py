from abc import ABC
from random import shuffle
from secrets import choice

from pacman.data_core import Dirs, PathUtl


class PtxUtl(ABC):
    @staticmethod
    def norm(path: str) -> str:
        return f"default/{path}"

    @staticmethod
    def fun(path: str) -> str:
        pathes = PathUtl.get_list(f"{Dirs.SOUND}/fun/{path}")
        shuffle(pathes)
        return choice(pathes)

    @staticmethod
    def valve(path: str) -> str:
        return f"valve/{path}"

    @staticmethod
    def win(path: str) -> str:
        return f"windows/{path}"

    @staticmethod
    def stalker(path: str) -> str:
        pathes = PathUtl.get_list(f"{Dirs.SOUND}/stalker/{path}")
        shuffle(pathes)
        return choice(pathes)
