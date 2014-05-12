import heuristics

def identity(model_properties_to_values):
    return model_properties_to_values

def make_constructor(AnotherPrimeType, prefix, rotations={}, seperator='_'):
    #TODO: "roations" is a hack. There should be some sort of nested mapper
    translate = lambda p_to_v: _make_AnotherPrimeType(
        AnotherPrimeType, p_to_v, prefix, rotations, seperator)
    return translate

def _make_AnotherPrimeType(AnotherPrimeType, model_properties_to_values,
                           prefix, rotations, seperator):
    prime_args = _get_AnotherPrimeType_args_from_model_properties(
        model_properties_to_values, prefix, rotations, seperator)
    prime = AnotherPrimeType(**prime_args)
    return {prefix:prime}

def _get_AnotherPrimeType_args_from_model_properties(
        model_properties_to_values, prefix, rotations, seperator):
    len_prefix = len(prefix+seperator)
    #kwargs = dict((prop[len_prefix:], value)
    #              for prop, value in model_properties_to_values.items())
    kwargs = {}
    for prop, value in model_properties_to_values.items():
        prime_prop = rotations[prop] \
                     if prop in rotations else prop[len_prefix:]
        kwargs[prime_prop] = value
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

def make_rotation(prime_property_name):
    translation = lambda p_to_v: _get_rotation_args(
        p_to_v, prime_property_name)
    return translation

def _get_rotation_args(model_properties_to_values, prime_property_name):
    #TODO: how to handle multiple model properties?
    prop, value = model_properties_to_values.items()[0]
    return {prime_property_name:value}
