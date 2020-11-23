import json
import os.path

from misc.constants import MAPS_COUNT, MAPS
from misc.path import create_file_if_not_exist


class HighScore:
    filename = os.path.join('saves', 'records.txt')
    json_filename = os.path.join('saves', 'records.json')
    RECORDS_COUNT = 5

    def __init__(self, game):
        self.game = game
        self.level_name = self.game.level_name
        self.json_data = self.load_json_record()
        self.data = sorted(self.json_data[self.level_name])

    def __del__(self):
        file = open(self.filename, 'w')
        file.write('\n'.join([str(record) for record in self.data]))
        file.close()

    def load_json_record(self) -> dict:
        create_file_if_not_exist(self.json_filename, json.dumps({f"level_{index + 1}": [0 for _ in range(
            self.RECORDS_COUNT)] for index in range(MAPS_COUNT)}))
        with open(self.json_filename, 'r') as file:
            record_table_json = json.load(file)
        if len(record_table_json) < MAPS_COUNT:
            for level_name in MAPS.keys():
                if level_name not in record_table_json:
                    record_table_json[level_name] = [0 for _ in range(self.RECORDS_COUNT)]
            with open(self.json_filename, 'w') as file:
                file.write(json.dumps(record_table_json))

        return record_table_json

    def save_json_record(self):
        with open(self.json_filename, 'w') as file:
            file.write(json.dumps(self.json_data))

    def set_new_record(self, score):
        self.json_data[self.level_name].append(score)
        sorted(self.json_data[self.level_name])
        self.json_data[self.level_name] = self.json_data[self.level_name][-self.RECORDS_COUNT:]
        self.data = self.json_data[self.level_name]

    def update_records(self):
        self.level_name = self.game.level_name
        self.data = sorted(self.json_data[self.level_name])
