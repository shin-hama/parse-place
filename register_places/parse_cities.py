import dataclasses
from itertools import chain

from places_api import find_place
from register_places.places_api import Candidate
import csv_io


@dataclasses.dataclass
class Cities:
    prefecture: str
    cities: list[str]


@dataclasses.dataclass
class City(Candidate):
    prefecture: str


def build_place(place: list[str]):
    prefecture = place[0]
    cities = place[1].split("、")

    return Cities(prefecture, cities)


def find_cities(cities: Cities) -> list[City]:
    return [City(prefecture=cities.prefecture, **find_place(city).candidates[0]) for city in cities.cities]


if __name__ == "__main__":
    outputs = csv_io.read("majorCities.csv")
    places = [build_place(output) for output in outputs]

    cities = chain.from_iterable([find_cities(place) for place in places])

    csv_io.write([dataclasses.asdict(city) for city in cities], "cities.json")
