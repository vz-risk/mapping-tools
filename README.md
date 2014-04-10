```
pip install git+ssh://git@github.com/natb1/mapping_tools.git
```
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
## Mappers
An example mapping of the domain to a document:
```
>>> from mapping_tools import document
>>> doc_metadata = document.MetaData()
>>> penguin_doc = document.Document(
...                   doc_metadata,
...                   document.Member('name'),
...                   document.Member('mood'),
...                   document.Member('id'))
>>> goose_doc = document.Document(
...                 doc_metadata,
...                 document.Member('name'),
...                 document.Member('favorite_penguin', penguin_doc),
...                 document.Member('id'))
>>> goose_doc_mapper = document.Mapper(Goose, goose_doc, {
...                        'favorite_penguin':document.DocumentProperty(
...                            Penguin, goose_doc.members['favorite_penguin'])
...                    })

```
ORM using pure SQLAlchemy:
```
>>> import sqlalchemy
>>> import sqlalchemy.orm
>>> from sqlalchemy import Table, Column, Integer, String, ForeignKey
>>> table_metadata = sqlalchemy.MetaData()
>>> penguin_relation = Table('penguins', table_metadata,
...                          Column('id', Integer, primary_key=True),
...                          Column('name', String(50)),
...                          Column('mood', String(50)))
>>> goose_relation = Table('geese', table_metadata,
...                        Column('id', Integer, primary_key=True),
...                        Column('name', String(50)),
...                        Column('favorite_penguin$id', Integer,
...                            ForeignKey('penguins.id')))
>>> penguin_relational_map = sqlalchemy.orm.mapper(Penguin, penguin_relation)
>>> goose_relational_map = sqlalchemy.orm.mapper(
...                            Goose, goose_relation, {
...                            'favorite_penguin':sqlalchemy.orm.relationship(
...                                Penguin)})

```
Map a model to an aggregate table:
```
>>> import mapping_tools.mappers.table
>>> aggregate_metadata = sqlalchemy.MetaData()
>>> goose_aggregate = Table('geese_aggregate', aggregate_metadata,
...                  Column('id', Integer, primary_key=True),
...                  Column('name', String(50)),
...                  Column('favorite_penguin$id', Integer),
...                  Column('favorite_penguin$name', String(50)),
...                  Column('favorite_penguin$mood', String(50)))
>>> goose_aggregate_map = mapping_tools.mappers.table.Mapper(
...     Goose, goose_aggregate, {
...         'favorite_penguin': mapping_tools.mappers.table.CompositeProperty(
...             Penguin, {
...             'name': goose_aggregate.c['favorite_penguin$name'],
...             'mood': goose_aggregate.c['favorite_penguin$mood'],
...             'id': goose_aggregate.c['favorite_penguin$id']})
...     })

```
## Encoders
Mappers can be used by encoders:
```
>>> grace = Goose('grace', Penguin('jerry', 'fat'))
>>> betty = Goose('betty', Penguin('fred', 'cool'))
>>> ginger = Goose('ginger', Penguin('larry', 'boring'))

```
```
>>> import json
>>> JSONEncoder = document.make_JSONEncoder(goose_doc_mapper)
>>> json.dumps(betty, cls=JSONEncoder, sort_keys=True) \
... # doctest: +NORMALIZE_WHITESPACE
'{"favorite_penguin": {"id": null, "mood": "cool", "name": "fred"},
  "id": null, "name": "betty"}'
>>> goose_doc_mapper.load(json.loads(
...   '{"favorite_penguin": {"mood": "cool", "name": "fred"}, "name": "betty"}'
... ))
< betty, the goose that likes < fred the cool penguin > >

```
Table mappings can be used by csv encoders. csv encoder interface is
consistent with csv writer from python libs:
```
>>> import mapping_tools.repositories.csv_writer
>>> writer = mapping_tools.repositories.csv_writer.CSVWriter(
...     goose_aggregate_map)
>>> writer.writeheader() # doctest: +NORMALIZE_WHITESPACE
favorite_penguin$id,favorite_penguin$mood,favorite_penguin$name,id,name
>>> writer.writerows((grace, betty)) # doctest: +NORMALIZE_WHITESPACE
,fat,jerry,,grace
,cool,fred,,betty

```
Extensions to the csv writer interface implement the mapping_tools encoder
interface:
```
>>> writer.add_all((grace, betty)) # doctest: +NORMALIZE_WHITESPACE
,fat,jerry,,grace
,cool,fred,,betty

```
## Repositories
Repositories are encoders that also implement persistance and querying
strategies:
```
#TODO
>>> from sqlalchemy import create_engine
>>> from sqlalchemy.orm import sessionmaker
>>> engine = create_engine('sqlite:///:memory:')
>>> 
>>> table_metadata.create_all(engine)
>>> session = sessionmaker(bind=engine)()
>>> session.add(Goose('betty', Penguin('fred', 'cool')))
>>> session.commit()
>>> session.query(Goose).join(Penguin).filter(Penguin.name=='fred').one()
< betty, the goose that likes < fred the cool penguin > >

```
```
#TODO
>>> aggregate_metadata.create_all(engine)
>>> from sqlalchemy.sql import select
>>> r = engine.execute(goose_aggregate_map.table.insert(), 
...                    **goose_aggregate_map.dump(grace))
>>> sorted((k,v) for k,v in r.last_inserted_params().items())\
... # doctest: +NORMALIZE_WHITESPACE
[('favorite_penguin$id', None), ('favorite_penguin$mood', 'fat'),
('favorite_penguin$name', 'jerry'), ('id', None), ('name', 'grace')]
>>> select_jerry = select([goose_aggregate])\
...                    .where(goose_aggregate.c['favorite_penguin$name']=='jerry')
>>> goose_aggregate_map.load(engine.execute(select_jerry).first())
< grace, the goose that likes < jerry the fat penguin > >

```
TODO:
- other repositories
- mapping to other domains
- mappings to other document schemas (json-schema.org)
- xml encoder (xmltodict)
- sqla query subclass that chooses best mapper
