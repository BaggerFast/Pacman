from copy import deepcopy

from misc.patterns import Singleton
from misc.storage.base import SerDes


class LevelStorage(SerDes, Singleton):

    def __init__(self):
        self.current = 0
        self.__unlocked = [[]]

    # @property
    # def unlocked(self):
    #     return deepcopy(self.__unlocked)

    def get_current_records(self, total: bool = False):
        self.__unlocked[self.current].sort(reverse=True)
        if total:
            try:
                return self.__unlocked[self.current][0] if self.__unlocked[self.current][0] else 0
            except IndexError:
                return 0
        return deepcopy(self.__unlocked[self.current])

    def update_current_records(self, score: int) -> None:
        self.__unlocked[self.current].append(score)
        self.__unlocked[self.current] = sorted(set(self.__unlocked[self.current]), reverse=True)[:5]

    def unlock_next_level(self) -> None:
        self.__unlocked.append([])

    def __str__(self):
        return f'Level:{self.current + 1}'
