import json

_mapper_registry = {}

class Mapper(object):
    
    def __init__(self, model, document):
        self.document = document
        self.model = model
        _mapper_registry[model] = self

    def get_document(self):
        return self.document

    def load(self, dct):
        for key_name in dct:
            nested_model = self.document.get_key(key_name).model
            if nested_model is not None:
                nested_obj = dct[key_name]
                nested_mapper = _mapper_registry[nested_model]
                dct[key_name] = nested_mapper.load(nested_obj)
    
        return self.model(**dct)

class Document:

    def __init__(self, *keys):
        self.keys = keys
        self._key_names_to_key = dict([(key.name, key) for key in keys])

    def __iter__(self):
        return iter(self.keys)

    def get_key(self, key_name):
        return self._key_names_to_key[key_name]

class Key:

    def __init__(self, name, model=None):
        self.name = name
        self.model = model
        
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        kv = []
        for key in _mapper_registry[obj.__class__].get_document():
            try:
                value = getattr(obj, key.name)
                kv.append((key.name, value))
            except AttributeError:
                pass
        return dict(kv)
    
