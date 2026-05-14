import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SqlAlchemyBase = declarative_base()

def global_init(db_path):
    global engine
    engine = sqlalchemy.create_engine(db_path, echo=True)
    SqlAlchemyBase.metadata.create_all(engine)

def create_session():
    Session = sessionmaker(bind=engine)
    return Session()