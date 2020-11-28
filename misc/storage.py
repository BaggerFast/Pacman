import json
import os

from misc import ROOT_DIR, create_file_if_not_exist


class Storage:
    __last_level_filepath = os.path.join(ROOT_DIR, "saves", "storage.json")

    def __init__(self) -> None:
        self.last_level = None
        self.read_last_level()

    def save_last_level(self) -> None:
        string = json.dumps({f"level_name": f"{self.last_level}"})
        with open(self.__last_level_filepath, "w") as file:
            file.write(string)

    def read_last_level(self) -> None:
        create_file_if_not_exist(self.__last_level_filepath, json.dumps({"level_name": "level_1"}))
        with open(self.__last_level_filepath, "r") as file:
            self.last_level = json.load(file)["level_name"]
