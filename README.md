tools for serializing python objects with an interface that is consistent with 
sqlalchemy
```
>>> class Penguin(object):
...     def __init__(self, name, mood):
...         self.name = name
...         self.mood = mood

```
```
>>> import mapping_tools
>>> import sqlalchemy
>>> from sqlalchemy import Table, Column, Integer, Unicode
>>> import sqlalchemy.orm.mapper
>>> 
>>> relational_metadata = sqlalchemy.MetaData()
>>> dict_metadata = mapping_tools.DictMetaData()
>>> 
>>> penguin_table = Table('penguins', relational_metadata,
...                       Column('id', Integer, primary_key=True),
...                       Column('name', Unicode(50)),
...                       Column('mood', Unicode(50)),
...                      )
>>> 
>>> sqla_mapping = sqlalchemy.orm.mapper(Penguin, penguin_table)
>>> mapping_tools.dict_mapper(Penguin, keys=('id', 'name', 'mood'),
...                           metadata=dict_metadata)

```
```
>>> fred = Penguin('fred', 'cool')
>>>
>>> import json
>>> print(json.dumps(fred, cls=mapping_tools.json_encoder(dict_metadata)))
{"mood": "cool", "id": null, "name": "fred"}
>>> from sqlalchemy import create_engine
>>> from sqlalchemy.orm import sessionmaker
>>> engine = create_engine('sqlite:///:memory:')
>>> session = sessionmaker(bind=engine)()
>>> session.add(fred)

```
