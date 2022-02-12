from dataclasses import dataclass
import os
from typing import Any, Optional

import googlemaps
from dotenv import load_dotenv

load_dotenv(verbose=True)

gmaps = googlemaps.Client(key=os.environ.get("GOOGLE_MAP_API_KEY"))


@dataclass
class Location:
    lat: float
    lng: float


@dataclass
class Viewport:
    northeast: Location
    southwest: Location

    def __post_init__(self) -> None:
        self.northeast = Location(**self.northeast)
        self.southwest = Location(**self.southwest)


@dataclass
class Geometry:
    location: Location
    viewport: Viewport

    def __post_init__(self) -> None:
        self.location = Location(**self.location)
        self.viewport = Viewport(**self.viewport)


@dataclass
class PlusCode:
    compound_code: str
    global_code: str


@dataclass
class Candidate:
    formatted_address: str
    name: str
    place_id: str
    geometry: Geometry
    types: list[str]
    business_status: Optional[str] = ""
    plus_code: Optional[PlusCode] = None

    def __post_init__(self) -> None:
        self.geometry = Geometry(**self.geometry)
        if self.plus_code:
            self.plus_code = PlusCode(**self.plus_code)


@dataclass
class GoogleApiResponse:
    candidates: list[Candidate]
    status: str

    def __post_init__(self) -> None:
        self.candidates = [Candidate(**candidate) for candidate in self.candidates]


def find_place(name: str) -> GoogleApiResponse:
    result: dict[str, Any] = gmaps.find_place(
        input=[name],
        input_type="textquery",
        fields=[
            "formatted_address",
            "place_id",
            "geometry",
            "name",
            "types",
            "business_status",
            "plus_code",
        ],
    )
    return GoogleApiResponse(**result)
