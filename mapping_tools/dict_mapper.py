import types
import datetime

import heuristics
import mapper

class DictMapper(mapper.Mapper):

    primitive_types = (types.BooleanType, types.DictType, types.DictionaryType,
                       types.FloatType, types.IntType, types.LongType,
                       types.NoneType, types.StringType, types.StringTypes,
                       types.UnicodeType, types.ListType, datetime.datetime)

    def __init__(self, ModelType):
        self.ModelType = ModelType
        model_properties_to_translation = {
            heuristics.properties(ModelType):self._make_dict}
        super(DictMapper, self).__init__(dict, model_properties_to_translation)

    @staticmethod
    def _make_dict(model_properties_to_values):
        #TODO: some of this logic could be handled by the base Mapper for
        #more natural handling of nested types
        kwargs = {}
        for prop, value in model_properties_to_values.items():
            if isinstance(value, DictMapper.primitive_types): 
                kwargs[prop] = value
            else:
                kwargs[prop] = DictMapper._make_nested_dict(value)
        return kwargs

    @staticmethod
    def _make_nested_dict(obj):
        properties = heuristics.properties(type(obj))
        p_to_v = mapper.Mapper._map_properties_to_values(properties, obj)
        nested_dict = DictMapper._make_dict(p_to_v)
        return nested_dict
