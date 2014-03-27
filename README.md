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
An example mapping of the domain to a document:
```
>>> from mapping_tools import document
>>> penguin_doc = document.Document(
...                   document.Member('name'),
...                   document.Member('mood'),
...                   document.Member('id'))
>>> goose_doc = document.Document(
...                 document.Member('name'),
...                 document.Member('favorite_penguin', penguin_doc),
...                 document.Member('id'))
>>> doc_metadata = document.MetaData()
>>> goose_doc_mapper = document.Mapper(Goose, goose_doc, doc_metadata, {
...                        'favorite_penguin':document.DocumentProperty(
...                            Penguin, goose_doc.members['favorite_penguin'])
...                    })

```
Mappers can be realized by encoders:
```
>>> fred = Penguin('fred', 'cool')
>>> betty = Goose('betty', fred)
>>>
>>> import json
>>> json.dumps(betty, cls=document.json_encoder(doc_metadata),
...     sort_keys=True) # doctest: +NORMALIZE_WHITESPACE
'{"favorite_penguin": {"id": null, "mood": "cool", "name": "fred"},
  "id": null, "name": "betty"}'

```
Encoders can be realized by repositories:
```
#TODO
>>> goose_doc_mapper.load(json.loads(
...   '{"favorite_penguin": {"mood": "cool", "name": "fred"}, "name": "betty"}'
... ))
< betty, the goose that likes < fred the cool penguin > >

```
The mapping, and repository interfaces are consistent with pure sqlalchemy:
```
>>> import sqlalchemy
>>> import sqlalchemy.orm
>>> from sqlalchemy import Table, Column, Integer, String, ForeignKey
>>> from sqlalchemy import create_engine
>>> from sqlalchemy.orm import sessionmaker
>>> engine = create_engine('sqlite:///:memory:')
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
...                            Goose, goose_relation, {
...                            'favorite_penguin':sqlalchemy.orm.relationship(
...                                Penguin)})
>>> sql_metadata.create_all(engine)
>>> session = sessionmaker(bind=engine)()
>>> session.add(Goose('betty', Penguin('fred', 'cool')))
>>> session.commit()
>>> session.query(Goose).join(Penguin).filter(Penguin.name=='fred').one()
< betty, the goose that likes < fred the cool penguin > >

```
An extension to the sqlalchemy query object enables mappings to aggregate
tables:
```
#TODO
>>> from mapping_tools import table
>>> goose_mv = Table('geese_mv', sql_metadata,
...                  Column('id', Integer, primary_key=True),
...                  Column('name', String(50)),
...                  Column('favorite_penguin$id', Integer),
...                  Column('favorite_penguin$name', String(50)),
...                  Column('favorite_penguin$mood', String(50)))
>>> goose_mv_map = table.Mapper(
...                    Goose, goose_mv, {
...                        'favorite_penguin': table.CompositeProperty(
...                            Penguin, {
...                            'name': goose_mv.c['favorite_penguin$name'],
...                            'mood': goose_mv.c['favorite_penguin$mood'],
...                            'id': goose_mv.c['favorite_penguin$id']})
...                    })
>>> sql_metadata.create_all(engine, (goose_mv,))
>>> from sqlalchemy.sql import select
>>> r = engine.execute(goose_mv_map.dump(Goose('tom', Penguin('jerry', 'fat'))))
>>> sorted((k,v) for k,v in r.last_inserted_params().items())\
... # doctest: +NORMALIZE_WHITESPACE
[('favorite_penguin$id', None), ('favorite_penguin$mood', 'fat'), 
('favorite_penguin$name', 'jerry'), ('id', None), ('name', 'tom')]
>>> select_jerry = select([goose_mv])\
...                    .where(goose_mv.c['favorite_penguin$name']=='jerry')
>>> goose_mv_map.load(engine.execute(select_jerry).first())
< tom, the goose that likes < jerry the fat penguin > >

```
TODO:
- other repositories
- mapping to other domains
- mappings to other document schemas (json-schema.org)
- xml encoder (xmltodict)
