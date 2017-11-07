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


# class CategoryFuelMap(Base):
#     __tablename__ = 'category_fuel_map'
#     id = Column(Integer, primary_key=True, nullable=False)
#     category_id = Column(Integer, ForeignKey('category.id'))
#     fuel_id = Column(Integer, ForeignKey('fuel.id'))


# class Category(Base):
#     __tablename__ = 'category'
#     id = Column(Integer, primary_key=True, nullable=False)
#     name = Column(String, nullable=False)


# class Fuel(Base):
#     __tablename__ = 'fuel'
#     id = Column(Integer, primary_key=True, nullable=False)
#     name = Column(String, nullable=False)


# # Many-To-Many table
# class Z1TYPEFUEL(Base):
#     __tablename__ = 'Z_1TYPEFUEL'
#     __table_args__ = (
#         Index('Z_1TYPEFUEL_Z_3TYPEFUEL_INDEX', 'Z_3TYPEFUEL', 'Z_1TYPECATEGORY'),
#     )

#     # Z_1TYPECATEGORY = Column(Integer, primary_key=True, nullable=False)
#     category_id = Column('Z_1TYPECATEGORY', Integer, ForeignKey('ZCATEGORY.Z_PK'), primary_key=True)
#     # Z_3TYPEFUEL = Column(Integer, primary_key=True, nullable=False)
#     fuel_type_id = Column('Z_3TYPEFUEL', Integer, ForeignKey('ZFUEL.Z_PK'), primary_key=True)


# class Category(Base):
#     __tablename__ = 'ZCATEGORY'

#     Z_PK = Column(Integer, primary_key=True)
#     Z_ENT = Column(Integer)
#     Z_OPT = Column(Integer)
#     name = Column('ZID', String)

#     def fuels(self):
#         return session.query(Fuel).filter(
#             and_(
#                 self.Z_PK == Z1TYPEFUEL.category_id,
#                 Z1TYPEFUEL.fuel_type_id == Fuel.Z_PK)).all()


# class Fuel(Base):
#     __tablename__ = 'ZFUEL'

#     Z_PK = Column(Integer, primary_key=True)
#     Z_ENT = Column(Integer)
#     Z_OPT = Column(Integer)
#     name = Column('ZID', String)

#     def eurostds(self):
#         pass


# class Z2EUROSTDSEGMENT(Base):
#     __tablename__ = 'Z_2EUROSTDSEGMENT'
#     __table_args__ = (
#         Index('Z_2EUROSTDSEGMENT_Z_9EUROSTDSEGMENT_INDEX', 'Z_9EUROSTDSEGMENT', 'Z_2TYPEEUROSTD'),
#     )

#     Z_2TYPEEUROSTD = Column(Integer, primary_key=True, nullable=False)
#     Z_9EUROSTDSEGMENT = Column(Integer, primary_key=True, nullable=False)


# class EuroStandard(Base):
#     __tablename__ = 'ZEUROSTD'

#     Z_PK = Column(Integer, primary_key=True)
#     Z_ENT = Column(Integer)
#     Z_OPT = Column(Integer)
#     name = Column('ZID', String)


# class Load(Base):
#     __tablename__ = 'ZLOAD'

#     Z_PK = Column(Integer, primary_key=True)
#     Z_ENT = Column(Integer)
#     Z_OPT = Column(Integer)
#     name = Column('ZID', String)


# class Mode(Base):
#     __tablename__ = 'ZMODE'

#     Z_PK = Column(Integer, primary_key=True)
#     Z_ENT = Column(Integer)
#     Z_OPT = Column(Integer)
#     name = Column('ZID', String)


# class Parameter(Base):
#     __tablename__ = 'ZPARAMETERS'

#     Z_PK = Column(Integer, primary_key=True)
#     Z_ENT = Column(Integer)
#     Z_OPT = Column(Integer)
#     ZALPHA = Column(Float)
#     ZBETA = Column(Float)
#     ZDELTA = Column(Float)
#     ZEPSILON = Column(Float)
#     ZGAMMA = Column(Float)
#     ZHTA = Column(Float)
#     ZMAXSPEED = Column(Float)
#     ZMINSPEED = Column(Float)
#     ZREDUCTIONFACTOR = Column(Float)
#     ZSPEED = Column(Float)
#     ZZITA = Column(Float)
#     parameter_id = Column('ZID', String)


# class Pollutant(Base):
#     __tablename__ = 'ZPOLLUTANT'

