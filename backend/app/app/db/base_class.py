from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import declared_attr


class CustomBase(object):
    # Typically, we declare tablename on a per
    # model basis, as shown in the SQLAlchemy docs:
    #
    # class Company(Base):
    #   __tablename__ = 'company'
    #   id = Column(Integer, primary_key=True)
    #
    # To have a simpler, less verbose interface - this
    # custom base class will allow us to
    # generate __tablename__ automatically 
    
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(cls=CustomBase)