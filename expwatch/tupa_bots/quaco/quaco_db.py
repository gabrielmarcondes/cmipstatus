import sqlalchemy
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def create():
    return create_engine('sqlite:///quaco.db')


def connect():
    Session = sessionmaker(bind=create())
    return Session()


class Register(Base):
    __tablename__ = 'registers'

    name = Column(String, primary_key=True)
    error = Column(Integer)
    ack = Column(Integer)

    def __repr__(self):
        return "arq: {0}, err: {1}, ack: {2}".format(self.name, self.error, self.ack)


def start():
    engine = create()
    Base.metadata.create_all(engine)


def get(session, name):
    return session.query(Register).filter_by(name=name).first()


def set_recheck(session, name):
    register = session.query(Register).filter_by(name=name).first()
    register.ack = 2


def gen_report(session):
    registers = session.query(Register).filter(Register.error>0).filter(Register.ack==0)
    msgs = [[r.name, str(r.error)] for r in registers]
    for r in registers:
        r.ack = 1
    return msgs


def include(session, info):
    register = session.query(Register).filter_by(name=info['name']).first()
    if register:
        register.error = info['error']
        register.ack = 0
    else:
        session.add(Register(name=info['name'], error=info['error'], ack=0))
    
