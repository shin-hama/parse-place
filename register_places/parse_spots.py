from dataclasses import asdict
from itertools import chain

from get_spots import SpotResult
from register_places.get_spots import Spot
from register_places.graphql_query import SpotSchema, insert_spots
from register_places.places_api import Candidate
from graphql_query import insert_types
import util
from constants.prefectures_code import pref_code


def read_spots() -> list[SpotResult]:
    spots = util.read_json("./not_processed_spots.json")

    if isinstance(spots, list) is False:
        print("ERROR: Json format is incorrect")
        raise Exception

    spots = [
        SpotResult(spot=Spot(**spot["spot"]), place=[Candidate(**place) for place in spot["place"]]) for spot in spots
    ]
    return spots


def parse_processed():
    from processed import processed_spots

    spots = read_spots()

    processed_ids = [s["place_id"] for s in processed_spots]

    not_processed = [asdict(spot) for spot in spots if spot.place[0].place_id not in processed_ids]

    util.write_json(not_processed, "not_processed_spots.json")


def add_spots() -> None:
    spots = read_spots()

    spot_schemas = [
        SpotSchema(
            name=spot.place[0].name,
            lat=spot.place[0].geometry.location.lat,
            lng=spot.place[0].geometry.location.lng,
            place_id=spot.place[0].place_id,
            prefecture_code=pref_code[spot.spot.prefecture],
            spots_types={
                "data": [
                    {
                        "type": {
                            "data": {"name": type_name},
                            "on_conflict": {"constraint": "spot_types_name_key", "update_columns": "name"},
                        },
                    }
                    for type_name in set(spot.place[0].types)
                ]
            },
        )
        for spot in spots
    ]

    # insert_spots(spot_schemas)
    for i, schema in enumerate(spot_schemas):
        try:
            insert_spots([schema])
        except Exception as e:
            print(i, schema.name)


def extract_place_types(spot: SpotResult) -> list[str]:
    return list(chain.from_iterable([place.types for place in spot.place]))


def get_all_place_types() -> list[str]:
    spots = read_spots()

    types = list(chain.from_iterable([extract_place_types(spot) for spot in spots]))

    return list(set(types))


def add_types() -> None:
    types = get_all_place_types()
    insert_types(types)


def get_spots():
    pass


if __name__ == "__main__":
    add_spots()
    # parse_processed()
    pass
