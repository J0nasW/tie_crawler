####################################################################################
# Project Overview
# by JW
#
# Just a page to get an overview over all projects in the database
# 
# pages / Project Overview.py
####################################################################################

# IMPORT STATEMENTS ----------------------------------------------------------------

import pandas as pd
import streamlit as st

# Own Functions
from helpers.db_functions import *

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="Project Overview", page_icon="🔎")

st.title("🔎 Project Overview")

st.write("A simple page for your projects.")

st.dataframe(pd.DataFrame(list_projects()))