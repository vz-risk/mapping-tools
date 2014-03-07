...tools for mapping python objects. Like these objects:
```
>>> class Penguin(object):
...     def __init__(self, name, mood):
...         self.name = name
...         self.mood = mood
...     def __repr__(self):
...         return '< %s the %s penguin >' % (self.name, self.mood)
...
>>> class Goose(object):
...     def __init__(self, name, favorite_penguin):
...         self.name = name
...         self.favorite_penguin = favorite_penguin
...     def __repr__(self):
...         return '< %s, the goose that likes %s >' \
...                % (self.name, repr(self.favorite_penguin))
...

```
## Mapping objects to documents

declaring mappings:
```
>>> import mapping_tools
>>> document_metadata = mapping_tools.DocumentMetaData()
>>> mapping_tools.map_to_document(
...     Penguin, 'penguns', document_metadata,
...     mapping_tools.Key('name'),
...     mapping_tools.Key('mood'),
...     mapping_tools.Key('id'))
>>> mapping_tools.map_to_document(
...     Goose, 'geese', document_metadata,
...     mapping_tools.Key('name'),
...     mapping_tools.Key('favorite_penguin', Penguin),
...     mapping_tools.Key('id'))

```
encoding objects as documents and serializing documents as json:
```
>>> fred = Penguin('fred', 'cool')
>>> betty = Goose('betty', fred)
>>>
>>> import json
>>> json.dumps(betty, cls=mapping_tools.document_encoder(document_metadata),
...            sort_keys=True)
'{"favorite_penguin": {"mood": "cool", "name": "fred"}, "name": "betty"}'

```
decoding objects from json serialized documents:
```
>>> goose_doc = json.loads(
...   '{"favorite_penguin": {"mood": "cool", "name": "fred"}, "name": "betty"}')
>>> mapping_tools.decode_document(goose_doc, Goose, document_metadata)
< betty, the goose that likes < fred the cool penguin > >

```
