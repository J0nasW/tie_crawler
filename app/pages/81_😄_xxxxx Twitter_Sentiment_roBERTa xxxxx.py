####################################################################################
# Twitter Sentiment Analyzer
# by JW
#
# A simple python tool to analyze twitter sentiments
# 
# pages / Twitter_Sentiment.py
####################################################################################

# IMPORT STATEMENTS ----------------------------------------------------------------

import pandas as pd
import numpy as np
from datetime import datetime as dt
from math import floor
# import os

from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
from scipy.special import softmax

# Streamlit Web App
import streamlit as st

# Own Functions
from helpers.db_functions import *
from helpers.twitter_api import *
from preprocessors.roberta import *

### STREAMLIT Init:

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="Twitter Analyzer", page_icon="🐦")

# Start of the page

st.title("😄 Twitter Sentiment Analyzer with roBERTa")

st.write("The gateway to analyze tweets with roBERTa Sentiment analyzer")

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

    if st.button("Analyze"):

        MODEL = f"cardiffnlp/twitter-xlm-roberta-base-sentiment"

        tokenizer = AutoTokenizer.from_pretrained(MODEL)
        config = AutoConfig.from_pretrained(MODEL)

        # PT
        model = AutoModelForSequenceClassification.from_pretrained(MODEL)
        model.save_pretrained(MODEL)

        text = "Good night 😊"
        text = preprocess_roberta(text)
        encoded_input = tokenizer(text, return_tensors='pt')
        output = model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        # # TF
        # model = TFAutoModelForSequenceClassification.from_pretrained(MODEL)
        # model.save_pretrained(MODEL)

        # text = "Good night 😊"
        # encoded_input = tokenizer(text, return_tensors='tf')
        # output = model(encoded_input)
        # scores = output[0][0].numpy()
        # scores = softmax(scores)

        # Print labels and scores
        ranking = np.argsort(scores)
        ranking = ranking[::-1]
        for i in range(scores.shape[0]):
            l = config.id2label[ranking[i]]
            s = scores[ranking[i]]
            st.write(f"{i+1}) {l} {np.round(float(s), 4)}")




        # temp_tweets_data = (st.session_state.temp_tweets).data
        # temp_tweets_includes = (st.session_state.temp_tweets).includes
        # users = {u["id"]: u for u in temp_tweets_includes['users']}    
        # # for tweet in temp_tweets.data:
        # #     if users[tweet.author_id]:
        # #         user = users[tweet.author_id]
        # #         st.write(user)
        # #         st.write(user.profile_image_url)


        # for result in paginator(temp_tweets_data, 10, "tweet_next", "tweet_prev"):
        #     display_tweet(result, users)
        #     "---"