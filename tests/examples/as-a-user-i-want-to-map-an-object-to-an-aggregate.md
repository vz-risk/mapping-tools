As a **user** I want to **map an object to an aggregate**.
```python
>>> import mapping_tools
>>> import test_data.zoo
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
>>> penguin_projection = mapping_tools.make_projection(test_data.zoo.Penguin)
>>> goose_aggregate_map = mapping_tools.Mapper(GooseAggregate, {
...     ('name', 'id'):mapping_tools.identity,
...     'favorite_penguin':penguin_projection})
>>> gale_aggregate = goose_aggregate_map.map(test_data.zoo.gale)
>>> gale_aggregate
< gale the goose has a cool penguin mood >

```
