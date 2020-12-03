import json
import os.path

from misc import Maps
from misc.path import create_file_if_not_exist  # НЕ УДАЛЯТЬ .path (Без него ошибка из-за зацикленного импорта)


class HighScore:
    __json_filename = os.path.join('saves', 'records.json')
    __RECORDS_COUNT = 5

    def __init__(self, game) -> None:
        self.__json_default = [[0 for _ in range(self.__RECORDS_COUNT)] for _ in range(Maps.count)]
        self.__game = game
        self.__level_id = self.__game.level_id
        self.__json_data = self.load_json_record()
        self.__data = sorted(self.__json_data[self.__level_id])

    @property
    def data(self):
        return self.__data

    @property
    def level_id(self):
        return self.__level_id

    def load_json_record(self) -> dict:
        create_file_if_not_exist(self.__json_filename, json.dumps(self.__json_default))
        with open(self.__json_filename, 'r') as file:
            record_table_json = json.load(file)
        if len(record_table_json) < Maps.count:
            for level_id in Maps.keys():
                if str(level_id) not in record_table_json:
                    record_table_json[level_id] = [0 for _ in range(self.__RECORDS_COUNT)]
            with open(self.__json_filename, 'w') as file:
                file.write(json.dumps(record_table_json))
        return record_table_json

    def save_json_record(self) -> None:
        with open(self.__json_filename, 'w') as file:
            file.write(json.dumps(self.__json_data))

    def add_new_record(self, score) -> None:
        self.__json_data[self.__level_id].append(score)
        self.__json_data[self.__level_id] = sorted(self.__json_data[self.__level_id])
        self.__json_data[self.__level_id] = self.__json_data[self.__level_id][-self.__RECORDS_COUNT:]
        self.__data = self.__json_data[self.__level_id]
        self.save_json_record()

    def update_records(self) -> None:
        self.__level_id = self.__game.level_id
        self.__data = sorted(self.__json_data[self.__level_id])
