####################################################################################
# Twitter API
# by JW
#
# A helper script to connect to the official Twitter API using Tweepy and other
# helpful scripts.
# 
# helpers / twitter_api.py
####################################################################################

# Twitter crawling
import tweepy

# Streamlit Web App
import streamlit as st

# Own functions
from helpers.helper_functions import *

# START OF THE SCRIPT ---------------------------------------------------------------

def connect_twitter_api():
    try:
        # Using Tweepy's v1 API
        if st.session_state.env_cred == True:
            # Using API Credentials from secrets.toml
            auth = tweepy.OAuth2AppHandler(st.secrets.TWITTER_API_KEY, st.secrets.TWITTER_API_SECRET)
        else:
            # Using API Credentials defined in the session state
            auth = tweepy.OAuth2AppHandler(st.session_state.tw_api_key, st.session_state.tw_api_secret)
        #twitter_client = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

        st.session_state.twitter_client = tweepy.API(auth)
    except Exception as e:
        st.error("There was a problem connecting to the Twitter API.")
        st.write(e)


def get_tweets(search_params):

    try:
        if st.session_state.twitter_client != "":
            twitter_client = st.session_state.twitter_client
        else:
            st.error("You are not connected to the Twitter API. Check your credentials.")

        start_date = str(rel_to_abs_date(search_params["days_ago"]))
        min_replies = search_params["min_replies"]
        min_retweets = search_params["min_retweets"]
        min_faves = search_params["min_faves"]

        query_list = [
                search_params["query"],
                " -RT" if search_params["exclude_retweets"] else "",
                f"since:{start_date}",
                "-filter:replies" if search_params["exclude_replies"] else "",
                "-filter:nativeretweets" if search_params["exclude_retweets"] else "",
                f"min_replies:{min_replies}",
                f"min_retweets:{min_retweets}",
                f"min_faves:{min_faves}",
            ]

        query_str = " ".join(query_list)

        tweets = tweepy.Cursor(
                    twitter_client.search_tweets,
                    q=query_str,
                    lang="en",
                    count=search_params["limit"],
                    include_entities=False,
                ).items(search_params["limit"])

    except Exception as e:
        st.error("There was a problem collecting the tweets!")
        st.write(e)

    return tweets

def get_tweet_url(tweet):
        return f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id_str}"

def display_tweet(tweet):
    parsed_tweet = {
        "author": tweet.user.screen_name,
        "created_at": tweet.created_at,
        "url": get_tweet_url(tweet),
        "text": tweet.text,
    }
    display_dict(parsed_tweet)