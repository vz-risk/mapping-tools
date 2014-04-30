import heuristics
import mapper
import translations

class DictSchema(mapper.Mapper):

    def __init__(self, ModelPrimeType, keys_to_schema={}):
        model_properties_to_translation =\
            self._make_translations_for_properties(ModelPrimeType)
        model_properties_to_translation.update(
            self._make_translations_for_schema(keys_to_schema))
        super(DictSchema, self).__init__(
            ModelPrimeType, model_properties_to_translation)

    @staticmethod
    def _make_translations_for_properties(ModelPrimeType):
        model_properties_to_translation = {}
        for prop in heuristics.properties(ModelPrimeType):
            model_properties_to_translation[prop] = translations.identity
        return model_properties_to_translation

    @staticmethod
    def _make_translations_for_schema(keys_to_schema):
        model_properties_to_translation = {}
        for key, schema in keys_to_schema.items():
            model_properties_to_translation[key] =\
                lambda ptov: DictSchema._translate_with_schema(ptov, schema)
        return model_properties_to_translation

    @staticmethod
    def _translate_with_schema(model_properties_to_values, schema):
        first_property, first_value = model_properties_to_values.items()[0]
        kwargs = {first_property:schema.map(first_value)}
        return kwargs

    def map(self, dict_object):
        return super(DictSchema, self).map(DictObjectAdaptor(dict_object))

class DictObjectAdaptor:

    def __init__(self, dict_object):
        self.dict_object = dict_object

    def __getattr__(self, attr):
        return self.dict_object[attr]

    def __stattr__(self, attr, value):
        self.dict_object[attr] = value
