# coding: utf-8
from sqlalchemy import Column, Float, Index, Integer, LargeBinary, String, Table, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker, backref, relationship
import sys
import os

# Generate the correct path for the sqlite file
current_path = os.path.dirname(sys.modules[__name__].__file__)
sqlite_file_name = "database.db"
sqlite_full_path = os.path.join(current_path, sqlite_file_name)

Base = declarative_base()
metadata = Base.metadata

# Create the engine connected to the sqlite db
db_engine = create_engine('sqlite:///{}'.format(sqlite_full_path))

# Create the 'Session' class binded with the db engine
Session = sessionmaker(bind=db_engine)

# Create a session instance
session = Session()


class MapCategoryFuel(Base):
    __tablename__ = 'MAPCATEGORYFUEL'
    __table_args__ = (
        Index('MAPCATEGORYFUEL_INDEX', 'IDFUEL', 'IDCATEGORY'),
    )

    IDCATEGORY = Column(Integer, ForeignKey('CATEGORY.ID'), primary_key=True, nullable=False)
    IDFUEL = Column(Integer, ForeignKey('FUEL.ID'), primary_key=True, nullable=False)


class Category(Base):
    __tablename__ = 'CATEGORY'

    ID = Column(Integer, primary_key=True)
    ENT = Column(Integer)
    NAME = Column(String)

    fuels = relationship('Fuel',
                         secondary="MAPCATEGORYFUEL",
                         backref=backref('category'))


class Fuel(Base):
    __tablename__ = 'FUEL'

    ID = Column(Integer, primary_key=True)
    ENT = Column(Integer)
    NAME = Column(String)

    categories = relationship('Category',
                              secondary="MAPCATEGORYFUEL",
                              backref=backref("fuel"))



class EUROSTD(Base):
    __tablename__ = 'EUROSTD'

    ID = Column(Integer, primary_key=True)
    ENT = Column(Integer)
    NAME = Column(String)



class LOAD(Base):
    __tablename__ = 'LOAD'

    ID = Column(Integer, primary_key=True)
    ENT = Column(Integer)
    NAME = Column(String)




class MAPEUROSTDPOLLUTANT(Base):
    __tablename__ = 'MAPEUROSTDPOLLUTANT'
    __table_args__ = (
        Index('MAPEUROSTDPOLLUTANT_INDEX', 'IDEUROSTD', 'IDPOLLUTANT'),
    )

    IDPOLLUTANT = Column(Integer, primary_key=True, nullable=False)
    IDEUROSTD = Column(Integer, primary_key=True, nullable=False)


class MAPFUELSEGMENT(Base):
    __tablename__ = 'MAPFUELSEGMENT'
    __table_args__ = (
        Index('MAPFUELSEGMENT_INDEX', 'IDFUEL', 'IDSEGMENT'),
    )

    IDSEGMENT = Column(Integer, primary_key=True, nullable=False)
    IDFUEL = Column(Integer, primary_key=True, nullable=False)


class MAPLOADPARAMETER(Base):
    __tablename__ = 'MAPLOADPARAMETERS'
    __table_args__ = (
        Index('MAPLOADPARAMETERS_INDEX', 'IDLOAD', 'IDPARAMETERS'),
    )

    IDPARAMETERS = Column(Integer, primary_key=True, nullable=False)
    IDLOAD = Column(Integer, primary_key=True, nullable=False)


class MAPMODESLOPE(Base):
    __tablename__ = 'MAPMODESLOPE'
    __table_args__ = (
        Index('MAPMODESLOPE_INDEX', 'IDMODE', 'IDSLOPE'),
    )

    IDSLOPE = Column(Integer, primary_key=True, nullable=False)
    IDMODE = Column(Integer, primary_key=True, nullable=False)


class MAPPOLLUTANTMODE(Base):
    __tablename__ = 'MAPPOLLUTANTMODE'
    __table_args__ = (
        Index('MAPPOLLUTANTMODE_INDEX', 'IDMODE', 'IDPOLLUTANT'),
    )

    IDPOLLUTANT = Column(Integer, primary_key=True, nullable=False)
    IDMODE = Column(Integer, primary_key=True, nullable=False)


class MAPSEGMENTEUROSTD(Base):
    __tablename__ = 'MAPSEGMENTEUROSTD'
    __table_args__ = (
        Index('MAPSEGMENTEUROSTD_INDEX', 'IDEUROSTD', 'IDSEGMENT'),
    )

    IDSEGMENT = Column(Integer, primary_key=True, nullable=False)
    IDEUROSTD = Column(Integer, primary_key=True, nullable=False)


class MAPSLOPELOAD(Base):
    __tablename__ = 'MAPSLOPELOAD'
    __table_args__ = (
        Index('MAPSLOPELOAD_INDEX', 'IDLOAD', 'IDSLOPE'),
    )

    IDSLOPE = Column(Integer, primary_key=True, nullable=False)
    IDLOAD = Column(Integer, primary_key=True, nullable=False)


class MODE(Base):
    __tablename__ = 'MODE'

    ID = Column(Integer, primary_key=True)
    ENT = Column(Integer)
    NAME = Column(String)


class PARAMETER(Base):
    __tablename__ = 'PARAMETERS'

    ID = Column(Integer, primary_key=True)
    ENT = Column(Integer)
    ALPHA = Column(Float)
    BETA = Column(Float)
    DELTA = Column(Float)
    EPSILON = Column(Float)
    GAMMA = Column(Float)
    HTA = Column(Float)
    MAXSPEED = Column(Float)
    MINSPEED = Column(Float)
    REDUCTIONFACTOR = Column(Float)
    SPEED = Column(Float)
    ZITA = Column(Float)
    NAME = Column(String)


class POLLUTANT(Base):
    __tablename__ = 'POLLUTANT'

    ID = Column(Integer, primary_key=True)
    ENT = Column(Integer)
    NAME = Column(String)


class PRIMARYKEY(Base):
    __tablename__ = 'PRIMARYKEY'

    ENT = Column(Integer, primary_key=True)
    NAME = Column(String)
    SUPER = Column(Integer)
    MAX = Column(Integer)


class ROADSLOPE(Base):
    __tablename__ = 'ROADSLOPE'

    ID = Column(Integer, primary_key=True)
    ENT = Column(Integer)
    NAME = Column(String)


class SEGMENT(Base):
    __tablename__ = 'SEGMENT'

    ID = Column(Integer, primary_key=True)
    ENT = Column(Integer)
    NAME = Column(String)
