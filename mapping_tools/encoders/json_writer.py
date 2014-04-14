import json
import sys

import mapping_tools.mappers.document

class JSONWriter(object):
    
    def __init__(self, mapping):
        self.JSONEncoder = mapping_tools.mappers.document.make_JSONEncoder(
            mapping)

    def make_session(self):
        return Session(self.JSONEncoder)

class Session:

    def __init__(self, JSONEncoder):
        self.JSONEncoder = JSONEncoder

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass #do nothing

    def add_all(self, iterable):
        json.dump(list(iterable), sys.stdout, cls=self.JSONEncoder, indent=2)
