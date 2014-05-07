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
    kwargs = {}
    len_prefix = len(prefix+seperator)
    for prop, value in model_properties_to_values.items():
         kwargs[prop[len_prefix:]] = value
    return kwargs
