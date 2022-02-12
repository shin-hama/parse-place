from get_spots import SpotResult
from itertools import chain
from register_places.places_api import Candidate
from graphql_query import insert_types
import util


def read_spots() -> list[SpotResult]:
    spots = util.read_json("./spots.json")

    if isinstance(spots, list) is False:
        print("ERROR: Json format is incorrect")
        raise Exception

    spots = [SpotResult(spot=spot["spot"], place=[Candidate(**place) for place in spot["place"]]) for spot in spots]
    return spots


def extract_place_types(spot: SpotResult) -> list[str]:
    return list(chain.from_iterable([place.types for place in spot.place]))


def get_all_place_types() -> list[str]:
    spots = read_spots()

    types = list(chain.from_iterable([extract_place_types(spot) for spot in spots]))

    return list(set(types))


def add_types():
    types = get_all_place_types()
    insert_types(types)


if __name__ == "__main__":
    pass
