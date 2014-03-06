from collections import Mapping
import json

class DictMetaData(Mapping):
    
    _mapped_keys = {}

    def __getitem__(self, cls):
        return self._mapped_keys[cls]

    def __setitem__(self, cls, mapped_keys):
        self._mapped_keys[cls] = mapped_keys

    def __iter__(self):
        return iter(self._mapped_keys)

    def __len__(self):
        return len(self._mapped_keys)

def dict_mapper(cls, keys, metadata):
    metadata[cls] = keys

def json_encoder(metadata):
    return type('DictMapper', (_DictMapper,), {'_metadata':metadata})

class _DictMapper(json.JSONEncoder):
    def default(self, obj):
        if obj.__class__ in self._metadata:
            kv = []
            for key in self._metadata[obj.__class__]:
                try:
                    value = getattr(obj, key)
                    kv.append((key, value))
                except AttributeError:
                    pass
            return dict(kv)
        else:
            raise TypeError('%s is not json serializable' % repr(obj))
    
