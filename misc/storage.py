import json
import os
from json import JSONDecodeError

from misc import ROOT_DIR, create_file_if_not_exist


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
                          ]
                          }
        self.last_level = None
        self.last_skin = None
        self.unlocked_levels = []
        self.unlocked_skins = []
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
                if "last_level_id" in json_dict:
                    self.__content["last_level_id"] = json_dict["last_level_id"]
                if "last_skin" in json_dict:
                    self.__content["last_skin"] = json_dict["last_skin"]
                if "unlocked_levels" in json_dict:
                    self.__content["unlocked_levels"] = json_dict["unlocked_levels"]
                if "unlocked_skins" in json_dict:
                    self.__content["unlocked_skins"] = json_dict["unlocked_skins"]
            except JSONDecodeError:
                pass
        self.update()
        self.save()

    def update(self):
        self.last_level = self.__content["last_level_id"]
        self.last_skin = self.__content["last_skin"]
        self.unlocked_levels = self.__content["unlocked_levels"]
        self.unlocked_skins = self.__content["unlocked_skins"]
