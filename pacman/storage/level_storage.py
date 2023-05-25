from pygame.event import Event

from pacman.data_core import EvenType

from .utils import SerDes


class LevelStorage(SerDes):
    def __init__(self):
        self.__level_count = 10
        self.__unlocked = []
        self.__current = 0

    @property
    def len(self) -> int:
        return self.__level_count

    @property
    def len_unlocked(self) -> int:
        return len(self.__unlocked)

    @property
    def current(self) -> int:
        return self.__current

    @current.setter
    def current(self, value):
        if isinstance(value, int) and 0 <= value < self.__level_count:
            self.__current = value % len(self.__unlocked)
        else:
            raise Exception(f"Current level must be in 0 <= {value} < {self.__level_count}")

    def unlock_next_level(self) -> None:
        if len(self.__unlocked) < self.__level_count:
            self.__unlocked.append([0])

    def set_next_level(self) -> None:
        self.current = self.current + 1

    def set_prev_level(self) -> None:
        self.current = self.current - 1

    def current_highscores(self) -> list[int]:
        if self.__current > len(self.__unlocked) - 1:
            return []
        self.__unlocked[self.__current] = sorted(set(self.__unlocked[self.__current]), reverse=True)[0:5]
        return self.__unlocked[self.__current]

    def get_highscore(self) -> int:
        if self.__current > len(self.__unlocked) - 1:
            return 0
        highscore = self.current_highscores()
        if not highscore:
            return 0
        return highscore[0]

    def add_record(self, score: int) -> None:
        if self.__current > len(self.__unlocked) - 1:
            return
        self.__unlocked[self.__current].append(int(score))
        self.current_highscores()

    def is_last_level(self) -> bool:
        return LevelStorage().current + 1 >= self.__level_count

    def event_handler(self, event: Event) -> None:
        if event.type == EvenType.UNLOCK_SAVES:
            self.__unlocked = [[] for _ in range(self.__level_count)]

    def __str__(self):
        return f"Level {self.current + 1}"
