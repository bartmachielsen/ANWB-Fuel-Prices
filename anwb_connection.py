import requests

class Connection:
    """Connection class connects to the rest server of ANWB
    NOTE: Anwb uses different versions of api (1-3) Fuel is only version 1
    """

    base_url = "https://api.anwb.nl/v1/"
    api_key = "GNYXLHxCa14zfA1nVJkVV8ldQZHbPTcu"

    class Redirects:
        FUEL_TYPES = "/fuel/types"
        STATIONS = "/fuel/stations"

    def __init__(self):
        pass
    
    def get_fuel_types(self):
        response = requests.get(self.base_url + self.Redirects.FUEL_TYPES, headers={"apiKey": self.api_key})
        if response.status_code == 200:
            return response.json()["items"]
    
    def get_stations(self, southWest, northEast):
        response = requests.get(
            "{}{}?sw={},{}&ne={},{}".format(
                self.base_url,
                self.Redirects.STATIONS,
                southWest[0], southWest[1],
                northEast[0], northEast[1]
                ), headers={"apiKey": self.api_key})
        if response.status_code == 200:
            return response.json()["items"]
        return []
        
