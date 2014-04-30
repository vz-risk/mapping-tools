import inspect

def properties(Type):
    args = set(inspect.getargspec(Type.__init__).args)
    properties = tuple(args - set(('self',)))
    return properties
