from specklepy.api import operations
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_account_from_token
from specklepy.transports.server import ServerTransport
import os

# Replace with your Speckle API key and server URL
API_KEY = os.getenv("SPECKLE_API")
SPECKLE_SERVER = "https://speckle.xyz"  # Update with your Speckle server URL
STREAM_ID = "467a461a84"
COMMIT_ID = '24be54f603'

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


''' FOR THE BREP DATA '''
# Retrieve the Brep object from Speckle
brep_object = client.object.get(object_id='99fd6a7561d5b47a6e8c52bbc7ed057d', stream_id = STREAM_ID)

# Print basic properties of the Brep
print(f"Brep Geometry Properties:")
print(f"Area: {brep_object.area}")
print(f"Volume: {brep_object.volume}")
print(f"Is Closed: {brep_object.IsClosed}")
print(f"Provenance: {brep_object.provenance}")
print(f"Orientation: {brep_object.Orientation}")
print(f"Speckle Type: {brep_object.speckle_type}")

# # Print user strings (custom data)
# if 'userStrings' in brep_object:
#     print("\nUser Strings (Custom Data):")
#     user_strings = brep_object.userStrings
#     for key, value in user_strings.items():
#         print(f"{key}: {value}")




''' FOR THE MESH DATA '''
# res_object = operations.receive(commit.referencedObject, transport)

# objects = []
# # Check if the main object has elements
# if hasattr(res_object, 'elements'):
#     stack = res_object.elements[:]  # Start with the main object's elements
#     while stack:
#         element = stack.pop()
#         obj = operations.receive(element.id, transport)
#         objects.append(obj)

#         # If the object has nested elements, add them to the stack
#         if hasattr(obj, 'elements'):
#             stack.extend(obj.elements)
# else:
#     # If the main object does not have elements, print it directly
#     objects.append(res_object)

# for object in objects:
#     # print(object)
#     print(object.area)
#     print('')