#     Z_PK = Column(Integer, primary_key=True)
#     Z_ENT = Column(Integer)
#     Z_OPT = Column(Integer)
#     name = Column('ZID', String)


# class RoadSlope(Base):
#     __tablename__ = 'ZROADSLOPE'

#     Z_PK = Column(Integer, primary_key=True)
#     Z_ENT = Column(Integer)
#     Z_OPT = Column(Integer)
#     name = Column('ZID', String)


# class Segment(Base):
#     __tablename__ = 'ZSEGMENT'

#     Z_PK = Column(Integer, primary_key=True)
#     Z_ENT = Column(Integer)
#     Z_OPT = Column(Integer)
#     name = Column('ZID', String)


# ## Many-To-Many relations described below here


# class Z2TYPEPOLLUTANT(Base):
#     __tablename__ = 'Z_2TYPEPOLLUTANT'
#     __table_args__ = (
#         Index('Z_2TYPEPOLLUTANT_Z_7TYPEPOLLUTANT_INDEX', 'Z_7TYPEPOLLUTANT', 'Z_2POLLUTANTEUROSTD'),
#     )

#     Z_2POLLUTANTEUROSTD = Column(Integer, primary_key=True, nullable=False)
#     Z_7TYPEPOLLUTANT = Column(Integer, primary_key=True, nullable=False)


# class Z3TYPESEGMENT(Base):
#     __tablename__ = 'Z_3TYPESEGMENT'
#     __table_args__ = (
#         Index('Z_3TYPESEGMENT_Z_9TYPESEGMENT_INDEX', 'Z_9TYPESEGMENT', 'Z_3SEGMENTFUEL'),
#     )

#     Z_3SEGMENTFUEL = Column(Integer, primary_key=True, nullable=False)
#     Z_9TYPESEGMENT = Column(Integer, primary_key=True, nullable=False)


# class Z4LOADSLOPE(Base):
#     __tablename__ = 'Z_4LOADSLOPE'
#     __table_args__ = (
#         Index('Z_4LOADSLOPE_Z_8LOADSLOPE_INDEX', 'Z_8LOADSLOPE', 'Z_4TYPELOAD1'),
#     )

#     Z_4TYPELOAD1 = Column(Integer, primary_key=True, nullable=False)
#     Z_8LOADSLOPE = Column(Integer, primary_key=True, nullable=False)


# class Z4PARAMETER(Base):
#     __tablename__ = 'Z_4PARAMETERS'
#     __table_args__ = (
#         Index('Z_4PARAMETERS_Z_6PARAMETERS_INDEX', 'Z_6PARAMETERS', 'Z_4TYPELOAD'),
#     )

#     Z_4TYPELOAD = Column(Integer, primary_key=True, nullable=False)
#     Z_6PARAMETERS = Column(Integer, primary_key=True, nullable=False)


# class Z5MODEPOLLUTANT(Base):
#     __tablename__ = 'Z_5MODEPOLLUTANT'
#     __table_args__ = (
#         Index('Z_5MODEPOLLUTANT_Z_7MODEPOLLUTANT_INDEX', 'Z_7MODEPOLLUTANT', 'Z_5TYPEMODE'),
#     )

#     Z_5TYPEMODE = Column(Integer, primary_key=True, nullable=False)
#     Z_7MODEPOLLUTANT = Column(Integer, primary_key=True, nullable=False)


# class Z5TYPESLOPE(Base):
#     __tablename__ = 'Z_5TYPESLOPE'
#     __table_args__ = (
#         Index('Z_5TYPESLOPE_Z_8TYPESLOPE_INDEX', 'Z_8TYPESLOPE', 'Z_5SLOPEMODE'),
#     )

#     Z_5SLOPEMODE = Column(Integer, primary_key=True, nullable=False)
#     Z_8TYPESLOPE = Column(Integer, primary_key=True, nullable=False)


# # class ZMETADATUM(Base):
# #    __tablename__ = 'Z_METADATA'
# #
# #    Z_VERSION = Column(Integer, primary_key=True)
# #    Z_UUID = Column(Text(255))
# #    Z_PLIST = Column(LargeBinary)
# #
# #
# # t_Z_MODELCACHE = Table(
# #    'Z_MODELCACHE', metadata,
# #    Column('Z_CONTENT', LargeBinary)
# # )


# class ZPRIMARYKEY(Base):
#     __tablename__ = 'Z_PRIMARYKEY'

#     Z_ENT = Column(Integer, primary_key=True)
#     Z_NAME = Column(String)
#     Z_SUPER = Column(Integer)
#     Z_MAX = Column(Integer)
