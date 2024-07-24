import os
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

# set streamlit to force wide mode
st.set_page_config(layout="wide")


API_KEY = os.getenv('SPECKLE_API')
SERVER = 'speckle.xyz'
STREAM = 'PZ_Beta'

# 01 HEADER
hl, space, hr = st.columns((1, 5, 1,))
with hr:
    st.image('speckle/pz_logo.png', width=200)

with hl:
    st.image('speckle/logo.png', width=250)

st.title("PROJECT ZERO: Project Analytics")

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
def commit2viewer(stream, commit, height=800) -> str:
    embed_src = f"https://{SERVER}/embed?stream={stream.id}&commit={commit.id}"
    return st.components.v1.iframe(src=embed_src, height=height)

commit2viewer(stream, commits[0])

# 06 GET OBJECTS
latest_commit = commits[0]
object_id = latest_commit.referencedObject
transport = ServerTransport(client=client, stream_id=stream.id)
speckle_object = operations.receive(object_id, transport)




# 07 ACCESS DATA
# create 3 streamlit columns
col1, col2, col3, col4 = st.columns((1, 1, 1, 1))

with col1:
    # typologies
    typologies = [element.name for element in speckle_object.elements]
    st.metric(label="Building Typologies 🏢", value=len(typologies))
    typologies

with col2:
    # areas
    areas = []
    for element in speckle_object.elements:
        for subelement in element.elements:
            areas.append(f'{int(subelement.area)}m2')
            
    st.metric(label="Building Areas 📏", value=len(areas))
    areas

with col3:
    buildings = []
    for element in speckle_object.elements:
        for subelement in element.elements:
            building_id = getattr(subelement.userStrings, 'Building', None)
            if building_id:
                buildings.append(building_id)

    # Remove duplicates and sort
    unique_building_ids = sorted(set(buildings))

    st.metric(label="Building IDs 🪪", value=len(unique_building_ids))
    st.write(unique_building_ids)

with col4:
    plots = []
    for element in speckle_object.elements:
        for subelement in element.elements:
            plot_id = getattr(subelement.userStrings, 'Plot', None)
            if plot_id:
                plots.append(plot_id)

    # Remove duplicates and sort
    unique_plot_ids = sorted(set(plots))

    st.metric(label="Plot IDs 🪪", value=len(unique_plot_ids))
    st.write(unique_plot_ids)
