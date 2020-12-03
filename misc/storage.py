import json
import os
from json import JSONDecodeError

from misc import ROOT_DIR, create_file_if_not_exist, FRUITS_COUNT


class Storage:
    __storage_filepath = os.path.join(ROOT_DIR, "saves", "storage.json")

    def __init__(self) -> None:
        self.__content = {"last_level_id": 0,
                          "last_skin": "default",
                          "unlocked_levels": [
                              0
                          ],
                          "unlocked_skins": [
                              "default"
                          ],
                          "eaten_fruits": [
                              0 for _ in range(FRUITS_COUNT)
                          ]
                          }
        self.last_level_id = None
        self.last_skin = None
        self.unlocked_levels = []
        self.unlocked_skins = []
        self.eaten_fruits = []
        self.load()

    def save(self) -> None:
        string = json.dumps(self.__content)
        with open(self.__storage_filepath, "w") as file:
            file.write(string)

    def load(self) -> None:
        create_file_if_not_exist(self.__storage_filepath, json.dumps(self.__content))
        with open(self.__storage_filepath, "r") as file:
            try:
                json_dict = json.load(file)
                for key in self.__content.keys():
                    if key in json_dict:
                        self.__content[key] = json_dict[key]
            except JSONDecodeError:
                pass
        self.update()
        self.save()

    def update(self):
        for key in self.__dict__.keys():
            if key != "_Storage__content":
                self.__dict__[key] = self.__content[key]
