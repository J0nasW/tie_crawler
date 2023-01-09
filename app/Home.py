####################################################################################
# Home
# by JW
#
# Starting point for the TIE Trend Analyzer
# 
# Home.py
####################################################################################

# IMPORT STATEMENTS ----------------------------------------------------------------


import pandas as pd
import numpy as np
import datetime
import jsonpickle
# import os

# Twitter crawling (possibly not needed here in future versions)
import tweepy

# Streamlit Web App
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# ToDo: Streamlit Auth (https://blog.streamlit.io/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/)
# import streamlit_authenticator as stauth

# Own Functions
from helpers.first_init import *

# INITIALIZATION OF THE APPLICATION -------------------------------------------------

### STREAMLIT Init:

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="TIE Trend Navigator", page_icon="📈")

### General Init:
if "app_init" not in st.session_state:
    init_application()

# START OF THE APPLICATION -------------------------------------------------------------------


st.image("assets/logo_wide.png", width=600, clamp=True)
st.title("📈 TIE Trend Navigator")

st.write("Welcome to the TIE Trend Navigator. With this app, you can easily discover trends and crawl useful data from a lot of different data-sources.")
st.caption("In order to work, the Trend Navigator uses API access from most of its sources. Please head over to the settings page to provide suitable API credentials or store them as secrets in a secrets.toml file (or online).")

st.write("")
st.write("")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    if st.button("🐦 Twitter API"):
        switch_page("Twitter API")

with col2:
    if st.button("🏢 OpenCorporates API"):
        switch_page("OpenCorporates API")

with col3:
    if st.button("📄 OpenALEX API"):
        switch_page("OpenCorporates API")

with col4:
    if st.button("📘 Scopus API"):
        switch_page("OpenCorporates API")

with col5:
    if st.button("🗄 arXiv API"):
        switch_page("OpenCorporates API")

with col6:
    if st.button("⚙ Settings"):
        switch_page("Settings")


# st.image("assets/tw_sentiment_banner.jpg", use_column_width="auto")
        
        


# SIDEBAR --------------------------------------------

#with st.sidebar:
