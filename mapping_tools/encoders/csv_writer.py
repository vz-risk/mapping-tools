import csv 
import sys

class CSVWriter(object):

    def __init__(self, mapping, columns=None):
        self.mapping = mapping
        self.header = columns if columns is not None else \
                      sorted([column.key for column in self.mapping.columns]) 
        self.writer = csv.DictWriter(sys.stdout, self.header)

    def writeheader(self):
        self.writer.writeheader()

    def writerows(self, iterable):
        for obj in iterable:
            row = self._filter_columns(
                self.mapping.composite_property.dump(obj))
            self.writer.writerow(row)

    def _filter_columns(self, row):
        row = dict((key, value) 
                   for key, value in row.items() if key in self.header)
        return row

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
