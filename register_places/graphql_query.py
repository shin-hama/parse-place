from dataclasses import asdict, dataclass
from typing import Literal
import os
from typing import Any

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from dotenv import load_dotenv
from graphql import DocumentNode

from util import read_json


load_dotenv(verbose=True)

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(
    url=os.environ.get("HASURA_URL", ""),
    headers={"x-hasura-admin-secret": os.environ.get("HASURA_API_KEY", ""), "x-hasura-role": "dev"},
)

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True, execute_timeout=None)


def exec_query(q: DocumentNode, param: dict[str, Any] = None) -> dict[str, Any]:
    # Execute the query on the transport
    result = client.execute(q, variable_values=param)
    return result


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


@dataclass
class SpotSchema:
    name: str
    lat: float
    lng: float
    prefecture_code: int
    place_id: str
    spots_types: dict[
        Literal["data"],
        list[
            dict[
                Literal["type"],
                dict[Literal["data", "on_conflict"], dict[Literal["name", "constraint", "update_columns"], str]],
            ]
        ],
    ]


def insert_spots(schemas: list[SpotSchema]) -> None:
    mutation = gql(
        """
        mutation MyMutation($objects: [spots_insert_input!]!) {
            insert_spots(objects: $objects) {
                affected_rows
            }
        }
    """
    )

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


def get_types():
    m = gql(
        """
        query MyQuery {
            types {
                name
                id
                spots_types {
                    spot_id
                }
            }
        }
        """
    )
    result = exec_query(m)
    print(result["types"][0])

    formatted = [{"name": r["name"], "id": r["id"], "len": len(r["spots_types"])} for r in result["types"]]
    print(formatted[0])
    import json

    with open("test.json", mode="w", encoding="utf-8") as f:
        json.dump(formatted, f)


def update_prefecture_place_id():
    m = gql(
        """
        mutation MyMutation($name: String!, $place_id: String!) {
            update_prefectures(where: {name: {_eq: $name}}, _set: {place_id: $place_id}) {
                affected_rows
            }
        }
        """
    )

    prefectures = read_json("prefectures.json")
    for p in prefectures:
        param = {"name": p["candidates"][0]["name"], "place_id": p["candidates"][0]["place_id"]}
        print(param)
        exec_query(m, param)


get_types()
