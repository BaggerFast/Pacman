import os.path


class HighScore:
    def __init__(self, file_name=os.path.join('saves',
                                              'records.txt'), record_count=5):
        self.file_name = file_name
        self.records_count = record_count
        self.checksForFileExistence()
        self.record_table = self.getRecord()
        self.record = self.record_table[len(self.record_table) - 1]

    def checksForFileExistence(self):
        if not os.path.isfile(self.file_name):
            file = open(self.file_name, 'w')
            for i in range(self.records_count):
                file.write('0\n')
            file.close()

    def getRecord(self):
        file = open(self.file_name)
        record_table = [int(line.strip()) for line in file]
        file.close()
        return record_table

    def checkRecord(self, score):
        self.record_table.append(score)
        self.record_table = sorted(self.record_table)
        self.record_table.pop(0)
        file = open(self.file_name, 'w')

        for i in range(len(self.record_table)):
            file.write(str(self.record_table[i]))
            file.write('\n')
        file.close()
