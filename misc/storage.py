import json
import os
from json import JSONDecodeError

from misc import ROOT_DIR, create_file_if_not_exist, FRUITS_COUNT, HIGHSCORES_COUNT


class Field:
    def dict(self):
        data = {}
        for key in self.__dict__.keys():
            if hasattr(self.__dict__[key], 'dict'):
                data[key] = self.__dict__[key].dict()
            else:
                if hasattr(self.__dict__[key], '__dict__'):
                    data[key] = self.__dict__[key].__dict__
                else:
                    data[key] = self.__dict__[key]
        return data

    def read_dict(self, value):
        for key in self.__dict__.keys():
            if key in value.keys():
                if hasattr(self.__dict__[key], 'dict'):
                    self.__dict__[key].read_dict(value[key])
                else:
                    self.__dict__[key] = value[key]


class Storage(Field):
    class __Settings(Field):
        def __init__(self):
            self.SOUND = True
            self.FUN = False
            self.VOLUME = 100
            self.DIFFICULTY = 0

    __storage_filepath = os.path.join(ROOT_DIR, "saves", "storage.json")

    def __init__(self, game) -> None:
        self.last_level_id = 0
        self.last_skin = "default"
        self.unlocked_levels = [0]
        self.unlocked_skins = ["default"]
        self.settings = self.__Settings()
        self.eaten_fruits = [0 for _ in range(FRUITS_COUNT)]
        self.highscores = [[0 for _ in range(HIGHSCORES_COUNT)] for _ in range(game.maps.count)]
        self.load()

    def save(self) -> None:
        string = json.dumps(self.dict(), indent=2)
        with open(self.__storage_filepath, "w") as file:
            file.write(string)

    def load(self) -> None:
        create_file_if_not_exist(self.__storage_filepath, json.dumps(self.dict(), indent=2))
        with open(self.__storage_filepath, "r") as file:
            try:
                json_dict = json.load(file)
                self.read_dict(json_dict)
            except JSONDecodeError:
                pass
        self.save()
