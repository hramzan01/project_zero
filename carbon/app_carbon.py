import streamlit as st
import os
from speck.main import speck_viewer
from PIL import Image


# Set the page layout
st.set_page_config(layout="wide")

# Load the speckle viewer
speck_viewer()
