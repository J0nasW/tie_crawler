####################################################################################
# Settings Page
# by JW
#
# Manage Settings and Session States
# 
# Home.py / Settings.py
####################################################################################

# IMPORT STATEMENTS ----------------------------------------------------------------
import streamlit as st

# Own Functions
from helpers.db_functions import *


# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="Settings", page_icon="⚙")

project_submit = st.session_state["project_submit"]

st.title("⚙ Settings")
st.markdown("Here you can manage your settings, provide own API keys for a session and inspect session states. If you have provided API credentials in a secret environment (either secrets.toml locally or via deployment), you can overwrite your API credentials here.")

st.markdown("## API Credentials")
st.write("In this section, you can provide API Credentials for several services.")

with st.expander("Twitter API"):
    if st.secrets.TWITTER_API_KEY != "":
        st.info("There are Twitter API Credentials stored as secrets. Providing new credentials will overwrite them in this session.", icon="ℹ️")

    with st.form("twitter_credentials_form"):
        st.markdown("### Twitter API")
        st.markdown("Please provide your Twitter API credentials. You can find them in your [Twitter Developer Account](https://developer.twitter.com/).")

        tw_api_cred = {}

        tw_api_cred["tw_api_key"] = st.text_input("Twitter API Key")
        tw_api_cred["tw_api_secret"] = st.text_input("Twitter API Secret")
        tw_api_cred["tw_acc_token"] = st.text_input("Twitter Access Token")
        tw_api_cred["tw_acc_token_secret"] = st.text_input("Twitter Access Token Secret")
        tw_api_cred["tw_bearer_token"] = st.text_input("Twitter Bearer Token")

        twitter_api_cred_submit = st.form_submit_button(label="Submit")

with st.expander("OpenCorporates API"):
    if st.secrets.OPENCORPORATES_API_KEY != "":
        st.info("There are OpenCorporates API Credentials stored as secrets. Providing new credentials will overwrite them in this session.", icon="ℹ️")

    with st.form("opencorporates_credentials_form"):
        st.markdown("### OpenCorporates API")
        st.markdown("Please provide your OpenCorporates API credentials. You can find them in your [OpenCorporates Account](https://opencorporates.com/users/account).")

        oc_api_token = st.text_input("OpenCorporates API Key")
        oc_api_cred_submit = st.form_submit_button(label="Submit")

if twitter_api_cred_submit:
    st.session_state.tw_api_cred = tw_api_cred
    st.session_state.tw_env_cred = False

if oc_api_cred_submit:
    st.session_state.oc_api_token = oc_api_token
    st.session_state.oc_env_cred = False