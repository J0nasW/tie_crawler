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
# import os

# Streamlit Web App
import streamlit as st

# Simple Sentiment Analysis
import re
import numpy as np
from textblob import TextBlob
import matplotlib.pyplot as plt

# Own Functions
from helpers.db_functions import *
from helpers.twitter_api import *

from preprocessors.roberta import *

### STREAMLIT Init:

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="Twitter API", page_icon="🐦")

# Start of the page

st.title("🐦 Twitter API")

st.write("Here you find some useful Tools and Functions to work with the Twitter API")

# SIDEBAR --------------------------------------------
# with st.sidebar:

# Some helper variables
query_exists = st.session_state.tw_query_exists

submit_basic = False
submit_advanced = False
submit_query = False

delete_tw_query = False

search_params_basic = {}
search_params_adv = {}
search_params_query = {}

with st.expander("#1: Build Twitter Search Query", expanded=not query_exists):

    if query_exists:
        st.info("We found an existing query. You can either delete the existing query or continue with the existing one.", icon="ℹ️")
        st.write(st.session_state.tw_basic_query)
        delete_tw_query = st.button(label="Delete", disabled=False)

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
                search_params_query["limit"] = st.number_input("Tweet limit", 1, 10000, 1000)
                st.markdown("See [Twitter API Examples](https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query#examples).")

                submit_query = st.form_submit_button(label="Submit")

if submit_basic:
    with st.spinner('Wait while we collect the tweets...'):
        try:
            #tweets = get_tweets(search_params_basic)
            twitter_client_v2 = st.session_state.twitter_client_v2
            tweets = twitter_client_v2.search_recent_tweets(query=search_params_basic["query"] +  " -RT", end_time=None, max_results=search_params_basic["limit"], tweet_fields=st.session_state.twitter_tweet_fields, expansions="author_id")
            # for tweet in tweets.data:
            #     st.write(tweet)
            st.session_state.temp_tweets = tweets
            st.session_state.tw_basic_query = search_params_basic
            st.session_state.tw_query_exists = True

            st.success('Done!')
            st.experimental_rerun()


        except Exception as e:
            st.error("There was an unexpected error while collecting the tweets. Please try again and double check your API credentials.")
            st.write(e)

if submit_advanced:
    with st.spinner('Wait while we collect the tweets...'):
        try:
            #tweets = get_tweets(search_params_basic)
            twitter_client_v2 = st.session_state.twitter_client_v2
            tweets = twitter_client_v2.search_recent_tweets(query=search_params_adv["query"], end_time=None, max_results=search_params_adv["limit"], tweet_fields=st.session_state.twitter_tweet_fields, expansions="author_id")
            # for tweet in tweets.data:
            #     st.write(tweet)
            st.session_state.temp_tweets = tweets
            st.session_state.tw_adv_query = search_params_adv
            st.session_state.tw_query_exists = True

            st.success('Done!')
            st.experimental_rerun()

        except Exception as e:
            st.error("There was an unexpected error while collecting the tweets. Please try again and double check your API credentials.")
            st.write(e)

if submit_query:
    with st.spinner('Wait while we collect the tweets...'):
        try:
            #tweets = get_tweets(search_params_basic)
            twitter_client_v2 = st.session_state.twitter_client_v2
            tweets = twitter_client_v2.search_recent_tweets(query=search_params_adv["query"], end_time=None, max_results=search_params_query["limit"], tweet_fields=st.session_state.twitter_tweet_fields, expansions="author_id")
            # for tweet in tweets.data:
            #     st.write(tweet)
            st.session_state.temp_tweets = tweets
            st.session_state.tw_raw_query = search_params_query
            st.session_state.tw_query_exists = True

            st.success('Done!')
            st.experimental_rerun()

        except Exception as e:
            st.error("There was an unexpected error while collecting the tweets. Please try again and double check your API credentials.")
            st.write(e)


if delete_tw_query:
    st.session_state.tw_query_exists = False
    st.session_state.tw_basic_query = {}
    delete_tw_query = False
    st.experimental_rerun()

if query_exists:
    with st.expander("#2: Browse crawled tweets", expanded=False):
        st.write("Here you can browse the tweets you crawled before.")
        temp_tweets_data = st.session_state.temp_tweets.data
        temp_tweets_includes = (st.session_state.temp_tweets).includes
        #st.write(temp_tweets_data)
        users = {u["id"]: u for u in temp_tweets_includes['users']}    
        # for tweet in temp_tweets.data:
        #     if users[tweet.author_id]:
        #         user = users[tweet.author_id]
        #         st.write(user)
        #         st.write(user.profile_image_url)


        for result in paginator(temp_tweets_data, 10, "tweet_next", "tweet_prev"):
            display_tweet(result, users)
            "---"

    with st.expander("#3: Simple Sentiment Analysis", expanded=query_exists):
        st.write("Here you can do a simple sentiment analysis on the crawled tweets.")
        def clean_tweets(tweets):
            '''
            Utility function to clean tweet text by removing links, special characters
            using simple regex statements.
            '''
            preprocess_roberta(tweets)
            return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweets).split())

        def get_tweets_sentiment(tweets):
            '''
            Utility function to classify sentiment of passed tweet
            using textblob's sentiment method
            '''
            # create TextBlob object of passed tweet text
            analysis = TextBlob(clean_tweets(tweets))
            # set sentiment
            if analysis.sentiment.polarity > 0:
                return 'positive'
            elif analysis.sentiment.polarity == 0:
                return 'neutral'
            else:
                return 'negative'

        tweets = st.session_state.temp_tweets.data

        cleaned_tweets = []

        for i in range(len(tweets)):
            cleaned_tweets.append(tweets[i].text)

        #cleaned_tweets

        tweet_texts = []

        for i in range(len(cleaned_tweets)):
            tweet_texts.append(cleaned_tweets[i])

        #tweet_texts

        sentiment = []

        for i in range(len(tweet_texts)):
            sentiment.append(get_tweets_sentiment(tweet_texts[i]))

        #sentiment

        # picking positive tweets from tweets
        ptweets = [tweet for tweet in sentiment if tweet == 'positive']
        ntweets = [tweet for tweet in sentiment if tweet == 'negative']


        pos, neg, neutral = st.columns(3)

        with pos:
            st.metric(label="Positive Sentiment", value=str(np.round(100*len(ptweets)/len(tweets), decimals=2)) + " %")
        with neg:
            st.metric(label="Neutral Sentiment", value=str(np.round(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets), decimals=2)) + " %")
        with neutral:
            st.metric(label="Negative Sentiment", value=str(np.round(100*len(ntweets)/len(tweets), decimals=2)) + " %")
        
        col1, col2, col3 = st.columns(3)

        with col1:
            # Pie chart, where the slices will be ordered and plotted counter-clockwise:
            labels = 'Positive', 'Neutral', 'Negative'
            sizes = [(100*len(ptweets)/len(tweets)), (100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets)), (100*len(ntweets)/len(tweets))]

            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                    shadow=True, startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            st.pyplot(fig1)