from sqlalchemy import Column, Integer, String, Float, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from operator import sub

class Coordinate(Base):
    __tablename__ = 'coordinates'
    id = Column(Integer, primary_key=True)
    southWest_lat = Column(Float)
    southWest_lon = Column(Float)
    northEast_lat = Column(Float)
    northEast_lon = Column(Float)

    __table_args__ = (UniqueConstraint('southWest_lat', 'southWest_lon', 'northEast_lat', 'northEast_lon', name='unique_coordinates'),)

    @property
    def diff(self):
        return tuple(map(sub, (self.northEast_lat, self.northEast_lon), (self.southWest_lat, self.southWest_lon)))
    

class FuelType(Base):
    __tablename__ = 'fueltypes'
    code = Column(String(20), primary_key=True)
    name = Column(String(50))
    average_fuel_prices = relationship('AverageFuelPrice')

class AverageFuelPrice(Base):
    __tablename__ = "avgfuelprice"
    id = Column(Integer, primary_key=True)
    fueltype = Column(String(20), ForeignKey('fueltypes.code'))
    price = Column(Float)
    updated = Column(String(50))

    __table_args__ = (UniqueConstraint('fueltype', 'updated', name='duplicate_measurement'),)