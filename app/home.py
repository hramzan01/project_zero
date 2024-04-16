import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
import streamlit as st
# import plotly.graph_objects as go
from datetime import datetime


import matplotlib.pylab as plt

# import datetime
import requests

from PIL import Image
import os


st.set_page_config(page_title="Project Zero")


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

    # HOME: PZero logo
    # col1, col2, col3 = st.columns([1, 2, 1])

    # Load in images
    logo = Image.open('app/assets/logo.png')
    what = Image.open('app/assets/pz_what.png')
    
    st.image(logo, use_column_width=True)
    st.markdown('')  # Empty markdown line for spacing
    st.markdown('')  # Empty markdown line for spacing
    st.markdown('')  # Empty markdown line for spacing
    st.markdown('')  # Empty markdown line for spacing
    st.markdown('')  # Empty markdown line for spacing


    st.markdown('')
    st.write("""Project Zero&#8482; is a cutting-edge data analytics tool designed to streamline and enhance the management of evolving city projects. By centralizing and facilitating dynamic data tracking, Project Zero&#8482; empowers project stakeholders to adapt and optimize their designs effectively.""")

    st.markdown('')  # Empty markdown line for spacing
    st.markdown('')  # Empty markdown line for spacing
    
    st.image(what, use_column_width=True)

    st.markdown('')  # Empty markdown line for spacing
    st.markdown('')  # Empty markdown line for spacing
    st.markdown('')  # Empty markdown line for spacing
    st.markdown('')  # Empty markdown line for spacing

    
    st.video('app/assets/pz_vid.mp4')

    # Architecture
    st.title('Project Architecture')
    st.image('app/assets/pz_arch.png')

    st.title('Project Features')
    st.write('Project Zero generates comprehensive outputs based on the integrated data, offering insights into various aspects of the project, such as expected energy demand, predicted population growth, and embodied carbon emissions.')

    # Utilities
    st.image('app/assets/pz_utilities.png')
    
    # Carbon
    st.image('app/assets/pz_carbon.png')

    # Population
    st.image('app/assets/pz_population.png')
