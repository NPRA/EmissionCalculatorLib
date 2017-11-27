# coding: utf-8
from __future__ import unicode_literals
import sys
import os

from sqlalchemy import Column, Float, Index, Integer, LargeBinary, String, Table, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker, backref, relationship, scoped_session

# Generate the correct path for the sqlite file
current_path = os.path.dirname(sys.modules[__name__].__file__)
sqlite_file_name = "database.db"
sqlite_full_path = os.path.join(current_path, sqlite_file_name)

Base = declarative_base()
metadata = Base.metadata

# Create the engine connected to the sqlite db
db_engine = create_engine('sqlite:///{}'.format(sqlite_full_path))

# Create the 'Session' class binded with the db engine
Session = scoped_session(sessionmaker(bind=db_engine))

# Create a session instance
session = Session()


def filter_parms(**items):
    """
    To get all segment for 'petrol truck'. Valid parameters:
        cat=category
        fuel=fuel
        segment=segment
        eurostd=eurostd
        pollutant=pollutant
        mode=mode

    >>> truck = session.query(emission.models.Category).all()[2]
    >>> fuel = list(truck.fuels())[0]
    >>> filtered_parameters = emission.models.filter(cat=truck, fuel=fuel)
    >>> set(x.segment for x in filtered_parameters)
    """
    parameters = []
    if "cat" in items:
        parameters = items.get("cat").parameter

    if "fuel" in items:
        parameters = list(filter(lambda x: x.fuel == items.get("fuel"), parameters))

    if "segment" in items:
        parameters = list(filter(lambda x: x.segment == items.get("segment"), parameters))

    if "eurostd" in items:
        parameters = list(filter(lambda x: x.eurostd == items.get("eurostd"), parameters))

    if "pollutant" in items:
        parameters = list(filter(lambda x: x.pollutant == items.get("pollutant"), parameters))

    if "mode" in items:
        parameters = list(filter(lambda x: x.mode == items.get("mode"), parameters))

    return parameters


class Category(Base):
    __tablename__ = 'CATEGORY'

    ID = Column(Integer, primary_key=True)
    ENT = Column(Integer)
    name = Column('NAME', String, unique=True)
    parameter = relationship('Parameter', backref=backref('category'))

    def fuels(self):
        """Find all valid fuel types for this Category vehicle"""
        parm = self.parameter
        vehicle_fuels = set(x.fuel for x in parm)
        return vehicle_fuels

    @classmethod
    def get_for_type(class_, vehicle):
        """Return query to find Category for a particular Vechicle type"""
        Category = class_
        found = session.query(Category).filter_by(name=vehicle.get_category_id()).first()
        return found

    def __repr__(self):
        return '{}(name="{}")'.format(self.__class__.__name__, self.name)


class Fuel(Base):
    __tablename__ = 'FUEL'

    ID = Column(Integer, primary_key=True)
    ENT = Column(Integer)
    name = Column('NAME', String, unique=True)
    parameter = relationship('Parameter', backref=backref('fuel'))

    def segments(self):
        param = self.parameter
        vehicle_segments = set(x.segment for x in param)
        return vehicle_segments

    @classmethod
    def get_for_type(class_, vehicle):
        """Return query to find Fuel for a particluar Vehicle type"""
        Fuel = class_
        found = session.query(Fuel).filter_by(name=vehicle.fuel_type).first()
        return found

    def __repr__(self):
        return '{}(name="{}")'.format(self.__class__.__name__, self.name)


class Segment(Base):
    __tablename__ = 'SEGMENT'

    ID = Column(Integer, primary_key=True)
    ENT = Column(Integer)
    name = Column('NAME', String, unique=True)
    parameter = relationship('Parameter', backref=backref('segment'))

    def __repr__(self):
        return '{}(name="{}")'.format(self.__class__.__name__, self.name)


class EuroStd(Base):
    __tablename__ = 'EUROSTD'

    ID = Column(Integer, primary_key=True)
    ENT = Column(Integer)
    name = Column('NAME', String, unique=True)
    parameter = relationship('Parameter', backref=backref('eurostd'))

    def __repr__(self):
        return '{}(name="{}")'.format(self.__class__.__name__, self.name)


class Pollutant(Base):
    __tablename__ = 'POLLUTANT'

    ID = Column(Integer, primary_key=True)
    ENT = Column(Integer)
    name = Column('NAME', String, unique=True)
    parameter = relationship('Parameter', backref=backref('pollutant'))

    def __repr__(self):
        return '{}(name="{}")'.format(self.__class__.__name__, self.name)


class Mode(Base):
    __tablename__ = 'MODE'

    ID = Column(Integer, primary_key=True)
    ENT = Column(Integer)
    name = Column('NAME', String, unique=True)
    parameter = relationship('Parameter', backref=backref('mode'))

    def __repr__(self):
        return '{}(name="{}")'.format(self.__class__.__name__, self.name)


class Parameter(Base):
    __tablename__ = 'Parameters'

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

    slope = Column(Float, nullable=True)
    load = Column(Float, nullable=True)

    category_id = Column(Integer, ForeignKey('CATEGORY.ID'))
    fuel_id = Column(Integer, ForeignKey('FUEL.ID'))
    segment_id = Column(Integer, ForeignKey('SEGMENT.ID'))
    euro_std_id = Column(Integer, ForeignKey('EUROSTD.ID'))
    mode_id = Column(Integer, ForeignKey('MODE.ID'))
    pollutant_id = Column(Integer, ForeignKey('POLLUTANT.ID'))

    @classmethod
    def by_vehicle(class_, vehicle):
        Parameter = class_
        cat = session.query(Category).filter_by(name=vehicle.get_category_id()).first()
        fuel = session.query(Fuel).filter_by(name=vehicle.fuel_type).first()
        query = session.query(Parameter).filter_by(category=cat)
        return query

    def __repr__(self):
        return '{}(id={}, pollutant={}, category={}, fuel={}, segment={}, euro_std={}, mode={}, load={}, slope={})'.format(
            self.__class__.__name__,
            self.ID,
            self.pollutant.name,
            self.category.name,
            self.fuel.name,
            self.segment.name,
            self.eurostd.name,
            self.mode.name,
            self.load,
            self.slope)
