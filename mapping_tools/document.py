import json

class Mapper(object):
    
    def __init__(self, model, document, properties):
        #TODO: make _root member implicit
        root = Member('_root', document)
        self.document_property = DocumentProperty(model, root, properties)

    def dump(self, obj):
        return self.document_property.dump(obj)['_root']

    def load(self, dct):
        return self.document_property.load(dct)

class MetaData: 
    
    documents = set()

class Document:

    def __init__(self, metadata, *members):
        metadata.documents.add(self)
        self.members = dict((member.key, member) for member in members)

    def __iter__(self):
        return iter(self.members.values())

class Member:

    #TODO: should the schema be explicitly defined here, or by the mapper
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

#TODO: dump and load should be implemented by the encoder, not the property
def make_JSONEncoder(mapper):
    return type('JSONEncoder', (_JSONEncoder,), 
                {'_mapper':mapper})

class _JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        return self._mapper.dump(obj)
