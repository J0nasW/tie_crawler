####################################################################################
# PAGE DIVIDER
# by JW
#
# Manage Settings and Session States
# 
# pages / 61_xxxxxxx EXPERIMENTAL PAGES xxxxxxx.py
####################################################################################

# IMPORT STATEMENTS ----------------------------------------------------------------
import streamlit as st

# Own Functions
from helpers.db_functions import *


# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="Settings", page_icon="⚙")

project_submit = st.session_state["project_submit"]

st.title("🥽 Experimental Pages")

st.write("TIE Trend Navigator Settings")