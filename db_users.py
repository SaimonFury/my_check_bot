import os

from sqlalchemy import create_engine, Column, Integer, String 
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import basedir

engine = create_engine('sqlite:///' + os.path.join(basedir, 'students_data.db')) 

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Users(Base):
    __tablename__='Users'
    id = Column(Integer, primary_key=True)
    user = Column(String, unique=True, nullable=True)
    git_url = Column(String, unique=True, nullable=True)
    gmt = Column(Integer, nullable=True)

    def __str__(self):
        return(self.user)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)