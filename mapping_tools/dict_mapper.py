import inspect
import types

import mapper
import translations

class DictMapper(mapper.Mapper):

    primitive_types = (types.BooleanType, types.DictType, types.DictionaryType,
                       types.FloatType, types.IntType, types.LongType,
                       types.NoneType, types.StringType, types.StringTypes,
                       types.UnicodeType)

    def __init__(self, ModelType):
        model_properties_to_translation = {
            self._inspect_properties(ModelType):self._make_dict}
        super(DictMapper, self).__init__(dict, model_properties_to_translation)

    @staticmethod
    def _inspect_properties(ModelType):
        args = set(inspect.getargspec(ModelType.__init__).args)
        properties = tuple(args - set(('self',)))
        return properties

    @staticmethod
    def _make_dict(model_property_names_to_values):
        #TODO: some of this logic could be handled by the base Mapper for
        #more natural handling of nested types
        kwargs = {}
        for prop, value in model_property_names_to_values.items():
            if isinstance(value, DictMapper.primitive_types): 
                kwargs[prop] = value
            else:
                kwargs[prop] = DictMapper._make_nested_dict(value)
        return kwargs

    @staticmethod
    def _make_nested_dict(obj):
        properties = DictMapper._inspect_properties(type(obj))
        p_to_v = mapper.Mapper._map_properties_to_values(properties, obj)
        nested_dict = DictMapper._make_dict(p_to_v)
        return nested_dict
