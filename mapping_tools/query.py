class And:
    
    _criteria = []

    def add(self, *path, **kwargs):
        '''
        kwargs: value
        '''
        self._criteria.append({'value':kwargs['value'], path:path})
