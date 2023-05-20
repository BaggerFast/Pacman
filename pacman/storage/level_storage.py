from .utils import SerDes


class LevelStorage(SerDes):
    def __init__(self):
        self.level_count = 10
        self.unlocked = []
        self.__current = 0

    @property
    def current(self) -> int:
        return self.__current

    @current.setter
    def current(self, value):
        if isinstance(value, int) and 0 <= value < self.level_count:
            self.__current = value % len(self.unlocked)
        else:
            raise Exception(f"Current level must be in 0 <= {value} < {self.level_count}")

    def unlock_next_level(self) -> None:
        if len(self.unlocked) < self.level_count:
            self.unlocked.append([0])

    def set_next_level(self):
        self.current = self.current + 1

    def set_prev_level(self):
        self.current = self.current - 1

    def current_highscores(self):
        if self.__current > len(self.unlocked) - 1:
            return []
        self.unlocked[self.__current] = sorted(self.unlocked[self.__current], reverse=True)[0:5]
        return self.unlocked[self.__current]

    def get_highscore(self) -> int:
        if self.__current > len(self.unlocked) - 1:
            return 0
        highscore = self.current_highscores()
        if not highscore:
            return 0
        return highscore[0]

    def add_record(self, score: int):
        if self.__current > len(self.unlocked) - 1:
            return
        self.unlocked[self.__current].append(int(score))
        self.unlocked[self.__current] = self.current_highscores()

    def is_last_level(self) -> bool:
        return LevelStorage().current + 1 >= self.level_count

    def __str__(self):
        return f"Level {self.current + 1}"
