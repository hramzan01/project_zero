import streamlit as st 
import subprocess
from streamlit_option_menu import option_menu

# 1. as a sidebar option_menu
selected = option_menu(
    
    # Configuration
    menu_title='', # req
    options=[' ','Projects','Contact'], # req
    icons=['house','pie-chart','envelope'], #opt
    # menu_icon='cast', #opt
    default_index=0, #opt
    orientation='horizontal',
    
    #Styles
    # styles={
                # "container": {"padding": "0!important", "background-color": "black"},
                # "icon": {"color": "orange", "font-size": "25px"},
                # "nav-link": {
                #     "font-size": "25px",
                #     "text-align": "left",
                #     "margin": "0px",
                #     "--hover-color": "#eee",
                # },
                # "nav-link-selected": {"background-color": "green"},
            # },

    )

if selected == 'Home':
    st.title(f'Project Zero')

if selected == 'Projects':
    project = option_menu(
    
    menu_title='', # req
    options=[' ', 'City Plan','Market'], # req
    icons=[None ,'buildings','lightning'], #opt
    orientation='horizontal', #opt
)
    
    if project == 'City Plan':
        subprocess.run(['streamlit', 'run', 'project_01.py'])
    if project == 'Market':
        st.title('You selected Marktet')


    
if selected == 'Contact':
    contact = option_menu(
    
    menu_title='', # req
    options=['', '', ''], # req
    icons=['github' ,'linkedin', 'medium'], #opt
    orientation='horizontal', #opt
)