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
from datetime import datetime as dt
from math import floor
import jsonpickle
# import os

# Twitter crawling (possibly not needed here in future versions)
import tweepy

# Streamlit Web App
import streamlit as st

# Own Functions
from helpers.db_functions import *
from helpers.twitter_api import *

### STREAMLIT Init:

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="Query Builder", page_icon=":open_book:")

# Some helper variables
twitter_query = False
oalex_query = False
scopus_query = False
arxiv_query = False

submit_basic = False
submit_advanced = False
submit_query = False

# Start of the page

st.title("📖 Query Builder")

st.write("A simple tool to build queries and specify search tasks for different sources. First, you have to choose a valid project. If you don't see any projects, head over to the Project Creator or check the database connection.")

dropdown_project, col_twitter, col_openalex, col_scopus, col_arxiv = st.columns([8, 1, 1, 1, 1])

with dropdown_project:
    list_of_projects = list_projects()
    df_list_of_projects = pd.DataFrame(list_of_projects)
    option = st.selectbox(
        'Project for Query Builder:',df_list_of_projects["id"])
with col_twitter:
    if (df_list_of_projects.loc[df_list_of_projects['id'] == option, 'use_twitter']).item():
       st.metric(label="Twitter", value="✔")
       twitter_query = True
    else:
        st.metric(label="Twitter", value="❌")
with col_openalex:
    if (df_list_of_projects.loc[df_list_of_projects['id'] == option, 'use_oalex']).item():
       st.metric(label="Open ALEX", value="✔")
       oalex_query = True
    else:
        st.metric(label="Open ALEX", value="❌")
with col_scopus:
    if (df_list_of_projects.loc[df_list_of_projects['id'] == option, 'use_scopus']).item():
       st.metric(label="Scopus", value="✔")
       scopus_query = True
    else:
        st.metric(label="Scopus", value="❌")
with col_arxiv:
    if (df_list_of_projects.loc[df_list_of_projects['id'] == option, 'use_arxiv']).item():
       st.metric(label="arXiv", value="✔")
       arxiv_query = True
    else:
        st.metric(label="arXiv", value="❌")

col_pj_name, col_pj_desc = st.columns([1, 1])

with col_pj_name:
    st.metric(label="Name of the Project", value=df_list_of_projects.loc[df_list_of_projects['id'] == option, 'name'].iloc[0])

with col_pj_desc:
    st.metric(label="Description", value=df_list_of_projects.loc[df_list_of_projects['id'] == option, 'description'].iloc[0])


query_exists, db_search_params = get_twitter_query(option)

tab_twitter, tab_oalex, tab_scopus, tab_arxiv = st.tabs(["Twitter", "Open ALEX", "Scopus", "arXiv"])

with tab_twitter:

    if twitter_query:

        if query_exists:
                    st.info("We found an existing query. Updating and deleting will be available soon! Head over to pgAdmin to manually edit or delete the query.", icon="ℹ️")

                    st.write(db_search_params)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        update_basic = st.button(label="Update", disabled=True)

                    with col2:
                        delete_basic = st.button(label="Delete", disabled=True)
        else:

            tab1, tab2, tab3 = st.tabs(["Basic Twitter Search", "Advanced Twitter Search", "Raw Query"])

            with tab1:
                st.write("A very basic twitter search for the most recent tweets (without Retweets).")
                with st.form("basic_twitter_form"):

                    search_params_basic = {}

                    a, b = st.columns([1, 1])
                    search_params_basic["query"] = a.text_input("Search Term", placeholder="Spaghetti")
                    search_params_basic["limit"] = b.slider("Tweet limit", 1, 100, 50)

                    submit_basic = st.form_submit_button(label="Submit")
            with tab2:
                with st.form("advanced_twitter_form"):
                    search_params_adv = {}

                    relative_dates = {
                        "1 day ago": 1,
                        "1 week ago": 7,
                        "2 weeks ago": 14,
                        "1 month ago": 30,
                    }

                    search_params_adv["query"] = st.text_input("Query", placeholder="(AI AND Machine Learning) OR Reinforcement Learning")
                    search_params_adv["limit"] = st.slider("Tweet limit", 1, 1024, 50)

                    a, b, c, d = st.columns([1, 1, 1, 1])
                    search_params_adv["min_replies"] = a.number_input("Minimum replies", 0, None, 0)
                    search_params_adv["min_retweets"] = b.number_input("Minimum retweets", 0, None, 0)
                    search_params_adv["min_faves"] = c.number_input("Minimum hearts", 0, None, 0)
                    selected_rel_date = d.selectbox("Search from date", list(relative_dates.keys()), 3)
                    search_params_adv["days_ago"] = relative_dates[selected_rel_date]

                    a, b, c  = st.columns([1, 2, 1])
                    search_params_adv["exclude_replies"] = a.checkbox("Exclude replies", False)
                    search_params_adv["exclude_retweets"] = b.checkbox("Exclude retweets", False)

                    submit_advanced = st.form_submit_button(label="Submit")
            with tab3:
                with st.form("raw_twitter_query_form"):
                    search_params_query = {}

                    search_params_query["query"] = st.text_area("Query", placeholder="has:geo (from:NWSNHC OR from:NHC_Atlantic OR from:NWSHouston OR from:NWSSanAntonio OR from:USGS_TexasRain OR from:USGS_TexasFlood OR from:JeffLindner1) -is:retweet")
                    st.markdown("See [Twitter API Examples](https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query#examples).")

                    submit_query = st.form_submit_button(label="Submit")
    elif twitter_query == False:
        st.error('Twitter Crawl was not specified in the project.', icon="🚨")

