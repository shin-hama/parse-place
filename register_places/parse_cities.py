import csv
import dataclasses
from itertools import chain
import json
from typing import Any

from places_api import find_place
from register_places.places_api import GoogleApiResponse


@dataclasses.dataclass
class Cities:
    prefecture: str
    cities: list[str]


def read() -> list[list[str]]:
    outputs = []
    with open("./majorCities.csv", mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)

        for row in reader:
            outputs.append(row)

    # remove header
    return outputs[1:]


def write(obj: Any):
    with open("cities.json", mode="w", encoding="utf-8") as f:
        json.dump(
            obj,
            f,
            indent=2,
            ensure_ascii=False,
        )


def build_place(place: list[str]):
    prefecture = place[0]
    cities = place[1].split("、")

    return Cities(prefecture, cities)


def find_cities(cities: list[str]) -> list[GoogleApiResponse]:
    return [find_place(city) for city in cities]


if __name__ == "__main__":
    outputs = read()
    places = [build_place(output) for output in outputs]

    cities = chain.from_iterable([find_cities(place.cities) for place in places])

    write([dataclasses.asdict(city) for city in cities])
