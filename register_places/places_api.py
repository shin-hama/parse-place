import os

import googlemaps
from dotenv import load_dotenv

load_dotenv(verbose=True)

gmaps = googlemaps.Client(key=os.environ.get("GOOGLE_MAP_API_KEY"))


def find_place(name: str) -> dict:
    result: dict = gmaps.find_place(
        input=[name],
        input_type="textquery",
        fields=["formatted_address", "place_id", "geometry/location", "name"],
    )
    print(result)

    return result
