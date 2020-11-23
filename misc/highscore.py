import os.path
from misc.path import create_file_if_not_exist


class HighScore:
    filename = os.path.join('saves', 'records.txt')
    json_filename = os.path.join('saves', 'records.json')
    RECORDS_COUNT = 5

    def __init__(self):
        #self.create_file_if_not_exist()
        create_file_if_not_exist(self.filename, '\n'.join(["0" for _ in range(self.RECORDS_COUNT)]))
        self.data = sorted(self.load_records())
        self.record = self.data[len(self.data) - 1]

    def __del__(self):
        file = open(self.filename, 'w')
        file.write('\n'.join([str(record) for record in self.data]))
        file.close()

    def load_records(self):
        with open(self.filename, 'r') as file:
            record_table = [int(line.strip()) for line in file]
        return record_table

    def set_new_record(self, score):
        self.data.append(score)
        self.data = sorted(self.data)
        self.data = self.data[:self.RECORDS_COUNT]
