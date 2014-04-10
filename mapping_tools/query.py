class And:
    
    _criteria = []

    def add(self, path, value, operator='in'):
        if isinstanve(path, basestring):
            path = (path,)
        self._criteria.append(
            {'value':value, 'path':path, 'operator':operator})

    def __iter__(self):
        return iter(self._criteria)
