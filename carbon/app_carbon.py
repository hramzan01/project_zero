import streamlit as st
import os
from speck.main import speck_viewer
from PIL import Image


# Set the page layout
st.set_page_config(layout="wide")

# 01 HEADER
hl, space, hr = st.columns((1, 5, 1,))

with hr:
    st.image('speckle/pz_logo.png', width=200)

with hl:
    st.image('speckle/logo.png', width=250)

st.title("PROJECT ZERO: Carbon Calculator")

API_KEY = os.getenv('SPECKLE_API')
SERVER = 'speckle.xyz'
STREAM = 'PZ_Beta'
USER_STRING = 'Building'

# Load the speckle viewer
speck_viewer(API_KEY,SERVER, STREAM, USER_STRING)
