####################################################################################
# Settings Page
# by JW
#
# Manage Settings and Session States
# 
# Home.py / Settings.py
####################################################################################

# IMPORT STATEMENTS ----------------------------------------------------------------
import streamlit as st

# Own Functions
from helpers.db_functions import *


# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="Settings", page_icon="⚙")

project_submit = st.session_state["project_submit"]

st.title("⚙ Settings")

st.write("TIE Trend Navigator Settings")