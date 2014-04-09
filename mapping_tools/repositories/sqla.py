from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class SQLAlchemy:

    def __init__(self):
        engine_url = 'sqlite:///:memory:'
        engine = create_engine(engine_url)
        self.sessionmaker = sessionmaker(bind=engine)

    def make_session(self):
        return SessionAdaptor(self.sessionmaker())

class SessionAdaptor:

    def __init__(self, session):
        self.session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

    def query(self, model, criteria):
        q = self.session.query(model)
        raise NotImplementedError()
