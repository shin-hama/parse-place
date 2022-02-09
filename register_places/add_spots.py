import os
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

from dotenv import load_dotenv

load_dotenv(verbose=True)

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(
    url=os.environ.get("HASURA_URL", ""),
    headers={"x-hasura-admin-secret": os.environ.get("HASURA_API_KEY", ""), "x-hasura-role": "dev"},
)

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Provide a GraphQL query
query = gql(
    """
    query MyQuery {
        prefectures {
            name
            code
        }
    }
"""
)

# Execute the query on the transport
result = client.execute(query)
print(result)
