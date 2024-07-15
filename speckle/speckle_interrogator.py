from specklepy.api import operations
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_account_from_token
from specklepy.transports.server import ServerTransport
import os

# Replace with your Speckle API key and server URL
API_KEY = os.getenv("SPECKLE_API")
SPECKLE_SERVER = "https://speckle.xyz"  # Update with your Speckle server URL
STREAM_ID = "ee7ebef689"
COMMIT_ID = '187596e290'

# Authenticate with Speckle using API key
client = SpeckleClient(host=SPECKLE_SERVER)
account = get_account_from_token(API_KEY, SPECKLE_SERVER)
client.authenticate_with_account(account)
streams = client.stream.list()
# print(streams)

# Retrieve the specified commit data
commits = client.commit.list(STREAM_ID)
commit = client.commit.get(STREAM_ID, COMMIT_ID)
# print(commits)

# Create an authenticated server transport from the client and receive the commit object
transport = ServerTransport(client=client, stream_id=STREAM_ID)
res_object = operations.receive(commit.referencedObject, transport)

objects = []
# Check if the main object has elements
if hasattr(res_object, 'elements'):
    stack = res_object.elements[:]  # Start with the main object's elements
    while stack:
        element = stack.pop()
        obj = operations.receive(element.id, transport)
        objects.append(obj)

        # If the object has nested elements, add them to the stack
        if hasattr(obj, 'elements'):
            stack.extend(obj.elements)
else:
    # If the main object does not have elements, print it directly
    objects.append(res_object)

for i in objects:
    print(i.name)
    print(i.speckle_type)
