from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users_details'

    user_id = Column(Integer, primary_key=True)
    request_count = Column(Integer, default=1)

def create_tables(engine):
    Base.metadata.create_all(engine)