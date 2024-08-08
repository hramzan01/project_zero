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
STREAM = 'revit2spevit'

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
typologies = []
areas = []
buildings = []
plots = []

for element in speckle_object.elements:
    for subelement in element.elements:
        typologies.append(element.name)
        areas.append(int(subelement.area))
        buildings.append(getattr(subelement.userStrings, 'Building', None))
        plots.append(getattr(subelement.userStrings, 'Plot', None))

# Create DataFrame
data = {
    "Typology": typologies,
    "Area (m2)": areas,
    "Building ID": buildings,
    "Plot ID": plots
}

df = pd.DataFrame(data)

# Remove duplicates
df.drop_duplicates(inplace=True)

# Sort by Building ID
df.sort_values(by="Building ID", inplace=True)

# Display metrics
chart1, chart2, chart3 = st.columns((1, 1, 1))
col1, col2, col3, col4 = st.columns((1, 1, 1, 1))

with col1:
    st.metric(label="Building Typologies 🏢", value=len(df["Typology"].unique()))

with col2:
    st.metric(label="Building Areas 📏", value=len(df["Area (m2)"]))

with col3:
    st.metric(label="Building IDs 🪪", value=len(df["Building ID"].unique()))

with col4:
    st.metric(label="Plot IDs 🪪", value=len(df["Plot ID"].unique()))

# Display DataFrame
st.dataframe(df,use_container_width=True)

# Display Charts

with chart1:
    # bar chart of areas by typology
    fig = px.bar(df, x="Typology", y="Area (m2)", title="Building Areas by Typology")
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    # pie chart of areas by building ID
    fig = px.pie(df, names="Typology", values="Area (m2)", title="Areas by Typology")
    st.plotly_chart(fig, use_container_width=True)

with chart3:
    # histogram of areas by typology
    fig = px.histogram(df, x="Area (m2)", title="Area Distribution")
    st.plotly_chart(fig, use_container_width=True)
