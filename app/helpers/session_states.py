####################################################################################
# Session States
# by JW
#
# A helper script to initialize all session states for streamlit
# 
# helpers / session_states.py
####################################################################################

# IMPORT STATEMENTS ----------------------------------------------------------------
import streamlit as st


# Session State Initializations -----------------------------------------------
def session_init():
    # Overall States
    if "app_init" not in st.session_state:
        st.session_state["app_init"] = False

    # Postgres DB Connection State
    if "postgres_cred" not in st.session_state:
        st.session_state["postgres_cred"] = {
            "name":"TN_DB",
            "host":"localhost",
            "port":"5433",
            "db_name":"tie_crawler",
            "db_user":"tie",
            "db_password":"iPkt9FsmoQ7*xdGr"
        }
    if "schema_name" not in st.session_state:
        st.session_state["schema_name"] = "tie"
    
    if "db_engine" not in st.session_state:
        st.session_state["db_engine"] = False
    if "db_connection" not in st.session_state:
        st.session_state["db_connection"] = ""
    if "db_session" not in st.session_state:
        st.session_state["db_session"] = ""
    if "db_meta" not in st.session_state:
        st.session_state["db_meta"] = ""
    if "db_connection_status" not in st.session_state:
        st.session_state["db_connection_status"] = False

    if "db_table_projects" not in st.session_state:
        st.session_state["db_table_projects"] = ""
    if "db_table_twitter_crawls" not in st.session_state:
        st.session_state["db_table_twitter_crawls"] = ""

    # Creation of Projects
    if "project_submit" not in st.session_state:
        st.session_state["project_submit"] = False

    # Twitter
    if "twitter_client" not in st.session_state:
        st.session_state["twitter_client"] = ""
    if "twitter_client_v2" not in st.session_state:
        st.session_state["twitter_client_v2"] = ""
    if "twitter_tweet_fields" not in st.session_state:
        st.session_state["twitter_tweet_fields"] = [
            "attachments",
            "author_id",
            "context_annotations",
            "conversation_id",
            "created_at",
            "edit_controls",
            "entities",
            "geo",
            "id",
            "in_reply_to_user_id",
            "lang", "public_metrics",
            "possibly_sensitive",
            "referenced_tweets",
            "reply_settings",
            "source",
            "text",
            "withheld"
        ]

    ## Twitter Queries
    if "tw_query_exists" not in st.session_state:
        st.session_state["tw_query_exists"] = False
    if "tw_basic_query" not in st.session_state:
        st.session_state["tw_basic_query"] = {
            "query":"",
            "limit":100,
        }
    if "tw_adv_query" not in st.session_state:
        st.session_state["tw_adv_query"] = {
            "query":"",
            "limit":100,
            "min_replies":0,
            "min_retweets":0,
            "min_faves":0,
            "days_ago":"",
            "exclude_replies":False,
            "exclude_retweets":False
        }
    if "tw_raw_query" not in st.session_state:
        st.session_state["tw_raw_query"] = {
            "query":"",
            "limit":1000
        }

    ## Twitter API Credentials
    if "tw_env_cred" not in st.session_state:
        if st.secrets.TWITTER_API_KEY == "":
            st.session_state["tw_env_cred"] = False
        else:
            st.session_state["tw_env_cred"] = True

    if "tw_api_cred" not in st.session_state:
        st.session_state["tw_api_cred"] = {
            "tw_api_key":"",
            "tw_api_secret":"",
            "tw_acc_token":"",
            "tw_acc_token_secret":"",
            "tw_bearer_token":"",
        }

    # OpenCorporates API Credentials
    if "oc_env_cred" not in st.session_state:
        if st.secrets.OPENCORPORATES_API_KEY == "":
            st.session_state["oc_env_cred"] = False
        else:
            st.session_state["oc_env_cred"] = True

    if "oc_api_token" not in st.session_state:
        st.session_state["oc_api_token"] = ""


    # if "tw_api_key" not in st.session_state:
    #     st.session_state["tw_api_key"] = ""
    # if "tw_api_secret" not in st.session_state:
    #     st.session_state["tw_api_secret"] = ""
    # if "tw_acc_token" not in st.session_state:
    #     st.session_state["tw_acc_token"] = ""
    # if "tw_acc_token_secret" not in st.session_state:
    #     st.session_state["tw_acc_token_secret"] = ""
    # if "tw_bearer_token" not in st.session_state:
    #     st.session_state["tw_bearer_token"] = ""

    if "temp_tweets" not in st.session_state:
        st.session_state["temp_tweets"] = ""
    if "tw_pagination_page" not in st.session_state:
        st.session_state["tw_pagination_page"] = 0

    # OpenALEX API Credentials
    # Scopus API Credentials
    # arXiv API Credentials (currently not needed)

    # Some other Session States
    if "crawl_status" not in st.session_state:
        st.session_state["crawl_status"] = False
    if "tw_bearer_token" not in st.session_state:
        st.session_state["tw_bearer_token"] = ""