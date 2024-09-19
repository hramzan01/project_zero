import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_account_from_token
from specklepy.transports.server import ServerTransport
from specklepy.core.api import operations

def speck_viewer(API_KEY,SERVER, STREAM):

    # 01 CLIENT
    client = SpeckleClient(host=SERVER)
    account = get_account_from_token(API_KEY, SERVER)
    client.authenticate_with_account(account)

    # 02 STREAM
    streams = client.stream.list()
    stream = client.stream.search(STREAM)[0]

    # 03 BRANCH
    branches = client.branch.list(stream.id)
    commits = client.commit.list(stream.id, limit=100)

    # 04 GET OBJECTS
    latest_commit = commits[0]
    object_id = latest_commit.referencedObject
    transport = ServerTransport(client=client, stream_id=stream.id)
    speckle_object = operations.receive(object_id, transport)

    # 05 VIEWER👁‍🗨
    def commit2viewer(stream, commit, height=800) -> str:
        # embed_src = f'https://{SERVER}/embed?stream={stream.id}&commit={commit.id}&autoplay=true&filter=%7B%22propertyInfoKey%22%3A%22userStrings.{USER_STRING}%22%7D' # how to filter by a property
        embed_src = f'https://{SERVER}/embed?stream={stream.id}&commit={commit.id}&autoplay=true'
        return st.components.v1.iframe(src=embed_src, height=height)

    commit2viewer(stream, commits[0])

    return(streams, stream, branches, commits, speckle_object)

'''EXAMPLE USE CASE'''
# API_KEY = os.getenv('SPECKLE_API')
# SERVER = 'speckle.xyz'
# STREAM = 'PZ_Beta'
# USER_STRING = 'Building'

# speck_viewer(API_KEY,SERVER, STREAM, USER_STRING)
