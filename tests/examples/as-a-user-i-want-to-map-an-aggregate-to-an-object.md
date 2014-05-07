As a **user** I want to **map an aggregate to an object**.

Create the test aggregate:
```python
>>> class GooseAggregate(object):
...     def __init__(self, name, favorite_penguin_name, favorite_penguin_mood,
...                  favorite_penguin_id=None, id=None):
...         self.name = name
...         self.favorite_penguin_name = favorite_penguin_name
...         self.favorite_penguin_mood = favorite_penguin_mood
...         self.favorite_penguin_id = favorite_penguin_id
...         self.id = id
...     def __repr__(self):
...         template = '< %s the goose has a %s penguin mood >' 
...         return template % (self.name, self.favorite_penguin_mood)
...
>>> gale_aggregate = GooseAggregate('gale', 'prince', 'cool')

```
Map the aggregate to an object:
```python
>>> import mapping_tools
>>> import test_data.zoo
>>> penguin_properties = ('favorite_penguin_name', 'favorite_penguin_mood',
...                       'favorite_penguin_id')
>>> aggregate_goose_schema = mapping_tools.Mapper(test_data.zoo.Goose, {
...     ('name', 'id'):mapping_tools.identity,
...     penguin_properties:mapping_tools.make_constructor(
...         test_data.zoo.Penguin, 'favorite_penguin')})
>>> aggregate_goose_schema.map(gale_aggregate)
< gale, the goose that likes < prince the cool penguin > >

```
