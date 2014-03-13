...tools for [mapping](http://martinfowler.com/eaaCatalog/dataMapper.html)
 python
[domain models](http://martinfowler.com/eaaCatalog/domainModel.html). For
example, this domain model:
```
>>> class Penguin(object):
...     def __init__(self, name, mood, id=None):
...         self.name = name
...         self.mood = mood
...         self.id = id
...     def __repr__(self):
...         return '< %s the %s penguin >' % (self.name, self.mood)
...
>>> class Goose(object):
...     def __init__(self, name, favorite_penguin, id=None):
...         self.name = name
...         self.favorite_penguin = favorite_penguin
...         self.id = id
...     def __repr__(self):
...         return '< %s, the goose that likes %s >' \
...                % (self.name, repr(self.favorite_penguin))
...

```
## Mapping domain models to documents
```
>>> from mapping_tools import document
>>> penguin_doc_mapper = document.Mapper(
...     Penguin, document.Document(
...         document.Key('name'),
...         document.Key('mood'),
...         document.Key('id')))
>>> goose_doc_mapper = document.Mapper(
...     Goose, document.Document(
...         document.Key('name'),
...         document.Key('favorite_penguin', Penguin),
...         document.Key('id')))

```
encoding domain objects as document objects:
```
>>> fred = Penguin('fred', 'cool')
>>> betty = Goose('betty', fred)
>>>
>>> import json
>>> json.dumps(betty, cls=document.JSONEncoder, sort_keys=True)\
... # doctest: +NORMALIZE_WHITESPACE
'{"favorite_penguin": {"id": null, "mood": "cool", "name": "fred"},
  "id": null, "name": "betty"}'

```
decoding domain objects from json serialized documents:
```
>>> goose_doc_mapper.load(json.loads(
...   '{"favorite_penguin": {"mood": "cool", "name": "fred"}, "name": "betty"}'
... ))
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
>>> session.query(Goose).join(Penguin).filter(Penguin.name=='fred').one()
< betty, the goose that likes < fred the cool penguin > >

```
## Mapping domain objects to aggregate tables
```
>>> goose_mv = Table('geese_mv', sql_metadata,
...                  Column('id', Integer, primary_key=True),
...                  Column('name', String(50)),
...                  Column('favorite_penguin$id', Integer, primary_key=True),
...                  Column('favorite_penguin$name', String(50)),
...                  Column('favorite_penguin$mood', String(50)))
>>> goose_mv_map = sqlalchemy.orm.mapper(
...                    Goose, goose_mv, non_primary=True, properties={
...                    'favorite_penguin':sqlalchemy.orm.composite(Penguin,
...                        goose_mv.c['favorite_penguin$name'],
...                        goose_mv.c['favorite_penguin$mood'],
...                        goose_mv.c['favorite_penguin$id'])})
>>> sql_metadata.create_all(engine, (goose_mv,))
>>> #TODO: application side materialization
>>> r = engine.execute(goose_mv.insert().values((1, 'tom', 1, 'jerry', 'fat')))
>>> session.query(goose_mv_map).\
...     filter(goose_mv.c['favorite_penguin$name']=='jerry').one()
< betty, the goose that likes < fred the cool penguin > >

```
## Mapping domain models to (other) aggregates
## Mapping domain models to another domain
