from parse_cities import City
from register_places.places_api import find_place
import util


def check_cities() -> None:
    cities = util.read_json("cities.json")

    if isinstance(cities, list) is False:
        print("ERROR: Json format is incorrect")
        return

    cities = [City(**city) for city in cities]

    wrong_cities = [city for city in cities if city.prefecture not in city.formatted_address]

    fixed_places = [find_place(f"{city.prefecture, city.name}") for city in wrong_cities]
    print(len(fixed_places))

    if len(fixed_places) > 0:
        test = [place.candidates[0] for place in fixed_places]
        util.write_json(test, "fixed.json")


if __name__ == "__main__":
    check_cities()
