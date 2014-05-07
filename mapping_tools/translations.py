import heuristics

def identity(model_properties_to_values):
    return model_properties_to_values

def make_constructor(AnotherPrimeType, prefix, seperator='_'):
    translate = lambda p_to_v: _make_AnotherPrimeType(
        AnotherPrimeType, p_to_v, prefix, seperator)
    return translate

def _make_AnotherPrimeType(AnotherPrimeType, model_properties_to_values,
                           prefix, seperator):
    prime_args = _get_AnotherPrimeType_args_from_model_properties(
        model_properties_to_values, prefix, seperator)
    prime = AnotherPrimeType(**prime_args)
    return {prefix:prime}

def _get_AnotherPrimeType_args_from_model_properties(
        model_properties_to_values, prefix, seperator):
    len_prefix = len(prefix+seperator)
    kwargs = dict((prop[len_prefix:], value)
                  for prop, value in model_properties_to_values.items())
    return kwargs

def make_projection(ValueType, seperator='_'):
    value_properties = heuristics.properties(ValueType)
    translation = lambda p_to_v: _get_projection_args_from_model_properties(
        p_to_v, value_properties, seperator)
    return translation

def _get_projection_args_from_model_properties(
        model_properties_to_values, value_properties, seperator):
    #TODO: how to handle multiple model properties?
    prop, value = model_properties_to_values.items()[0]
    kwargs = dict((prop+seperator+value_prop, getattr(value, value_prop))
                  for value_prop in value_properties)
    return kwargs
