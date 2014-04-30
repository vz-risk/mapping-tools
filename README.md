```
pip install git+ssh://git@github.com/natb1/mapping_tools.git
```
...tools for "mapping" python models. For example, this model:
```python
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
...         template = '< %s, the goose that likes %s >'
...         return template % (self.name, repr(self.favorite_penguin))
...

```
Some model objects:
```python
>>> grace = Goose('grace', Penguin('penny', 'fat'))
>>> gale = Goose('gale', Penguin('prince', 'cool'))
>>> ginger = Goose('ginger', Penguin('puck', 'boring'))

```

## Mappers
Mapper instances define translations between models. They have a factory
method `map` that takes a `ModelType` object as an argument and initializes and
returns an object of `ModelPrimeType`.

> #### Magic Mappers
`mapping_tools` is packaged with a number of "magic" mappers that
use various heuristics to guess the best mapping.
`mapping_tools.DictMapper(ModelType)` inspects the `ModelType` constructor to
return a mapper instance whose `map` method constructs dict objects:
```python
>>> import mapping_tools
>>> import json
>>> goose_dict_mapper = mapping_tools.DictMapper(Goose)
>>> grace_dict = goose_dict_mapper.map(grace)
>>> print(json.dumps(grace_dict, indent=2, sorted=True))\
... # doctest: +NORMALIZE_WHITESPACE
{
  "favorite_penguin": {
    "id": null,
    "mood": "fat",
    "name": "penny"
  },
  "id": null
  "name": "grace",
}

>```
>`mapping_tools.DictSchema(ModelPrimeType, keys_to_schema={})`
is a mapper with a map method that takes a `dict` and returns a
`ModelPrimeType`.
```python
>>> dict_penguin_schema = mapping_tools.DictSchema(Penguin)
>>> dict_goose_schema = mapping_tools.DictSchema(
...     Goose, {'favorite_penguin':dict_penguin_schema})
>>> dict_goose_schema.map(grace_dict)
< grace, the goose that likes < penny the fat penguin > >

>```
> `mapping_tools.AggregateMapper(ModelType, aggregate_type)` returns a
mapper instance that inspects the constructors of the `ModelType` and
`aggregate_type` to guess possible aggregations:
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
>>> goose_aggregate_mapper = mapping_tools.AggregateMapper(
...     Goose, GooseAggregate)
>>> aggregate_goose_mapper = mapping_tools.AggregateMapper(
...     Goose, GooseAggregate, inverse=True)
>>> gale_aggregate = goose_aggregate_mapper.map(gale)
>>> gale_aggregate
< gale has a cool penguin mood >
>>> aggregate_goose_mapper(gale_aggregate)
< gale, the goose that likes < prince the cool penguin > >

>```

Custom translations can be defined using the generic `Mapper`.
```python
class mapping_tools.Mapper(ModelPrimeType, model_properties_to_translation)
```  
... initialize a mapper for translating `model` objects to `model_prime` 
objects. `model_properties_to_translation` is a
[`mapping`](https://docs.python.org/2/library/stdtypes.html#mapping-types-dict)
from model property names to translation functions. Translation functions look
like:
```python
def my_translation_function(model_properties_to_values)
```
... return a
[`mapping`](https://docs.python.org/2/library/stdtypes.html#mapping-types-dict)
of keyword arguments to be passed to the `ModelPrimeType` constructor. Some 
common translation functions are packaged with `mapping_tools`.
> #### Translation Functions
```python
mapping_tools.identity(model_properties_to_values)
```
returns model_properties_to_values
```python
mapping_tools.make_rotation(prime_property_name)
```
makes a translation function that returns {prime_property_name:value}
```python
mapping_tools.make_projection(value_property_name_to_prime_property_name)
```
makes a translation function that returns 
{prime_property_name:value.value_property_name, ...}
```python
mapping_tools.make_constructor(another_prime_type, prime_property_name)
```
makes a transation function that returns 
{prime_property_name:another_prime_type(**model_properties_to_values)}

For example, mapping to an anonymized domain:
```python
>>> tokens = {
...     'grace':'fred',
...     'gail':'frank',
...     'ginger':'frankenstein'
... }
>>> def tokenize_values(model_properties_to_values):
...     tokenized = dict(
...         (name, tokens[value])
...         for name, value in model_properties_to_values.items())
...     return tokenized
>>> anonymizer = mapping_tools.Mapper(Goose, {
...     'name':tokenize_values,
...     ('favorite_penguin', 'id'):mapping_tools.identity})
>>> anonymizer.map(ginger)
< frankenstein, the goose that likes < puck the boring penguin > >

```

