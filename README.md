tools for mapping and serializing python objects using an interface that is 
consistent with sqlalchemy
```
>>> class Penguin(object):
...     def __init__(self, name, mood, id=None):
...         self.name = name
...         self.mood = mood
...         self.id = id
...     def __repr__(self):
...         return '< %s the %s penguin >' % (self.name, self.mood)

```
declaring mappings:
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
>>> relational_mapping = sqlalchemy.orm.mapper(Penguin, penguin_table)
>>> dict_mapping = mapping_tools.dict_mapper(Penguin, plural='penguins',
...                                          keys=('id', 'name', 'mood'),
...                                          metadata=dict_metadata)

```
encoding objects:
```
>>> fred = Penguin(u'fred', u'cool')
>>>
>>> from sqlalchemy import create_engine
>>> from sqlalchemy.orm import sessionmaker
>>> engine = create_engine('sqlite:///:memory:')
>>> relational_metadata.create_all(engine)
>>> session = sessionmaker(bind=engine)()
>>> session.add(fred)
>>> session.commit()
>>>
>>> import json
>>> json.dumps(fred, cls=mapping_tools.json_encoder(dict_metadata))
'{"mood": "cool", "id": 1, "name": "fred"}'

```
decoding objects:
```
>>> Penguin(**json.loads('{"mood": "cool", "id": 1, "name": "fred"}'))
< fred the cool penguin >

```
