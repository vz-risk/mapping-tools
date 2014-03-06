class DictMetaData:
    keys = {}
    classes = {}

def dict_mapper(cls, plural, keys, metadata):
    metadata.keys[cls] = keys
    metadata.classes[plural] = cls

def json_encoder(metadata):
    return type('DictMapper', (_DictMapper,), {'_metadata':metadata})

import json
class _DictMapper(json.JSONEncoder):
    def default(self, obj):
        if obj.__class__ in self._metadata.classes:
            kv = []
            for key in self._metadata.keys[obj.__class__]:
                try:
                    value = getattr(obj, key)
                    kv.append((key, value))
                except AttributeError:
                    pass
            return dict(kv)
        else:
            raise TypeError('%s is not json serializable' % repr(obj))
    
#def as_mapped_obj(dct, metadata):
#    for key in dct:
#        if key in metadata.classes:
#            dct[key] = _decode(key, dct[key], metadata)
#
#    return dct
#
#def _decode(key, value, metadata):
#    return [metadata.classes[key](**encoded_obj) for encoded_obj in value]
