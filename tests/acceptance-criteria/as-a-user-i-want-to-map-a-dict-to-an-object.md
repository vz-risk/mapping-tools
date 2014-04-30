As a **user** I want to **map dict to an object**.

Create the test dict:
```python
>>> import mapping_tools
>>> import sys
>>> sys.path.append('src/mapping_tools')
>>> import tests.data
>>> goose_dict_mapper = mapping_tools.DictMapper(tests.data.Goose)
>>> grace_dict = goose_dict_mapper.map(tests.data.grace)

```
Map the dict to an object:
```python
>>> dict_penguin_schema = mapping_tools.DictSchema(tests.data.Penguin)
>>> dict_penguin_schema.map({'id':None, 'mood':'ugly', 'name':'pen'})
< pen the ugly penguin >
>>> dict_goose_schema = mapping_tools.DictSchema(
...     tests.data.Goose, {'favorite_penguin':dict_penguin_schema})
>>> dict_goose_schema.map(grace_dict)
< grace, the goose that likes < penny the fat penguin > >

```
