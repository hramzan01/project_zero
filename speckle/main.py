import os
import json
import pandas as pd
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv
load_dotenv() 


from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_account_from_token
from specklepy.transports.server import ServerTransport
from specklepy.objects.base import Base
from specklepy.core.api import operations

API_KEY = os.getenv('SPECKLE_API')
SERVER = 'speckle.xyz'
STREAM = 'PZ_Beta'

# 01 HEADER
st.image('speckle/logo.png', width=150)
st.title("PROJECT ZERO: Analytics ")

# 02 CLIENT
client = SpeckleClient(host=SERVER)
account = get_account_from_token(API_KEY, SERVER)
client.authenticate_with_account(account)

# 03 STREAM
# list of available streams
streams = client.stream.list()
stream = client.stream.search(STREAM)[0]

# 04 BRANCH
branches = client.branch.list(stream.id)
commits = client.commit.list(stream.id, limit=100)
    
# 05 VIEWER👁‍🗨
def commit2viewer(stream, commit, height=400) -> str:
    embed_src = f"https://speckle.xyz/embed?stream={stream.id}&commit={commit.id}"
    return st.components.v1.iframe(src=embed_src, height=height)

commit2viewer(stream, commits[0])

# 06 DATA

# Fetch the latest commit
latest_commit = commits[0]

# Get the object ID from the commit
object_id = latest_commit.referencedObject

# Initialize the server transport
transport = ServerTransport(client=client, stream_id=stream.id)

# Receive the object
speckle_object = operations.receive(object_id, transport)


for element in speckle_object.elements:
    st.write(element.name)
    
# print(speckle_object.elements[0].name)
