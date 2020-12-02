import json
import os

from misc import ROOT_DIR, create_file_if_not_exist


class Storage:
    __storage_filepath = os.path.join(ROOT_DIR, "saves", "storage.json")
    __default_content = {"level_id": 0,
                         "unlocked_levels": [
                             0
                         ]}

    def __init__(self) -> None:
        self.last_level = None
        self.unlocked_levels = []
        self.load()

    def save(self) -> None:
        string = json.dumps({"level_id": self.last_level, "unlocked_levels": self.unlocked_levels})
        with open(self.__storage_filepath, "w") as file:
            file.write(string)

    def load(self) -> None:
        create_file_if_not_exist(self.__storage_filepath, json.dumps(self.__default_content))
        with open(self.__storage_filepath, "r") as file:
            json_dict = json.load(file)
            self.last_level = json_dict["level_id"]
            self.unlocked_levels = json_dict["unlocked_levels"]
