import pandas as pd

from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch

import streamlit as st

### STREAMLIT Init:

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="Scopus API", page_icon="📄")

Scopus_API_key = st.secrets["SCOPUS_API_KEY"]

def get_results_elsapy(api_query, api_count):
    client = ElsClient(Scopus_API_key)

    # Search for documents containing "machine learning"
    s = ElsSearch(api_query,'scopus')
    s.execute(client, get_all = False, count=api_count)
    # nr_s = len(s.results) 
    return s

# Start of the page

st.title("📄 Scopus API")

st.write("The gateway to the Scopus API.")
st.markdown("The Scopus API is a RESTful API that allows you to search for and retrieve information from the Scopus database. You can find more Information here: [Scopus Search API](https://dev.elsevier.com/sc_api.html).")

with st.form(key='my_form'):
    api_query = st.text_area("Scopus API Query", height=100)
    limit = st.number_input("Limit", min_value=1, max_value=5000, value=20)
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    st.write("API Query:", api_query)

    s = get_results_elsapy(api_query, limit)
    
    st.write("Found " + str(len(s.results)) + " Results:")
    st.write(s.results)
        