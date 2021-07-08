from typing import List
from misc import HIGHSCORES_COUNT


class HighScore:
    def __init__(self, game) -> None:
        self.game = game
        self.__level_id = self.game.maps.cur_id
        [self.highscores.append([0]*HIGHSCORES_COUNT) for _ in range(self.game.maps.count)]
        self.__data = sorted(self.highscores[self.__level_id])

    @property
    def highscores(self) -> List[List[int]]:
        return self.game.highscores

    @highscores.setter
    def highscores(self, value):
        self.game.highscores = value

    @property
    def data(self):
        return self.__data

    @property
    def level_id(self):
        return self.__level_id

    def add_new_record(self, score) -> None:
        self.highscores[self.__level_id].append(score)
        self.highscores[self.__level_id] = sorted(self.highscores[self.__level_id])
        self.highscores[self.__level_id] = self.highscores[self.__level_id][-HIGHSCORES_COUNT:]
        self.game.highscores = self.highscores

    def update_records(self) -> None:
        self.__level_id = self.game.maps.cur_id
        self.__data = sorted(self.highscores[self.__level_id])
