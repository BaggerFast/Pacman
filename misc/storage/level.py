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
        if total:
            try:
                return self.unlocked[self.current][0] if self.unlocked[self.current][0] else 0
            except IndexError:
                return 0
        return self.unlocked[self.current]

    def update_current_records(self, score: int) -> None:
        self.unlocked[self.current].append(score)
        self.unlocked[self.current] = sorted(set(self.unlocked[self.current]), reverse=True)[:5]

    def unlock_next_level(self) -> None:
        self.unlocked.append([])

    def __str__(self):
        return f'Level: {self.current + 1}'
