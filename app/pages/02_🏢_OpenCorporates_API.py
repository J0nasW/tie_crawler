import requests
import json
import os
import pandas as pd
import datetime

import streamlit as st

### STREAMLIT Init:

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="OpenCorporates API", page_icon="🏢")

# Start of the page

st.title("🏢 OpenCorporates API")

st.write("The gateway to the OpenCorporates API")

def corporation_search(corporation, jurisdiction, incorporation_date, created_at_date):
    st.spinner("Calling API...")

    url = "https://api.opencorporates.com/companies/search"
    data_params = {
        "q": str(corporation),
        "jurisdiction_code": str(jurisdiction),
        #"current_status": str(current_status),
        "inactive": "false",
        "incorporation_date=": str(incorporation_date),
        "created_at=": str(created_at_date),
        "normalise_company_name": "true",
        "sparse": "true",
        "api_token": str(st.secrets.OPENCORPORATES_API_KEY)
    }
    response = requests.request("GET", url, params=data_params)

    if response.status_code == 200:
        st.success("API call successful")
        return response.json()

    else:
        st.error("API call failed")
        return response.status_code

def company_id_search(id, jurisdiction):
    st.spinner("Calling API...")

    url = "https://api.opencorporates.com/companies/" + str(jurisdiction) + "/" + str(id) + "?api_token=" + str(st.secrets.OPENCORPORATES_API_KEY)
    response = requests.request("GET", url)

    # url = "https://api.opencorporates.com/companies"
    # data_params = {
    #     "jurisdiction_code": str(jurisdiction),
    #     "company_number": str(id),
    #     "api_token": str(st.secrets.OPENCORPORATES_API_KEY)
    # }
    # response = requests.request("GET", url, params=data_params)

    if response.status_code == 200:
        st.success("API call successful")
        return response.json()

    else:
        st.error("API call failed")
        return response.status_code


tab1, tab2 = st.tabs(["Company Search", "ID Search"])

with tab1:
    st.header("Search for a specific company")

    corporation = st.text_input("Corporation name", placeholder="Porsche")
    corporation.replace(" ", "+")
    jurisdiction = st.text_input("Jurisdiction", placeholder="de")
    #current_status = st.selectbox("Current status", ["all", "active", "inactive", "dissolved"])
    incorporation_date = st.date_input("Incorporation date", value=None, min_value=None, max_value=None, key=None, help=None)
    incorporation_date = str(incorporation_date) + ":" + datetime.datetime.now().strftime("%Y-%m-%d")
    created_at_date = st.date_input("Created at date", value=None, min_value=None, max_value=None, key=None, help=None)
    created_at_date = str(created_at_date) + ":" + datetime.datetime.now().strftime("%Y-%m-%d")

    if st.button("Search", key="company_search"):
        st.write("Searching for " + str(corporation) + " in " + str(jurisdiction) + " with incorporation date " + incorporation_date)
        result = corporation_search(corporation, jurisdiction, incorporation_date, created_at_date)

        st.write(result)

        companies = result["results"]["companies"]

        df_result = pd.DataFrame(companies).apply(pd.Series)


        st.write(df_result)




with tab2:
    st.header("Search for a specific company ID")

    company_id = st.text_input("Company ID", placeholder="17087985")
    jurisdiction_id = st.text_input("Jurisdiction of Company", placeholder="nl")

    if st.button("Search", key="company_id_search"):
        st.write("Searching for " + str(company_id) + " in " + str(jurisdiction_id))
        st.write("API key: " + str(st.secrets.OPENCORPORATES_API_KEY))
        result = company_id_search(company_id, jurisdiction_id)

        st.write(result)