import csv
import json
from typing import Any

from places_api import find_place


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


def find_cities(cities: list[str], prefecture: str):
    for city in cities:
        place = find_place(city)

        print(prefecture)
        print(place.get("formatted_address", ""))

        if prefecture in place.get("formatted_address", ""):
            print(place)
        else:
            print(False)


if __name__ == "__main__":
    outputs = read()
    obj = [{"prefecture": output[0], "cities": output[1].split("、")} for output in outputs]
    find_cities(obj[0]["cities"], obj[0]["prefecture"])
    write(obj)
