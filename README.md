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
method `map` that takes a model object as an argument and returns objects 
of a different model. 

> #### Magic Mappers
`mapping_tools` is packaged with a number of "magic" mappers that
use various heuristics to guess the best mapping.
`mapping_tools.DictMapper(model_type)` inspects the `model_type` constructor to
return a mapper instance whose `map` method constructs dict objects:
```python
>>> import mapping_tools
>>> import json
>>> goose_dict_mapper = mapping_tools.DictMapper(Goose)
>>> grace_dict = goose_dict_mapper.map(grace)
>>> print(json.dumps(grace_dict, indent=2, sorted=True))\
... # doctest: +NORMALIZE_WHITESPACE
[
  {
    "favorite_penguin": {
      "id": null,
      "mood": "fat",
      "name": "penny"
    },
    "name": "grace",
    "id": null
  }
]

>```
> The `inverse` argument of the `DictMapper` constructor will return an
instance whose `map` method takes a `dict` argument and initializes a
`model_type` object:
```python
>>> dict_goose_mapper = mapping_tools.DictMapper(Goose, inverse=True)
>>> dict_goose_mapper.map(grace_dict)
< grace, the goose that likes < penny the fat penguin > >

>```
> `mapping_tools.AggregateMapper(model_type, aggregate_type)` returns a
mapper instance that inspects the constructors of the `model_type` and
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
class mapping_tools.Mapper(model_type, model_prime_type, 
                           model_property_to_prime_property)
```  
... initialize a mapper for translating `model` objects to `model_prime` 
objects. `model_property_to_prime_property` is a
[`mapping`](https://docs.python.org/2/library/stdtypes.html#mapping-types-dict)
from model property names to translation functions. Translation functions look
like:
```python
def my_translation_function(**model_property_names_to_values)
```
... return a
[`mapping`](https://docs.python.org/2/library/stdtypes.html#mapping-types-dict)
of keyword arguments to be passed to the `model_prime_type` constructor. Some 
common translation functions are packaged with `mapping_tools`.
> #### Translation Functions
```python
mapping_tools.identity(**model_property_names_to_values)
```
returns model_property_names_to_values
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
{prime_property_name:another_prime_type(**model_property_names_to_values)}

For example, mapping to an anonymized domain:
```python
>>> tokens = {
...     'grace':'fred',
...     'gail':'frank',
...     'ginger':'frankenstein'
... }
>>> def tokenize_values(**model_property_names_to_values):
...     nv_items = model_property_names_to_values.items()
...     tokenized = dict(name, tokens[value] for name, value in nv_items)
...     return tokenized
>>> tokenizer = mapping_tools.Mapper(Goose, Goose, {
...     'name':tokenize_values,
...     ('favorite_penguin', 'id'):mapping_tools.identity})
>>> anonymous_goose = tokenizer.map(ginger)
>>> anonymous_goose
< frankenstein, the goose that likes < puck the boring penguin > >

```


