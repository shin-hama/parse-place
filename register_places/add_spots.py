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
mutation MyMutation($objects: [spots_insert_input!] = {}) {
  insert_spots(objects: $objects) {
    affected_rows
  }
}
"""
)

q = gql(
    """
query MyQuery {
  spots {
    place_id
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
            lat=city.geometry["location"]["lat"],
            lng=city.geometry["location"]["lng"],
            prefecture_code=pref_code[city.prefecture],
            place_id=city.place_id,
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
