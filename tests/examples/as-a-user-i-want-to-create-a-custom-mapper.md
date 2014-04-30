As a **user** I want to **create a custom mapper**.
```python
>>> import mapping_tools
>>> import sys
>>> sys.path.append('src/mapping_tools')
>>> import tests.data
>>> tokens = {
...     'grace':'fred',
...     'gail':'frank',
...     'ginger':'frankenstein'
... }
>>> def tokenize_values(model_property_names_to_values):
...     nv_items = model_property_names_to_values.items()
...     tokenized = dict((name, tokens[value]) for name, value in nv_items)
...     return tokenized
>>> anonymizer = mapping_tools.Mapper(tests.data.Goose, {
...     'name':tokenize_values,
...     ('favorite_penguin', 'id'):mapping_tools.identity})
>>> anonymizer.map(tests.data.ginger)
< frankenstein, the goose that likes < puck the boring penguin > >

```
