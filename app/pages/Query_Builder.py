####################################################################################
# Query Builder
# by JW
#
# A simple python tool to build queries and specify search tasks for different sources
# 
# pages / Query_Builder.py
####################################################################################

# IMPORT STATEMENTS ----------------------------------------------------------------

import pandas as pd
import numpy as np
import datetime
from math import floor
import jsonpickle
# import os

# Twitter crawling (possibly not needed here in future versions)
import tweepy

# Streamlit Web App
import streamlit as st

### STREAMLIT Init:

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="centered", page_title="Query Builder", page_icon=":open_book:")

# Some Session State Initializations -------

logo, title = st.columns([1, 5])

with logo:
    st.image("assets/logo.png")
with title:
    st.title("Query Builder")

st.write("A simple tool to build queries and specify search tasks for different sources.")
st.write("")
st.write("First, you have to choose a valid project. If you don't see any projects, head over to the Project Creator page or check the database connection.")

option = st.selectbox(
    'Project for Query Builder:',)

with st.expander("Twitter Search"):
    tab1, tab2, tab3 = st.tabs(["Basic Twitter Search", "Advanced Twitter Search", "Raw Query"])

    with tab1:
        with st.form("basic_twitter_form"):
            search_params = {}

            relative_dates = {
                "1 day ago": 1,
                "1 week ago": 7,
                "2 weeks ago": 14,
                "1 month ago": 30,
            }

            a, b = st.columns([1, 1])
            search_params["query"] = a.text_input("Search Term", placeholder="Spaghetti")
            search_params["limit"] = b.slider("Tweet limit", 1, 1024, 50)

            submit_basic = st.form_submit_button(label="Submit")
    with tab2:
        with st.form("advanced_twitter_form"):
            search_params = {}

            relative_dates = {
                "1 day ago": 1,
                "1 week ago": 7,
                "2 weeks ago": 14,
                "1 month ago": 30,
            }

            search_params["query"] = st.text_input("Query", placeholder="(AI AND Machine Learning) OR Reinforcement Learning")
            search_params["limit"] = st.slider("Tweet limit", 1, 1024, 50)

            a, b, c, d = st.columns([1, 1, 1, 1])
            search_params["min_replies"] = a.number_input("Minimum replies", 0, None, 0)
            search_params["min_retweets"] = b.number_input("Minimum retweets", 0, None, 0)
            search_params["min_faves"] = c.number_input("Minimum hearts", 0, None, 0)
            selected_rel_date = d.selectbox("Search from date", list(relative_dates.keys()), 3)
            search_params["days_ago"] = relative_dates[selected_rel_date]

            a, b, c  = st.columns([1, 2, 1])
            search_params["exclude_replies"] = a.checkbox("Exclude replies", False)
            search_params["exclude_retweets"] = b.checkbox("Exclude retweets", False)

            submit_advanced = st.form_submit_button(label="Submit")
    with tab3:
        with st.form("raw_twitter_query_form"):
            search_params = {}

            search_params["query"] = st.text_area("Query", placeholder="has:geo (from:NWSNHC OR from:NHC_Atlantic OR from:NWSHouston OR from:NWSSanAntonio OR from:USGS_TexasRain OR from:USGS_TexasFlood OR from:JeffLindner1) -is:retweet")
            st.markdown("See [Twitter API Examples](https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query#examples).")

            submit_query = st.form_submit_button(label="Submit")