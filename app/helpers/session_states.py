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

    ## Twitter API Credentials
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