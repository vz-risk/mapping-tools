...tools for mapping python
[domain models](http://martinfowler.com/eaaCatalog/domainModel.html). For
example, this domain model:
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
## Mapping domain models to documents
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
```
#>>> import mapping_tools
#>>> document_strategy = mapping_tools.DocumentStrategy()
#>>> document_strategy.add_mapping(Penguin, keys=('name', 'mood', 'id'))
#>>> document_strategy.add_mapping(Penguin,
#...                               keys=('name', 'favorite_penguin', 'id'),
#...                               value_types={'favorite_penguin':Penguin})
#
```
encoding domain objects as document objects:
```
>>> fred = Penguin('fred', 'cool')
>>> betty = Goose('betty', fred)
>>>
>>> import json
>>> json.dumps(betty, cls=mapping_tools.document_encoder(document_metadata),
...            sort_keys=True)
'{"favorite_penguin": {"mood": "cool", "name": "fred"}, "name": "betty"}'

```
```
#>>> import json
#>>> json.dumps(betty, cls=mapping_tools.document_encoder(goose_mapping),
#>>>            sort_keys=True)

```
decoding domain objects from json serialized documents:
```
>>> goose_doc = json.loads(
...   '{"favorite_penguin": {"mood": "cool", "name": "fred"}, "name": "betty"}')
>>> mapping_tools.decode_document(goose_doc, Goose, document_metadata)
< betty, the goose that likes < fred the cool penguin > >

```
## Mapping domain models to relations
```
>>> import sqlalchemy
>>> import sqlalchemy.orm
>>> from sqlalchemy import Table, Column, Integer, String, ForeignKey
>>> 
>>> sql_metadata = sqlalchemy.MetaData()
>>> penguin_relation = Table('penguins', sql_metadata,
...                          Column('id', Integer, primary_key=True),
...                          Column('name', String(50)),
...                          Column('mood', String(50)))
>>> goose_relation = Table('geese', sql_metadata,
...                        Column('id', Integer, primary_key=True),
...                        Column('name', String(50)),
...                        Column('favorite_penguin$id', Integer,
...                            ForeignKey('penguins.id')))
>>> penguin_relational_map = sqlalchemy.orm.mapper(Penguin, penguin_relation)
>>> goose_relational_map = sqlalchemy.orm.mapper(
...                            Goose, goose_relation, properties={
...                            'favorite_penguin':sqlalchemy.orm.relationship(
...                                Penguin)})

```
encoding, querying, and decoding domain objects as tuples
```
>>> from sqlalchemy import create_engine
>>> from sqlalchemy.orm import sessionmaker
>>> engine = create_engine('sqlite:///:memory:')
>>> sql_metadata.create_all(engine)
>>> session = sessionmaker(bind=engine)()
>>> session.add(Goose('betty', Penguin('fred', 'cool')))
>>> session.commit()
>>> session.query(Goose).join(Penguin).filter(Penguin.name=='fred').first()
< betty, the goose that likes < fred the cool penguin > >

```
## Mapping domain objects to aggregate tables
```
>>> goose_mv = Table('geese_mv', sql_metadata,
...                  Column('id', Integer, primary_key=True),
...                  Column('name', String(50)),
...                  Column('favorite_penguin$id', Integer, primary_key=True),
...                  Column('favorite_penguin$name', String(50)))
>>> goose_mv_map = sqlalchemy.orm.mapper(
...                    Goose, goose_mv, non_primary=True, properties={
...                    'favorite_panguin':sqlalchemy.orm.composite(Penguin,
...                        goose_mv.c['favorite_penguin$name'],
...                        goose_mv.c['favorite_penguin$id'])})
>>> sql_metadata.create_all(engine, (goose_mv,))
>>> #TODO: application side materialization
>>> r = engine.execute(goose_mv.insert().values((1, 'betty', 1, 'fred')))
>>> session.query(Goose).select_from(goose_mv).\
...     filter(goose_mv.c['favorite_penguin$name']=='fred').first()
< betty, the goose that likes < fred the cool penguin > >

```
## Mapping domain models to (other) aggregates
## Mapping domain models to another domain
