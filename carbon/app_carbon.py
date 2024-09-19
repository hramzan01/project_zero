import streamlit as st
import os
import pandas as pd
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

# Load the speckle viewer
# speck_viewer(API_KEY,SERVER, STREAM)
streams, stream, branches, commits, speckle_object = speck_viewer(API_KEY,SERVER, STREAM)

'''streams'''
st.write(streams)

'''stream'''
st.write(stream)

'''branches'''
st.write(branches)

'''commits'''
st.write(commits)

'''speckle_object'''
st.write(speckle_object)


# load the carbon table
carbon_data = 'carbon/data/ICE_SPICE.csv'
df = pd.read_csv(carbon_data, skiprows=1)

# df.columns
# df


materials = df['Material'].unique()
material = st.selectbox('Select a material', materials)

# filter the data based on the material
df = df[df['Material'] == material]
df = df[[
    # 'Material',
    'Sub-material',
    'ICE DB Name',
    'Units of declared unit',
    'Density of material - kg per m3',
    'Embodied Carbon per kg (kg CO2e per kg)',
    'Average Embodied Carbon - kg CO2e per kg']]

st.dataframe(df)

# create plotly chart with embodied carbon per kg by sub-material
df_chart = df[['Sub-material', 'Average Embodied Carbon - kg CO2e per kg']]
st.bar_chart(df_chart.set_index('Sub-material'), height=700)





# drop down menu for material selection
