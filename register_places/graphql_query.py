from dataclasses import asdict, dataclass
import os
from typing import Any
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from dotenv import load_dotenv
from graphql import DocumentNode

from constants.prefectures_code import pref_code
from check_place_result import read_cities

load_dotenv(verbose=True)

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(
    url=os.environ.get("HASURA_URL", ""),
    headers={"x-hasura-admin-secret": os.environ.get("HASURA_API_KEY", ""), "x-hasura-role": "dev"},
)

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)


def exec_query(q: DocumentNode, param: dict[str, Any] = None) -> None:
    # Execute the query on the transport
    result = client.execute(q, variable_values=param)
    print(result)


def insert_types(types: list[str]) -> None:
    mutation = gql(
        """
        mutation MyMutation($objects: [spot_types_insert_input!]!) {
            insert_spot_types(objects: $objects) {
                affected_rows
                returning {
                    name
                    id
                }
            }
        }
        """
    )

    param = {"objects": [{"name": name} for name in types]}
    exec_query(mutation, param)


def add_spots() -> None:

    mutation = gql(
        """
    mutation MyMutation($objects: [spots_insert_input!] = {}) {
    insert_spots(objects: $objects) {
        affected_rows
    }
    }
    """
    )

    @dataclass
    class CitySchema:
        name: str
        lat: float
        lng: float
        prefecture_code: int
        place_id: str
        type_id: int = 1

    def parse_cities() -> list[CitySchema]:
        cities = read_cities()

        schemas = [
            CitySchema(
                name=city.name,
                lat=city.geometry.location.lat,
                lng=city.geometry.location.lng,
                prefecture_code=pref_code[city.prefecture],
                place_id=city.place_id,
            )
            for city in cities
        ]

        return schemas

    schemas = parse_cities()
    test = [asdict(schema) for schema in schemas]
    param = {"objects": test}

    exec_query(mutation, param)


def add_city_type() -> None:
    test = [
        {"place_id": "ChIJO-USq4MmdV8RYREnMTSMkns"},
    ]
    m = gql(
        """
        mutation MyMutation($objects: [spot_type_insert_input!] = {}) {
            insert_spot_type(objects: $objects) {
                affected_rows
            }
        }
        """
    )
    param = {"objects": [{"spot_id": t["place_id"], "type_id": 1} for t in test]}
    exec_query(m, param)
