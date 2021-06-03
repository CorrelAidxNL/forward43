"""Module to extract latitude longitude from string location data."""
from typing import Dict

from geopy.geocoders import Nominatim
from geopy.location import Location


class Geolocator():
    """Interface for getting latitude and longitude of a place from a string describing a place."""
    def __init__(self):
        self.geolocator = Nominatim(user_agent="Forward 43 application")

    def get_latlon_from_location_string(self, location_string: str) -> Dict[str, float]:
        """Returns latitude longitude from a location string."""
        response = self.geolocator.geocode(location_string)

        # geocode can return either a Location, or a list of Locations.
        if isinstance(response, list):
            location = response[0]
            return {"latitude": location.latitude, "longitude": response.longitude}

        if isinstance(response, Location):
            return {"latitude": response.latitude, "longitude": response.longitude}

        return {}
