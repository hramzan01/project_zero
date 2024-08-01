import streamlit as st
import pandas as pd

from specklepy.api.wrapper import StreamWrapper # import the StreamWrapper class from the specklepy.api.wrapper module
from specklepy.api.client import SpeckleClient # entrypoint for the Speckle API
from specklepy.api import operations # import the operations module from the specklepy.api package

#container
header = st.container()
input = st.container()
data = st.container()

with header:
    st.title('Speckle Stream Data Schedule ⚙️ ')
    st.info('This app is a demonstration of how to use the Speckle API to access data from a Speckle Stream. ')

with input:
    URL = 'https://app.speckle.systems/projects/71ba43d958/models/b038c41ae2@cbf42ffe6e'
    st.subheader('Input Data')
    commit_url = st.text_input('Commit URL', URL)
    
    wrapper = StreamWrapper(commit_url) 
    client = wrapper.get_client()
    transport = wrapper.get_transport()
    
#commit object
commit = client.commit.get(wrapper.stream_id, wrapper.commit_id)
commit 
    
#get object id from commit
object_id = commit.referencedObject
commit_data = operations.receive(object_id, transport)

check = commit_data['elements'][0]['name']
check
names = commit_data.get_member_names()
names
