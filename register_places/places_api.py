import dataclasses
import os
from typing import Any

import googlemaps
from dotenv import load_dotenv

load_dotenv(verbose=True)

gmaps = googlemaps.Client(key=os.environ.get("GOOGLE_MAP_API_KEY"))


@dataclasses.dataclass
class Location:
    lat: float
    lng: float


@dataclasses.dataclass
class Geometry:
    location: Location


@dataclasses.dataclass
class Candidate:
    formatted_address: str
    name: str
    place_id: str
    geometry: Geometry


@dataclasses.dataclass
class GoogleApiResponse:
    candidates: list[Candidate]
    status: str


def find_place(name: str) -> GoogleApiResponse:
    result: dict[str, Any] = gmaps.find_place(
        input=[name],
        input_type="textquery",
        fields=["formatted_address", "place_id", "geometry/location", "name"],
    )

    res = GoogleApiResponse(**result)

    return res
