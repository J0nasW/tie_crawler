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
# ToDo: Streamlit Auth (https://blog.streamlit.io/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/)
# import streamlit_authenticator as stauth

# INITIALIZATION OF THE APPLICATION -------------------------------------------------

### STREAMLIT Init:

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="centered", page_title="TIE Trend Navigator", page_icon=":bar-chart:")

# Some Session State Initializations -------

# Own Twitter API Credentials
if "env_cred" not in st.session_state:
    st.session_state["env_cred"] = True
if "tw_api_key" not in st.session_state:
    st.session_state["tw_api_key"] = ""
if "tw_api_secret" not in st.session_state:
    st.session_state["tw_api_secret"] = ""
if "tw_acc_token" not in st.session_state:
    st.session_state["tw_acc_token"] = ""
if "tw_acc_token_secret" not in st.session_state:
    st.session_state["tw_acc_token_secret"] = ""
if "tw_bearer_token" not in st.session_state:
    st.session_state["tw_bearer_token"] = ""

if "crawl_status" not in st.session_state:
    st.session_state["crawl_status"] = False
if "crawled_tweets" not in st.session_state:
    st.session_state["crawled_tweets"] = ""


# START OF THE APPLICATION -------------------------------------------------------------------

logo, title = st.columns([1, 5])

with logo:
    st.image("assets/logo.png")
with title:
    st.title("TIE Trend Navigator")

st.write("Welcome to the TIE Trend Navigator. With this app, you can easily discover trends and crawl useful data from a lot of different data-sources.")
st.caption("In order to work, the Trend Navigator uses API access from most of its sources. Please head over to the settings page to provide suitable API credentials or store them as secrets in a secrets.toml file (or online)")

st.caption("If you did not specify your Twitter API Credentials in the environment variables, feel free to open up the sidebar and provide these credentials for this session.")

st.write("")
st.write("")
# st.image("assets/tw_sentiment_banner.jpg", use_column_width="auto")




# -------------------------------------------------------------

