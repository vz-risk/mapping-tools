import heuristics
import mapper
import translations

class DictSchema(mapper.Mapper):

    def __init__(self, ModelPrimeType, keys_to_schema={}):
        self.keys_to_schema = keys_to_schema
        model_properties_to_translation =\
            self._make_translations_for_properties(ModelPrimeType)
        model_properties_to_translation[tuple(keys_to_schema.keys())] =\
            self._translate_with_schema
        super(DictSchema, self).__init__(
            ModelPrimeType, model_properties_to_translation)

    def _make_translations_for_properties(self, ModelPrimeType):
        model_properties_to_translation = {}
        for prop in heuristics.properties(ModelPrimeType):
            if prop not in self.keys_to_schema:
                model_properties_to_translation[prop] = translations.identity
        return model_properties_to_translation

    def _translate_with_schema(self, model_properties_to_values):
        kwargs = {}
        for prop, value in model_properties_to_values.items():
            schema = self.keys_to_schema[prop]
            kwargs[prop] = schema.map(value)
        return kwargs

    def map(self, dict_object):
        model_object = None 
        if dict_object is not None:
            model_object = DictObjectAdaptor(dict_object)
        return super(DictSchema, self).map(model_object)

class DictObjectAdaptor(object):

    def __init__(self, dict_object):
        self.dict_object = dict_object

    def __getattr__(self, attr):
        return self.dict_object[attr]

    def __stattr__(self, attr, value):
        self.dict_object[attr] = value

    def __repr__(self):
        return str(self.dict_object)
