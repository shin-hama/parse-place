from dataclasses import asdict, dataclass
import os
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from dotenv import load_dotenv

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

mutation = gql(
    """
    mutation MyMutation($objects: [cities_insert_input!]!) {
        insert_cities(objects: $objects) {
            returning {
                id
                name
                created_at
            }
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


def parse_cities() -> list[CitySchema]:
    cities = read_cities()

    schemas = [
        CitySchema(
            name=city.name,
            lat=city.geometry["location"]["lat"],
            lng=city.geometry["location"]["lng"],
            prefecture_code=pref_code[city.prefecture],
        )
        for city in cities
    ]

    return schemas


schemas = parse_cities()
test = [asdict(schema) for schema in schemas]
param = {"objects": test}

# Execute the query on the transport
result = client.execute(mutation, variable_values=param)
print(result)
