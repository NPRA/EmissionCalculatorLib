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
    name = Column('NAME', String)

    fuels = relationship('Fuel',
                         secondary='MAPCATEGORYFUEL',
                         backref=backref('categories'))

    def __repr__(self):
        return '{}(name="{}")'.format(self.__class__.__name__, self.name)


class MapFuelSegment(Base):
    __tablename__ = 'MAPFUELSEGMENT'
    __table_args__ = (
        Index('MAPFUELSEGMENT_INDEX', 'IDFUEL', 'IDSEGMENT'),
    )

    IDSEGMENT = Column(Integer, ForeignKey('SEGMENT.ID'), primary_key=True, nullable=False)
    IDFUEL = Column(Integer, ForeignKey('FUEL.ID'), primary_key=True, nullable=False)


class Fuel(Base):
    __tablename__ = 'FUEL'

    ID = Column(Integer, primary_key=True)
    ENT = Column(Integer)
    name = Column('NAME', String)

    # categories = relationship('Category',
    #                           secondary='MAPCATEGORYFUEL',
    #                           backref=backref('fuel'))

    segments = relationship('Segment',
                            secondary='MAPFUELSEGMENT',
                            backref=backref('fuels'))

    def __repr__(self):
        return '{}(name="{}")'.format(self.__class__.__name__, self.name)


class MapSegmentEuroStd(Base):
    __tablename__ = 'MAPSEGMENTEUROSTD'
    __table_args__ = (
        Index('MAPSEGMENTEUROSTD_INDEX', 'IDEUROSTD', 'IDSEGMENT'),
    )

    IDSEGMENT = Column(Integer, ForeignKey('SEGMENT.ID'), primary_key=True, nullable=False)
    IDEUROSTD = Column(Integer, ForeignKey('EUROSTD.ID'), primary_key=True, nullable=False)


class Segment(Base):
    __tablename__ = 'SEGMENT'

    ID = Column(Integer, primary_key=True)
    ENT = Column(Integer)
    name = Column('NAME', String)

    # fuels = relationship('Fuel',
    #                      secondary='MAPFUELSEGMENT',
    #                      backref=backref('fuels'))

    eurostds = relationship('EuroStd',
                            secondary='MAPSEGMENTEUROSTD',
                            backref=backref('segments'))

    def __repr__(self):
        return '{}(name="{}")'.format(self.__class__.__name__, self.name.encode('utf-8'))


class EuroStd(Base):
    __tablename__ = 'EUROSTD'

    ID = Column(Integer, primary_key=True)
    ENT = Column(Integer)
    name = Column('NAME', String)

    # segments = relationship('Segment',
    #                         secondary='MAPSEGMENTEUROSTD',
    #                         backref=backref('segments'))

    pollutants = relationship('Pollutant',
                              secondary='MAPEUROSTDPOLLUTANT',
                              backref=backref('eurostds'))

    def __repr__(self):
        return '{}(name="{}")'.format(self.__class__.__name__, self.name)


class MapEuroStdPollutant(Base):
    __tablename__ = 'MAPEUROSTDPOLLUTANT'
    __table_args__ = (
        Index('MAPEUROSTDPOLLUTANT_INDEX', 'IDEUROSTD', 'IDPOLLUTANT'),
    )

    IDPOLLUTANT = Column(Integer, ForeignKey('POLLUTANT.ID'), primary_key=True, nullable=False)
    IDEUROSTD = Column(Integer, ForeignKey('EUROSTD.ID'), primary_key=True, nullable=False)


class Pollutant(Base):
    __tablename__ = 'POLLUTANT'

    ID = Column(Integer, primary_key=True)
    ENT = Column(Integer)
    name = Column('NAME', String)

    # eurostds = relationship('EuroStd',
    #                         secondary='MAPEUROSTDPOLLUTANT',
    #                         backref=backref('eurostds'))
    modes = relationship('Mode',
                         secondary='MAPPOLLUTANTMODE',
                         backref=backref('pollutants'))

    def __repr__(self):
        return '{}(name="{}")'.format(self.__class__.__name__, self.name)


