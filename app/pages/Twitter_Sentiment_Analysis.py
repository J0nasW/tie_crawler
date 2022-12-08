import streamlit as st
import re
from textblob import TextBlob
import matplotlib.pyplot as plt

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="TIE Twitter Sentiment Analyzer", page_icon=":smile:")

# States
if "sentiment_analysis" not in st.session_state:
    st.session_state["sentiment_analysis"] = False

st.title("Twitter Sentiment Analyzer")

start = ""

if st.session_state.crawl_status:
    st.success("Crawl successful - can access data", icon="✅")
    start = st.button("Perform Sentiment Analysis")
else:
    st.warning("It seems, that you did not execute a Crawl yet - head over to the Homepage to do so.", icon="⚠️")

if start:
    st.write("Lets go!")

    def clean_tweets(tweets):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
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

    tweets = st.session_state.crawled_tweets[:]

    cleaned_tweets = []

    for i in range(len(tweets)):
        cleaned_tweets.append(tweets[i]._json)

    #cleaned_tweets

    tweet_texts = []

    for i in range(len(cleaned_tweets)):
        tweet_texts.append(cleaned_tweets[i]["text"])

    #tweet_texts

    sentiment = []

    for i in range(len(tweet_texts)):
        sentiment.append(get_tweets_sentiment(tweet_texts[i]))

    #sentiment

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in sentiment if tweet == 'positive']
    # percentage of positive tweets
    st.write("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in sentiment if tweet == 'negative']
    # percentage of negative tweets
    st.write("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    # percentage of neutral tweets
    st.write("Neutral tweets percentage: {} % \
        ".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets)))

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

        