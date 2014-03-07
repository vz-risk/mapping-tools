import json
from collections import defaultdict

class DocumentMetaData:

    def __init__(self):
        self._cls_to_key_map = defaultdict(lambda: {})

    def add_keys(self, cls, *keys):
        for key in keys:
            self._cls_to_key_map[cls][key.name] = key

    def get_key(self, cls, key_name):
        return self._cls_to_key_map[cls][key_name]

    def get_keys(self, cls):
        return self._cls_to_key_map[cls].values()

    def has_class(self, cls): 
        return cls in self._cls_to_key_map

class Key:

    def __init__(self, name, value_type=None):
        self.name = name
        self.value_type = value_type
        
def map_to_document(cls, plural, metadata, *keys):
    metadata.add_keys(cls, *keys)

def document_encoder(metadata):
    return type('DocumentEncoder', (_DocumentEncoder,), {'_metadata':metadata})

class _DocumentEncoder(json.JSONEncoder):
    def default(self, obj):
        if self._metadata.has_class(obj.__class__):
            kv = []
            for key in self._metadata.get_keys(obj.__class__):
                try:
                    value = getattr(obj, key.name)
                    kv.append((key.name, value))
                except AttributeError:
                    pass
            return dict(kv)
        else:
            raise TypeError('%s is not json serializable' % repr(obj))
    
def decode_document(dct, cls, metadata):
    for key in dct:
        value_type = metadata.get_key(cls, key).value_type
        if value_type is not None:
            dct[key] = decode_document(dct[key], value_type, metadata)

    return cls(**dct)
#
#def _decode(key, value, metadata):
#    return [metadata.classes[key](**encoded_obj) for encoded_obj in value]
