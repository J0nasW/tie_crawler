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
import pandas as pd

# Session State Initializations -----------------------------------------------
def session_init(secrets_exist):
    # Overall States
    if "app_init" not in st.session_state:
        st.session_state["app_init"] = False

    # Secret Exists State
    if "secret_exists" not in st.session_state:
        if secrets_exist:
            st.session_state["secret_exists"] = True
        else:
            st.session_state["secret_exists"] = False

    # Postgres DB Connection State
    if "postgres_cred" not in st.session_state:
        st.session_state["postgres_cred"] = {
            "name":"TN_DB",
            "host":"localhost",
            "port":"15433",
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
        if secrets_exist:
            st.session_state["tw_env_cred"] = True
        else:
            st.session_state["tw_env_cred"] = False

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
        if secrets_exist:
            st.session_state["oc_env_cred"] = True
        else:
            st.session_state["oc_env_cred"] = False

    if "oc_api_token" not in st.session_state:
        st.session_state["oc_api_token"] = ""

    # Text Extraction
    if "text_extracted" not in st.session_state:
        st.session_state["text_extracted"] = False

    if "url_text" not in st.session_state:
        st.session_state["url_text"] = []

    if "cleaned_raw_text" not in st.session_state:
        st.session_state["cleaned_raw_text"] = ""

    if "uploaded_files_infos" not in st.session_state:
        st.session_state["uploaded_files_infos"] = []

    if "url_infos" not in st.session_state:
        st.session_state["url_infos"] = []

    # Geocode AI Radar
    if "geocode_df" not in st.session_state:
        st.session_state["geocode_df"] = ""


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
    if "arxiv_results" not in st.session_state:
        st.session_state["arxiv_results"] = ""
    if "arxiv_pdf_results" not in st.session_state:
        st.session_state["arxiv_pdf_results"] = pd.DataFrame()
    if "arxiv_pdf_dict" not in st.session_state:
        st.session_state["arxiv_pdf_dict"] = {}
    if "arxiv_pdf_corpus" not in st.session_state:
        st.session_state["arxiv_pdf_corpus"] = ""

    if "lda_num_topics" not in st.session_state:
        st.session_state["lda_num_topics"] = 10
    if "lda_num_iterations" not in st.session_state:
        st.session_state["lda_num_iterations"] = 10
    if "lda_num_workers" not in st.session_state:
        st.session_state["lda_num_workers"] = 4
    if "lda_num_passes" not in st.session_state:
        st.session_state["lda_num_passes"] = 10

    if "arxiv_lda_model" not in st.session_state:
        st.session_state["arxiv_lda_model"] = ""
    if "arxiv_lda_finished" not in st.session_state:
        st.session_state["arxiv_lda_finished"] = False

    if "arxiv_similarity_matrix" not in st.session_state:
        st.session_state["arxiv_similarity_matrix"] = ""

    # Some other Session States
    if "crawl_status" not in st.session_state:
        st.session_state["crawl_status"] = False
    if "tw_bearer_token" not in st.session_state:
        st.session_state["tw_bearer_token"] = ""