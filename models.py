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
    stations = relationship('FuelStation')

    __table_args__ = (UniqueConstraint('southWest_lat', 'southWest_lon', 'northEast_lat', 'northEast_lon', name='unique_coordinates'),)

    @property
    def diff(self):
        return tuple(map(sub, (self.northEast_lat, self.northEast_lon), (self.southWest_lat, self.southWest_lon)))
    
    @property
    def southWest(self):
        return (self.southWest_lat, self.southWest_lon)

    @property
    def northEast(self):
        return (self.northEast_lat, self.northEast_lon)

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

class FuelStation(Base):
    __tablename__ = "fuelstations"
    id = Column(String(10), primary_key=True)
    name = Column(String(50))
    brand_name = Column(String(100))
    display_name = Column(String(50))
    location_lat = Column(Float)
    location_lon = Column(Float)
    street = Column(String(100))
    postal_code = Column(String(10))
    city = Column(String(50))
    coordinate = Column(Integer, ForeignKey('coordinates.id'))
    fuelprices = relationship('FuelStationPrice')

    def __str__(self):
        return "<FuelStation(name={}, coordinate={})>".format(self.display_name, self.coordinate)

class FuelStationPrice(Base):
    __tablename__ = "fuelstationprice"
    id = Column(Integer, primary_key=True)
    fueltype = Column(String(50), ForeignKey('fueltypes.code'))
    station = Column(String(10), ForeignKey('fuelstations.id'))
    price = Column(Float)
    price_level = Column(String(20))
    record = Column(String(40))
    source = Column(String(20))

    __table_args__ = (UniqueConstraint('fueltype', 'station', 'record', name='unique_prices'),)

    def __str__(self):
        return "<FuelStationPrice(fueltype={}, station={}, price={}, price_level={})>".format(self.fueltype, self.station, self.price, self.price_level)