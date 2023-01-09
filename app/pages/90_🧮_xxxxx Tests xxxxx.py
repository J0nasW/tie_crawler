####################################################################################
# Some tests
# by JW
#
# ...
# 
# pages / tests.py
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
st.set_page_config(layout="wide", page_title="Tests", page_icon="🧮")

# Start of the page

st.title("🧮 Tests")

st.write("Some Tests")

if st.button("Search all tweets"):
    tw_client = connect_twitter_api_v2()
    fields = ["attachments", "author_id", "context_annotations", "conversation_id", "created_at", "edit_controls", "entities", "geo", "id", "in_reply_to_user_id", "lang", "public_metrics", "possibly_sensitive", "referenced_tweets", "reply_settings", "source", "text", "withheld"]
    tweets = tw_client.search_recent_tweets(query="from:suhemparack", end_time=None, max_results=10, tweet_fields=fields)
    print(tweets[0])
    # for tweet in tweets.data:
    #     st.write(tweet.id)
    #     st.write(tweet.text)
    #     st.write(tweet.created_at)
    #     if tweet.geo != None:
    #         st.write(tweet.geo)

    # tweepy.Paginator(tw_client.search_recent_tweets, query="Bundesregierung", tweet_fields=['context_annotations', 'created_at'], max_results=100).flatten(limit=1000)

    # for tweet in tweepy.Paginator(tw_client.search_recent_tweets, query="Bundesregierung", tweet_fields=['context_annotations', 'created_at'], max_results=100).flatten(limit=1000):
    #     st.write(tweet.id)
    #     st.write(tweet.text)