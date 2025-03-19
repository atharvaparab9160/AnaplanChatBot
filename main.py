import pandas as pd
import pickle
import requests
import streamlit as st
st.set_page_config(
        page_title="Anaplan ChatBot",
        page_icon="chart_with_upwards_trend",
        layout="wide",
)
from datetime import date
from streamlit_option_menu import option_menu



##############################################
######## importing chatting as text ##########
##############################################
import Anaplan_textForm

#############################################
##### importing chatting as Visualization ###
#############################################
import Anaplan_visualization




class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run(self):

        with st.sidebar:
            apps_op  = option_menu(
                menu_title='Anaplan ChatBot',
                options=['Chat With Data', '---' ,'Get Visualization'],
                icons=['house-fill',"house-fill","house-fill"],
                menu_icon='film',
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "23px" },
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "5px",
                                 "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"}, }
            )


        if apps_op == "Chat With Data":
            Anaplan_textForm.app()
        elif apps_op == "Get Visualization":
            Anaplan_visualization.app()


RunObj = MultiApp()
RunObj.run()
