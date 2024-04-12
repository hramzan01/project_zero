import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime


import matplotlib.pylab as plt

# import datetime
import requests

from PIL import Image
import os


st.set_page_config(page_title="Market", initial_sidebar_state="collapsed", layout='wide')


# Background
st.markdown(

    """
    <style>
    # [data-testid="stHeader"] {
    #     background-color: #00008b;
    # }
    </style>
    """
    """
    <style>
    [data-testid="stApp"] {
        background: linear-gradient(180deg, rgba(0, 0, 139, 1) 0%, rgba(0,0,0) 47%, rgba(0,0,0) 100%);
        height:auto;
    }
    </style>
    """
    """
    <style>
    [data-testid="stSlider"] {
        background-color: #EEF0F4;
        border-radius: 5px;
        padding: 10px;
    }
    </style>
    """
    """
    <style>
        .stPlotlyChart {
            border-radius: 10px;
            overflow: hidden; /* This is important to ensure the border radius is applied properly */
        }
    </style>
    """,
    unsafe_allow_html=True
)

with st.container():
    # HOME: MARKET logo
    col1, col2, col3 = st.columns([2, 1, 2])

    # Open the image
    image = Image.open('app/assets/logo.png')

    # Display the image with a custom width
    col2.image(image)