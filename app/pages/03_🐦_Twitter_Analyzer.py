####################################################################################
# Twitter Analyzer
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
st.set_page_config(layout="wide", page_title="Twitter Analyzer", page_icon="🐦")

# Start of the page

st.title("🐦 Twitter Analyzer")

st.write("The gateway to analyze twitter queries")

# SIDEBAR --------------------------------------------

with st.sidebar:
    st.header("Project selection")

    list_of_projects = list_projects()
    df_list_of_projects = pd.DataFrame(list_of_projects)
    option = st.selectbox(
        'Project with Twitter data:',df_list_of_projects["id"])

    query_exists, db_search_params = get_twitter_query(option)

    if query_exists:
        st.metric(label="Query", value=db_search_params["query"])
        st.metric(label="Last crawled", value=str(db_search_params["last_crawl"]))
        st.metric(label="Tweet limit", value=db_search_params["tweet_limit"])
    else:
        st.error('Twitter query was not found.', icon="🚨")

if query_exists:
    if st.button("Run new crawl"):
        with st.spinner('Wait while we collect the tweets...'):
            try:
                #tweets = get_tweets(search_params_basic)
                twitter_client_v2 = st.session_state.twitter_client_v2
                tweets = twitter_client_v2.search_recent_tweets(query=db_search_params["query"], end_time=None, max_results=db_search_params["tweet_limit"], tweet_fields=st.session_state.twitter_tweet_fields, expansions="author_id")
                # for tweet in tweets.data:
                #     st.write(tweet)
                st.session_state.temp_tweets = tweets


                st.success('Done!')
            except Exception as e:
                st.error("There was an unexpected error while collecting the tweets. Please try again and double check your API credentials.")
                st.write(e)

    if st.button("Analyze"):
        temp_tweets_data = (st.session_state.temp_tweets).data
        temp_tweets_includes = (st.session_state.temp_tweets).includes
        users = {u["id"]: u for u in temp_tweets_includes['users']}    
        # for tweet in temp_tweets.data:
        #     if users[tweet.author_id]:
        #         user = users[tweet.author_id]
        #         st.write(user)
        #         st.write(user.profile_image_url)


        for result in paginator(temp_tweets_data, 10, "tweet_next", "tweet_prev"):
            display_tweet(result, users)
            "---"