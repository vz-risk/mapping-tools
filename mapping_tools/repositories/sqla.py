from sqlalchemy import create_engine
from sqlalchemy.sql import select, and_

#TODO: this code assumes a single mapping, while a real session will
#have to handle multiple mappings (such as rumors, and associations)

class SQLAlchemy(object):

    def __init__(self, mapping):
        #TODO: choose either relational or aggregate mapping
        engine_url = 'sqlite:///:memory:'
        self.engine = create_engine(engine_url)
        #self.sessionmaker = sessionmaker(bind=engine)
        self.mapping = mapping

    def make_session(self):
        return AggregateSessionAdaptor(self.engine, self.mapping)

class AggregateSessionAdaptor:

    def __init__(self, engine, mapping):
        self.engine = engine
        self.mapping = mapping

    def __enter__(self):
        self.connection = self.engine.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    def add_all(iterable):
        self.connection.execute(self.mapping.table.insert(),
                                [mapping.dump(obj) for obj in iterable])

    def query(self, model, criteria):
        where_clause = self._parse_where_clause(model, criteria)
        criteria_select = select([self.mapping.table]).where(where_clause)
        results = self.connection.execute(criteria_select)
        return results

    def _parse_where_clause(self, model, criteria):
        #TODO: assumes And conjuction
        conjuction = []
        for cri in criteria:
            path = '$'.join(cri['path'])
            if cri['operator'] == 'in':
                conjuction.append(self.mapping.table.c[path].in_(cri['value']))
            elif cri['operator'] == 'not in':
                conjuction.append(
                    self.mapping.table.c[path].notin_(cri['value']))
            elif cri['operator'] == '>=':
                conjuction.append(self.mapping.table.c[path] >= cri['value'])
            elif cri['operator'] == '<':
                conjuction.append(self.mapping.table.c[path] < cri['value'])
        return and_(*conjuction)

class RelationalSessionAdaptor:

    def __init__(self, engine, mapping):
        raise NotImplementedError()

def _get_attribute_from_path(model, path):
    attribute = model
    for node in path:
        attribute = getattr(attribute, node)
    return node

