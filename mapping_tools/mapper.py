class Mapper(object):
    
    def __init__(self, ModelPrimeType, 
                 model_properties_to_translation):
        self.ModelPrimeType = ModelPrimeType
        self.model_properties_to_translation = model_properties_to_translation

    def map(self, model_object):
        if model_object is None:
            return None 
            # this prevents the constructor of the ModelPrime type
            # from beign called with null args when the ModelType is None
            # instead, None objects always map to None
        else:
            return self.ModelPrimeType(**self._translate_kwargs(model_object))

    def _translate_kwargs(self, model_object):
        kwargs = {}
        for model_properties in self.model_properties_to_translation:
            model_properties_to_values = self._map_properties_to_values(
                model_properties, model_object)
            translate = self.model_properties_to_translation[model_properties]
            kwargs.update(translate(model_properties_to_values))
        return kwargs

    @staticmethod
    def _map_properties_to_values(properties, obj):
        properties = Mapper._get_tuple_if_string(properties)
        properties_to_values = dict((prop, getattr(obj, prop)) 
                                    for prop in properties
                                    if hasattr(obj, prop))
        return properties_to_values

    @staticmethod
    def _get_tuple_if_string(obj):
        if isinstance(obj, basestring):
            return (obj,)
        else:
            return obj
            
