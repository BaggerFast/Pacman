import json
import os.path

from misc import MAPS_COUNT, Maps
from misc.path import create_file_if_not_exist # НЕ УДАЛЯТЬ .path (Без него ошибка из-за зацикленного импорта)


class HighScore:
    __json_filename = os.path.join('saves', 'records.json')
    __RECORDS_COUNT = 5

    def __init__(self, game):
        self.__game = game
        self.__level_name = self.__game.level_name
        self.__json_data = self.load_json_record()
        self.__data = sorted(self.__json_data[self.__level_name])

    @property
    def data(self):
        return self.__data

    @property
    def level_name(self):
        return self.__level_name

    def load_json_record(self) -> dict:
        create_file_if_not_exist(self.__json_filename, json.dumps({f"level_{index + 1}": [0 for _ in range(
            self.__RECORDS_COUNT)] for index in range(MAPS_COUNT)}))
        with open(self.__json_filename, 'r') as file:
            record_table_json = json.load(file)
        if len(record_table_json) < MAPS_COUNT:
            for level_name in vars(Maps).keys():
                if level_name not in record_table_json:
                    record_table_json[level_name] = [0 for _ in range(self.__RECORDS_COUNT)]
            with open(self.__json_filename, 'w') as file:
                file.write(json.dumps(record_table_json))
        return record_table_json

    def save_json_record(self):
        with open(self.__json_filename, 'w') as file:
            file.write(json.dumps(self.__json_data))

    def add_new_record(self, score):
        self.__json_data[self.__level_name].append(score)
        self.__json_data[self.__level_name] = sorted(self.__json_data[self.__level_name])
        self.__json_data[self.__level_name] = self.__json_data[self.__level_name][-self.__RECORDS_COUNT:]
        self.__data = self.__json_data[self.__level_name]
        self.save_json_record()

    def update_records(self):
        self.__level_name = self.__game.level_name
        self.__data = sorted(self.__json_data[self.__level_name])
