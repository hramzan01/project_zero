import streamlit as st 
import subprocess
from streamlit_option_menu import option_menu


# 1. as a sidebar option_menu
selected = option_menu(
    
    menu_title='', # req
    options=[' ', 'Home','Market'], # req
    icons=[None ,'home','lightning'], #opt
    orientation='horizontal', #opt
)

st.title('City Plan: Developing design of future cities')
'this is an example of some text to see how steamlit picks it up.'


if selected == 'Home':
    subprocess.run(['streamlit', 'run', 'home.py'])

if selected == 'Market':
    subprocess.run(['streamlit', 'run', 'project_02.py'])