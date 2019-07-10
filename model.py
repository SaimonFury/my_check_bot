from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///' + 'test.db')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    username = Column(String(40), index=True, unique=True)
    role = Column(String(10), index=True)

    def __repr__(self):
        return f'<Student: {self.username}>'


if __name__=="__main__":
    Base.metadata.create_all(bind=engine)