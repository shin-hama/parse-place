import dataclasses

import register_places.util as util
from places_api import find_place
from register_places.places_api import Candidate


@dataclasses.dataclass
class Spot:
    prefecture: str
    name: str
    abstract: str


@dataclasses.dataclass
class SpotResult:
    spot: Spot
    place: list[Candidate]


def get_place_info(spot: Spot) -> SpotResult:
    place = find_place(f"{spot.prefecture} {spot.name}")
    return SpotResult(spot=spot, place=place.candidates[0])


if __name__ == "__main__":
    outputs = util.read_csv("spots.csv")

    # Get one spot for debug
    # spot = get_place_info(Spot(*outputs[0]))
    # util.write_json(dataclasses.asdict(spot), "spots.json")

    spots = [get_place_info(Spot(*output)) for output in outputs]

    spots_dict = [dataclasses.asdict(spot) for spot in spots]
    util.write_json(spots_dict, "spots.json")
