####################################################################################
# Initialization
# by JW
#
# A helper script to initialize the DB and other things at first boot of the
# container cluster.
# 
# helpers / first_init.py
####################################################################################

# IMPORT STATEMENTS ----------------------------------------------------------------
import streamlit as st

# Own functions
from helpers.session_states import *
from helpers.db_functions import *
from helpers.twitter_api import *

def init_application():
    try:
        # Session State Initializations ----------------------------------------------------
        session_init()

        # Postgres DB Connection and Initialization ----------------------------------------
        tie_init(st.session_state.postgres_cred, st.session_state.schema_name)

        # Connect the Twitter API ----------------------------------------------------------
        connect_twitter_api()

        # Initialization done --------------------------------------------------------------
        st.session_state.app_init = True

    except Exception as e:
        st.warning("There was a problem initializing the app:", icon="⚠️")
        st.write(e)