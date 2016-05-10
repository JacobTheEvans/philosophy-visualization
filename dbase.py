#!/usr/bin/python
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData ,text, BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import ARRAY

engine = create_engine("postgresql://jacob:jacob@localhost/jacob")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Work(Base):
    __tablename__  = "Works"
    author = Column(String(1000), nullable=False)
    branch = Column(String(1000), nullable=False)
    name = Column(String(1000), primary_key=True)
    citations = Column(ARRAY(String(1000)), nullable=False)

Base.metadata.create_all(engine)

#Work query functions
def add_work(name, author, branch, citations):
    new_work = Work(name=name, author=author, branch=branch, citations=citations)
    session.add(new_work)
    session.commit()
    try:
        pass
    except:
        session.rollback()
        print "Error"

def get_works():
    result = []
    data = session.query(Work).all()
    return data