class Mode(Base):
    __tablename__ = 'MODE'

    ID = Column(Integer, primary_key=True)
    ENT = Column(Integer)
    name = Column('NAME', String)

    # pollutants = relationship('Pollutant',
    #                           secondary='MAPPOLLUTANTMODE',
    #                           backref=backref('pollutant'))

    slopes = relationship('RoadSlope',
                          secondary='MAPMODESLOPE',
                          backref=backref('modes'))

    def __repr__(self):
        return '{}(name="{}")'.format(self.__class__.__name__, self.name)


class MapPollutantMode(Base):
    __tablename__ = 'MAPPOLLUTANTMODE'
    __table_args__ = (
        Index('MAPPOLLUTANTMODE_INDEX', 'IDMODE', 'IDPOLLUTANT'),
    )

    IDPOLLUTANT = Column(Integer, ForeignKey('POLLUTANT.ID'), primary_key=True, nullable=False)
    IDMODE = Column(Integer, ForeignKey('MODE.ID'), primary_key=True, nullable=False)


class RoadSlope(Base):
    __tablename__ = 'ROADSLOPE'

    ID = Column(Integer, primary_key=True)
    ENT = Column(Integer)
    name = Column('NAME', String)

    # modes = relationship('Mode',
    #                      secondary='MAPMODESLOPE',
    #                      backref=backref('mode'))
    loads = relationship('Load',
                         secondary='MAPSLOPELOAD',
                         backref=backref('slopes'))

    def __repr__(self):
        return '{}(name="{}")'.format(self.__class__.__name__, self.name)


class MapModeSlope(Base):
    __tablename__ = 'MAPMODESLOPE'
    __table_args__ = (
        Index('MAPMODESLOPE_INDEX', 'IDMODE', 'IDSLOPE'),
    )

    IDSLOPE = Column(Integer, ForeignKey('ROADSLOPE.ID'), primary_key=True, nullable=False)
    IDMODE = Column(Integer, ForeignKey('MODE.ID'), primary_key=True, nullable=False)


class Load(Base):
    __tablename__ = 'LOAD'

    ID = Column(Integer, primary_key=True)
    ENT = Column(Integer)
    name = Column('NAME', String)

    parameters = relationship('Parameter',
                          secondary='MAPLOADPARAMETERS',
                          backref=backref('loads'))

    def __repr__(self):
        return '{}(name="{}")'.format(self.__class__.__name__, self.name)


class MapSlopeLoad(Base):
    __tablename__ = 'MAPSLOPELOAD'
    __table_args__ = (
        Index('MAPSLOPELOAD_INDEX', 'IDLOAD', 'IDSLOPE'),
    )

    IDSLOPE = Column(Integer, ForeignKey('ROADSLOPE.ID'), primary_key=True, nullable=False)
    IDLOAD = Column(Integer, ForeignKey('LOAD.ID'), primary_key=True, nullable=False)



class MapLoadParameter(Base):
    __tablename__ = 'MAPLOADPARAMETERS'
    __table_args__ = (
        Index('MAPLOADPARAMETERS_INDEX', 'IDLOAD', 'IDPARAMETERS'),
    )

    IDPARAMETERS = Column(Integer, ForeignKey('PARAMETERS.ID'), primary_key=True, nullable=False)
    IDLOAD = Column(Integer, ForeignKey('LOAD.ID'), primary_key=True, nullable=False)


class Parameter(Base):
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
    name = Column('Name', String)

    def __repr__(self):
        return '{}(name="{}")'.format(self.__class__.__name__, self.name)


class PRIMARYKEY(Base):
    """This table / model is not needed.
    """
    __tablename__ = 'PRIMARYKEY'

    ENT = Column(Integer, primary_key=True)
    NAME = Column(String)
    SUPER = Column(Integer)
    MAX = Column(Integer)



