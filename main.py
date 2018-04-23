from models import Coordinate, FuelType, AverageFuelPrice, FuelStation, FuelStationPrice, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
Session = sessionmaker()

import os
import math
import logging

def generate_coordinates(coordinate, maxSize):
    coordinates = []
    for x in range(math.ceil(coordinate.diff[0] / maxSize)):
        for y in range(math.ceil(coordinate.diff[1] / maxSize)):
            coordinates.append(
                Coordinate(
                    southWest_lat = coordinate.southWest_lat + (maxSize * x),
                    southWest_lon = coordinate.southWest_lon + (maxSize * y),
                    northEast_lat = coordinate.southWest_lat + (maxSize * (x + 1)),
                    northEast_lon = coordinate.southWest_lon + (maxSize * (y + 1))
                )
            )
    return coordinates


from anwb_connection import Connection


def run():
    engine = create_engine(
        'mysql+mysqldb://{}:{}@{}:{}/{}'.format(
            os.environ["MYSQL_USER"],
            os.environ["MYSQL_PASSWORD"],
            os.environ["MYSQL_HOST"],
            "3306",
            os.environ["MYSQL_DATABASE"]
        ),
        pool_recycle=3600
        )
    Base.metadata.create_all(engine)

    Session.configure(bind=engine)
    session = Session()
    connection = Connection()

    # calculating boxes and uploading them to the database for the first time
    if not session.query(Coordinate).all():
        for coordinate in generate_coordinates(
                Coordinate(
                    southWest_lat = 50.75038379999999,
                    southWest_lon = 3.3316001,
                    northEast_lat = 53.6316,
                    northEast_lon = 7.227510199999999                 
                ),
                0.257
            ):
            session.add(coordinate)

    # getting all available fuel types and saving them including the average pricing to the database
    for fueltype in connection.get_fuel_types():
        if not session.query(FuelType).filter(FuelType.code == fueltype["code"]):
            session.add(FuelType(code=fueltype["code"], name=fueltype["name"]))

        if not session.query(AverageFuelPrice).filter(AverageFuelPrice.fueltype == fueltype["code"], AverageFuelPrice.updated == fueltype["price_update_date"]):
            session.add(AverageFuelPrice(fueltype=fueltype["code"], price=fueltype["average_price"], updated=fueltype["price_update_date"])
    )

    session.commit()

    for coordinate in session.query(Coordinate).all():
        for station in connection.get_stations(coordinate.southWest, coordinate.northEast):
            if not session.query(FuelStation).filter(FuelStation.id == station["id"]):
                fuelstation = FuelStation(
                    id=station["id"],
                    name=station["name"],
                    brand_name=station["brand_name"],
                    display_name=station["display_name"],
                    location_lat=station["location"]["latitutde"],
                    location_lon=station["location"]["longitude"],
                    street=station["address"]["street"],
                    postal_code=station["address"]["postal_code"],
                    city=station["location"]["city"])
                session.add(fuelstation)
            for fuelspecification in station["fuel_specifications"]:
                pass
            



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run()