As a **user** I want to **map an object to a dict**.
```python
>>> import mapping_tools
>>> import json
>>> import sys
>>> sys.path.append('src/mapping_tools')
>>> import tests.data
>>> goose_dict_mapper = mapping_tools.DictMapper(tests.data.Goose)
>>> grace_dict = goose_dict_mapper.map(tests.data.grace)
>>> print(json.dumps(grace_dict, indent=2, sort_keys=True))\
... # doctest: +NORMALIZE_WHITESPACE
{
  "favorite_penguin": {
    "id": null,
    "mood": "fat",
    "name": "penny"
  },
  "id": null,
  "name": "grace"
}

```
