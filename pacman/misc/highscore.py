from pacman.misc import HIGHSCORES_COUNT
from pacman.misc.serializers import LevelStorage, MainStorage


class HighScore:

    def __init__(self, game) -> None:
        self.game = game
        self.__level_id = LevelStorage().current
        for _ in range(len(MainStorage().highscores), self.game.maps.count):
            MainStorage().highscores.append([0 for _ in range(HIGHSCORES_COUNT)])
        self.__data = sorted(MainStorage().highscores[self.__level_id])

    @property
    def data(self):
        return self.__data

    def add_new_record(self, score) -> None:
        MainStorage().highscores[self.__level_id].append(score)
        MainStorage().highscores[self.__level_id] = sorted(MainStorage().highscores[self.__level_id])
        MainStorage().highscores[self.__level_id] = MainStorage().highscores[self.__level_id][-HIGHSCORES_COUNT:]

    def update_records(self) -> None:
        self.__level_id = LevelStorage().current
        self.__data = sorted(MainStorage().highscores[self.__level_id])
