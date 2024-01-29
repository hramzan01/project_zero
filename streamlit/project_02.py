import streamlit as st 
import subprocess
from streamlit_option_menu import option_menu


# 1. as a sidebar option_menu
selected = option_menu(
    
    menu_title='', # req
    options=[' ', 'Home','City Plan'], # req
    icons=[None ,'home','buildings'], #opt
    orientation='horizontal', #opt
)

st.title('Market: community trading platform for renewable energy')
'this is an example of some text to see how steamlit picks it up.'


if selected == 'Home':
    subprocess.run(['streamlit', 'run', 'home.py'])

if selected == 'City Plan':
    subprocess.run(['streamlit', 'run', 'project_01.py'])