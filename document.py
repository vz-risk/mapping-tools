import json

class Mapper(object):
    
    def __init__(self, model, document, metadata, properties):
        #TODO: make _root member implicit
        root = Member('_root', document)
        self.document_property = DocumentProperty(model, root, properties)
        metadata.set_mapper(model, self)

    def dump(self, obj):
        return self.document_property.dump(obj)['_root']

    def load(self, dct):
        return self.document_property.load(dct)

class MetaData: 
    
    _model_to_mapper = {}

    def set_mapper(self, model, mapper):
        self._model_to_mapper[model] = mapper

    def get_mapper(self, obj):
        model = obj.__class__
        return self._model_to_mapper[model]

class Document:

    def __init__(self, *members):
        self.members = dict((member.key, member) for member in members)

    def __iter__(self):
        return iter(self.members.values())

class Member:

    def __init__(self, key, schema=None):
        self.key = key
        self.schema = schema
        
class MemberProperty:

    def __init__(self, member):
        self.member = member

    def dump(self, obj):
        return {self.member.key: obj}

    def load(self, value):
        return value

class DocumentProperty:

    def __init__(self, model, member, properties={}):
        self.model = model
        self.member = member
        properties.update(
            self._automap_unmapped_members(member.schema, properties))
        self.properties = properties
        self._key_to_propname = dict((prop.member.key, propname) 
                                     for propname, prop 
                                     in self.properties.items())

    @staticmethod
    def _automap_unmapped_members(document, properties):
        automapped_properties = {}
        for member in document:
            if member.key not in properties:
                automapped_properties[member.key] = MemberProperty(member)
    
        return automapped_properties

    def dump(self, obj):
        doc = {}
        for prop_name, prop in self.properties.items():
            value = getattr(obj, prop_name)
            doc.update(prop.dump(value))

        return {self.member.key: doc}

    def load(self, dct):
        for key, value in dct.items():
            propname = self._key_to_propname[key]
            dct[key] = self.properties[propname].load(value)
    
        return self.model(**dct)

def json_encoder(doc_metadata):
    return type('JSONEncoder', (_JSONEncoder,), 
                {'_doc_metadata':doc_metadata})

class _JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        mapper = None
        try:
            mapper = self._doc_metadata.get_mapper(obj)
        except ValueError: #obj not a mapped model
            return obj
        return mapper.dump(obj)
