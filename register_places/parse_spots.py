import dataclasses
from itertools import chain

from places_api import find_place
from register_places.places_api import GoogleApiResponse
import csv_io


@dataclasses.dataclass
class Spot:
    prefecture: str
    spot: str
    abstract: str


if __name__ == "__main__":
    outputs = csv_io.read("spots.csv")
    print(outputs[0])
    spots = [Spot(*output) for output in outputs]
    print(spots[0])

    # cities = chain.from_iterable([find_cities(place.cities) for place in places])

    # csv_io.write([dataclasses.asdict(city) for city in cities], "cities.json")
