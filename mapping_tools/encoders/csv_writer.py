import csv 
import sys

class CSVWriter(object):

    def __init__(self, mapping):
        self.mapping = mapping
        header = sorted([column.key for column in self.mapping.columns]) 
        self.writer = csv.DictWriter(sys.stdout, header)

    def writeheader(self):
        self.writer.writeheader()

    def writerows(self, iterable):
        for obj in iterable:
            row = self.mapping.composite_property.dump(obj)
            self.writer.writerow(row)

    def make_session(self):
        return Session(self.writeheader, self.writerows)

class Session:

    def __init__(self, writeheader, writerows):
        self.writeheader = writeheader
        self.writerows = writerows

    def __enter__(self):
        self.writeheader()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass #do nothing

    def add_all(self, iterable):
        self.writerows(iterable)
