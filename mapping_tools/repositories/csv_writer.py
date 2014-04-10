import csv 
import sys

class CSVWriter(object):

    def __init__(self, mapper):
        self.mapper = mapper
        header = sorted([column.key for column in self.mapper.columns]) 
        self.writer = csv.DictWriter(sys.stdout, header)

    def writeheader(self):
        self.writer.writeheader()

    def writerows(self, iterable):
        for obj in iterable:
            row = self.mapper.composite_property.dump(obj)
            self.writer.writerow(row)

    def add_all(self, iterable):
        self.writerows(iterable)