with tab_oalex:
    if oalex_query:
        st.info("This service will be available soon!", icon="ℹ️")
    elif oalex_query == False:
        st.error('Open ALEX Crawl was not specified in the project.', icon="🚨")

with tab_scopus:
    if scopus_query:
        st.info("This service will be available soon!", icon="ℹ️")
    elif scopus_query == False:
        st.error('Scopus Crawl was not specified in the project.', icon="🚨")

with tab_arxiv:
    if arxiv_query:
        st.info("This service will be available soon!", icon="ℹ️")
    elif arxiv_query == False:
        st.error('ArXiv Crawl was not specified in the project.', icon="🚨")


# ------------------------------------------------------------------------------

if submit_basic:

    search_params_basic["min_replies"] = 0
    search_params_basic["min_retweets"] = 0
    search_params_basic["min_faves"] = 0
    search_params_basic["days_ago"] = None
    search_params_basic["date_to"] = str(dt.now().date())

    search_params_basic["exclude_replies"] = False
    search_params_basic["exclude_retweets"] = False

    search_params_basic["query"] = search_params_basic["query"] + " -RT"
    search_params_basic["ext_query"] = ""

    with st.spinner('Wait while we create the twitter query...'):
        tw_query_created, tw_query_result = create_twitter_query(option, search_params_basic)
        if tw_query_created:
            st.success('The query was created')
        else:
            st.error("There was an unexpected error while creating the query. Please try again or check the database connection.")

# with st.expander("Twitter Search"):
#     tab1, tab2, tab3 = st.tabs(["Basic Twitter Search", "Advanced Twitter Search", "Raw Query"])

#     with tab1:
#         with st.form("basic_twitter_form"):
#             search_params = {}

#             relative_dates = {
#                 "1 day ago": 1,
#                 "1 week ago": 7,
#                 "2 weeks ago": 14,
#                 "1 month ago": 30,
#             }

#             a, b = st.columns([1, 1])
#             search_params["query"] = a.text_input("Search Term", placeholder="Spaghetti")
#             search_params["limit"] = b.slider("Tweet limit", 1, 1024, 50)

#             submit_basic = st.form_submit_button(label="Submit")
#     with tab2:
#         with st.form("advanced_twitter_form"):
#             search_params = {}

#             relative_dates = {
#                 "1 day ago": 1,
#                 "1 week ago": 7,
#                 "2 weeks ago": 14,
#                 "1 month ago": 30,
#             }

#             search_params["query"] = st.text_input("Query", placeholder="(AI AND Machine Learning) OR Reinforcement Learning")
#             search_params["limit"] = st.slider("Tweet limit", 1, 1024, 50)

#             a, b, c, d = st.columns([1, 1, 1, 1])
#             search_params["min_replies"] = a.number_input("Minimum replies", 0, None, 0)
#             search_params["min_retweets"] = b.number_input("Minimum retweets", 0, None, 0)
#             search_params["min_faves"] = c.number_input("Minimum hearts", 0, None, 0)
#             selected_rel_date = d.selectbox("Search from date", list(relative_dates.keys()), 3)
#             search_params["days_ago"] = relative_dates[selected_rel_date]

#             a, b, c  = st.columns([1, 2, 1])
#             search_params["exclude_replies"] = a.checkbox("Exclude replies", False)
#             search_params["exclude_retweets"] = b.checkbox("Exclude retweets", False)

#             submit_advanced = st.form_submit_button(label="Submit")
#     with tab3:
#         with st.form("raw_twitter_query_form"):
#             search_params = {}

#             search_params["query"] = st.text_area("Query", placeholder="has:geo (from:NWSNHC OR from:NHC_Atlantic OR from:NWSHouston OR from:NWSSanAntonio OR from:USGS_TexasRain OR from:USGS_TexasFlood OR from:JeffLindner1) -is:retweet")
#             st.markdown("See [Twitter API Examples](https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query#examples).")

#             submit_query = st.form_submit_button(label="Submit")