with st.form(key="search_inputs"):

    @st.cache

    class UncacheableList(list):
        pass

    cache_args = dict(
        show_spinner=False,
        allow_output_mutation=True,
        suppress_st_warning=True,
        hash_funcs={
            "streamlit.session_state.SessionState": lambda x: None,
            pd.DataFrame: lambda x: None,
            UncacheableList: lambda x: None,
        },
    )

    if "tweets" not in st.session_state:
        # These are all for debugging.
        st.session_state.tweets = []
        st.session_state.curr_tweet_page = 0
        st.session_state.curr_raw_tweet_page = 0


    # TWITTER FUNCTIONS --------------------------------------

    # Twitter API Auth
    
    if st.session_state.env_cred == True:
        auth = tweepy.OAuth2AppHandler(st.secrets.TWITTER_API_KEY, st.secrets.TWITTER_API_SECRET)
    else:
        auth = tweepy.OAuth2AppHandler(st.session_state.tw_api_key, st.session_state.tw_api_secret)
    #twitter_client = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
    twitter_client = tweepy.API(auth)

    def get_tweet_url(tweet):
        return f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id_str}"

    @st.cache(ttl=60 * 60, **cache_args)
    def get_tweets(query,
        days_ago,
        limit,
        exclude_replies,
        exclude_retweets,
        min_replies,
        min_retweets,
        min_faves):

        start_date = str(rel_to_abs_date(days_ago))

        query_list = [
                query,
                " -RT" if exclude_retweets else "",
                f"since:{start_date}",
                "-filter:replies" if exclude_replies else "",
                "-filter:nativeretweets" if exclude_retweets else "",
                f"min_replies:{min_replies}",
                f"min_retweets:{min_retweets}",
                f"min_faves:{min_faves}",
            ]

        query_str = " ".join(query_list)

        tweets = UncacheableList(
                tweepy.Cursor(
                    twitter_client.search_tweets,
                    q=query_str,
                    lang="en",
                    count=limit,
                    include_entities=False,
                ).items(limit)
            )

        return tweets

    # SOME UTILITIES ---------------------------------------------

    def rel_to_abs_date(days):
        if days == None:
            return (datetime.date(day=1, month=1, year=1970),)
        return datetime.date.today() - datetime.timedelta(days=days)

    def paginator(values, state_key, page_size, btn_key_next, btn_key_prev):
        curr_page = getattr(st.session_state, state_key)

        a, b, c = st.columns(3)

        def decrement_page():
            curr_page = getattr(st.session_state, state_key)
            if curr_page > 0:
                setattr(st.session_state, state_key, curr_page - 1)

        def increment_page():
            curr_page = getattr(st.session_state, state_key)
            if curr_page + 1 < len(values) // page_size:
                setattr(st.session_state, state_key, curr_page + 1)

        def set_page(new_value):
            setattr(st.session_state, state_key, new_value - 1)

        a.write(" ")
        a.write(" ")
        a.button("Previous page", on_click=decrement_page, key=btn_key_next)

        b.write(" ")
        b.write(" ")
        b.button("Next page", on_click=increment_page, key=btn_key_prev)

        c.selectbox(
            "Select a page",
            range(1, len(values) // page_size + 1),
            curr_page,
            on_change=set_page,
        )

        curr_page = getattr(st.session_state, state_key)

        page_start = curr_page * page_size
        page_end = page_start + page_size

        return values[page_start:page_end]

    def display_dict(dict):
        for k, v in dict.items():
            a, b = st.columns([1, 4])
            a.write(f"**{k}:**")
            b.write(v)

    def display_tweet(tweet):
        parsed_tweet = {
            "author": tweet.user.screen_name,
            "created_at": tweet.created_at,
            "url": get_tweet_url(tweet),
            "text": tweet.text,
        }
        display_dict(parsed_tweet)

    # --------------------------------------------------------------

    search_params = {}

    relative_dates = {
        "1 day ago": 1,
        "1 week ago": 7,
        "2 weeks ago": 14,
        "1 month ago": 30,
    }

    a, b = st.columns([1, 1])
    search_params["query"] = a.text_input("Query", placeholder="Spaghetti")
    search_params["limit"] = b.slider("Tweet limit", 1, 1024, 50)

    a, b, c, d = st.columns([1, 1, 1, 1])
    search_params["min_replies"] = a.number_input("Minimum replies", 0, None, 0)
    search_params["min_retweets"] = b.number_input("Minimum retweets", 0, None, 0)
    search_params["min_faves"] = c.number_input("Minimum hearts", 0, None, 0)
    selected_rel_date = d.selectbox("Search from date", list(relative_dates.keys()), 3)
    search_params["days_ago"] = relative_dates[selected_rel_date]

    a, b, c  = st.columns([1, 2, 1])
    search_params["exclude_replies"] = a.checkbox("Exclude replies", False)
    search_params["exclude_retweets"] = b.checkbox("Exclude retweets", False)

    submit_button = st.form_submit_button(label="Submit")

if submit_button:
    with st.spinner('Wait while we collect the tweets...'):
        try:
            tweets = get_tweets(**search_params)
            st.session_state.crawl_status = True
            st.session_state.crawled_tweets = tweets
            st.success('Done!')
        except Exception as e:
            st.error("There was an unexpected error while collecting the tweets. Please try again and double check your API credentials.")
            st.write(e)

if st.session_state.crawl_status:
    try:
        with st.expander("Show tweets"):
            for result in paginator(st.session_state.crawled_tweets, "curr_tweet_page", 10, "tweet_next", "tweet_prev"):
                display_tweet(result)
                "---"

        with st.expander("Show raw tweets"):
            #st.download_button(label="download_raw_tweets", data=json.dumps(tweets))
            for result in paginator(st.session_state.crawled_tweets, "curr_raw_tweet_page", 1, "raw_tweet_next", "raw_tweet_prev"):
                display_dict(result.__dict__)
                "---"

        with st.expander("Show raw json"):
            st.download_button(label="Download raw tweets JSON",
                data=jsonpickle.encode(st.session_state.crawled_tweets, unpicklable=False),
                mime="application/json", file_name=("Twitter_Query.json")
                )
            st.session_state.crawled_tweets
    except Exception as e:
        st.error("There was an unexpected error while displaying the tweets. Check back later.")
        st.write(e)
        
        


# SIDEBAR --------------------------------------------

with st.sidebar:
    st.header("Own API Credentials")
    st.write("""
    If you didn't specify your Twitter API Credentials in the environment variables, you have the option to specify them for this session:
    """)
    own_cred = st.checkbox('I want to use custom credentials (only for this session)', key="own_cred")
    if own_cred:
        st.session_state.tw_api_key = st.text_input("", placeholder="Twitter API Key",)
        st.session_state.tw_api_secret = st.text_input("", placeholder="Twitter API Secret",)
        st.session_state.tw_acc_token = st.text_input("", placeholder="Twitter Access Token",)
        st.session_state.tw_acc_token_secret = st.text_input("", placeholder="Twitter Access Token Secret",)
        st.session_state.tw_bearer_token = st.text_input("", placeholder="Twitter Bearer Token",)
