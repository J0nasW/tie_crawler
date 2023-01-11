import requests
import json
import os
import pandas as pd
import datetime
import urllib

import streamlit as st

### STREAMLIT Init:

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="OpenAlex API", page_icon="📄")

# Start of the page

st.title("📄 OpenAlex API")

st.write("The gateway to the OpenAlex API. OpenAlex can handle multiple IDs like DOI, ISSN, ORCID, ...")

st.info("If you want faster and more reliable API Calls, provide an E-Mail to use the Polite API.")
polite_email = st.text_input("Polite E-Mail", placeholder="mail@example.com")

def single_entity_search(oalex_id, polite_email):
    st.spinner("Calling API...")

    # url = "https://api.openalex.org/"
    # data_params = {
    #     "works": str(oalex_id),
    #     "mailto": str(polite_email)
    # }
    # response = requests.request("GET", url, params=data_params)

    if polite_email:
        url = "https://api.openalex.org/" + str(oalex_id) +  "&per-page=100?mailto=" + str(polite_email)
    else:
        url = "https://api.openalex.org/" + str(oalex_id) + "&per-page=100"
    url.replace(" ", "%20")
    st.write(url)
    response = requests.request("GET", url)

    if response.status_code == 200:
        st.success("API call successful")
        return response.json()

    else:
        if response.status_code == 429:
            st.error("429: API call failed: Too many requests")
        if response.status_code == 500:
            st.error("500: API call failed: Internal Server Error")
        if response.status_code == 503:
            st.error("503: API call failed: Service Unavailable")
        if response.status_code == 404:
            st.error("404: API call failed: Entry not found")
        else:
            st.error("API call failed, unknown error")
            return response.status_code

def multiple_entry_search(search_params_work, polite_email):
    st.spinner("Calling API...")

    # url = "https://api.openalex.org/"
    # data_params = {
    #     "works": str(oalex_id),
    #     "mailto": str(polite_email)
    # }
    # response = requests.request("GET", url, params=data_params)

    filter_string = ""

    for key, value in search_params_work.items():
        if search_params_work[key]:
            filter_string = filter_string + ":".join([key, str(value).replace(" ", "%20")]) + ","

    filter_string = filter_string[:-1]

    if polite_email:
        url = "https://api.openalex.org/works?filter=" + str(filter_string) + "&per-page=100?mailto=" + str(polite_email)
    else: url = "https://api.openalex.org/works?filter=" + str(filter_string) + "&per-page=100"

    st.write(url)
    response = requests.request("GET", url)

    if response.status_code == 200:
        return response.json()

    else:
        if response.status_code == 429:
            st.error("429: API call failed: Too many requests")
        if response.status_code == 500:
            st.error("500: API call failed: Internal Server Error")
        if response.status_code == 503:
            st.error("503: API call failed: Service Unavailable")
        if response.status_code == 404:
            st.error("404: API call failed: Entry not found")
        else:
            st.error("API call failed, unknown error")
            st.write(response.status_code)

submit_basic = False

tab1, tab2 = st.tabs(["Search for a specific Entry", "Search for multiple Entries"])

with tab1:
    st.header("Search for a specific entity using IDs like DOI, ISSN, ORCID, ...")

    col1, col2 = st.columns([1, 4])

    with col1:
        id_choice = st.selectbox("Type", ("Works (DOI)", "Authors (ORCID)", "Venues (ISSN)", "Institutions (ROR ID)", "OpenAlex ID"))

    with col2:
        if id_choice == "Works (DOI)":
            oalex_id = st.text_input("DOI", placeholder="10.7717/peerj.4375")
            if oalex_id != "": oalex_id = "works/https://doi.org/" + oalex_id

        if id_choice == "Authors (ORCID)":
            oalex_id = st.text_input("ORCID", placeholder="0000-0001-5109-3700")
            if oalex_id != "": oalex_id = "authors/orcid:" + oalex_id

        if id_choice == "Venues (ISSN)":
            oalex_id = st.text_input("ISSN", placeholder="2041-1723")
            if oalex_id != "": oalex_id = "venues/issn:" + oalex_id

        if id_choice == "Institutions (ROR ID)":
            oalex_id = st.text_input("ROR ID", placeholder="03yrm5c26")
            if oalex_id != "": oalex_id = "institutions/ror:" + oalex_id

        if id_choice == "OpenAlex ID":
            oalex_id = st.text_input("OpenAlex ID", placeholder="W17087985")
            if oalex_id != "": oalex_id = "works/" + oalex_id

    if st.button("Search", key="entity_search", disabled=not bool(oalex_id)):
        with st.spinner("Searching for " + str(oalex_id)):
            result = single_entity_search(oalex_id, polite_email)
            if result == None:
                st.error("No results found")
            else:    
                st.write(result)

with tab2:
    st.header("Search for multiple works")
    st.info("You can use logic operators in the form of:     AND : ,   OR : |   NOT : !   ", icon="ℹ️")


    with st.form("basic_work_form"):
        search_params_work = {}

        st.markdown("#### Text Filters")
        search_params_work["title.search"] = st.text_input("Title Search", placeholder="AI, ...")
        search_params_work["abstract.search"] = st.text_input("Abstract Search", placeholder="COVID-19, ...")
        search_params_work["fulltext.search"] = st.text_input("Fulltext Search", placeholder="Green Technologies, ...")

        st.markdown("#### Authors")
        a, b = st.columns(2)
        search_params_work["author.id"] = a.text_input("Author ID (OpenAlex)", placeholder="A17087985, ...")
        search_params_work["author.orcid"] = b.text_input("Author ID (ORCID)", placeholder="0000-0001-5109-3700, ...")

        st.markdown("#### Institutions")
        c, d, e = st.columns(3)
        search_params_work["institutions.country_code"] = c.text_input("Institution Country Code", placeholder="de, us, ...")
        search_params_work["institutions.id"] = d.text_input("Institution ID (OpenAlex)", placeholder="I18014758, ...")
        search_params_work["institutions.ror"] = e.text_input("Institution ID (ROR)", placeholder="03yrm5c26, ...")

        st.markdown("#### Concepts")
        f, g = st.columns(2)
        search_params_work["concept.id"] = f.text_input("Concept ID (OpenAlex)", placeholder="C2778793908, ...")
        search_params_work["concept.wikidata"] = g.text_input("Concept ID (Wikidata)", placeholder="Q5122404, ...")

        st.markdown("#### Venues")
        h, i = st.columns(2)
        search_params_work["host_venue.id"] = h.text_input("Host Venue ID", placeholder="V17087985, ...")
        search_params_work["host_venue.issn"] = i.text_input("Host Venue ISSN", placeholder="2041-1723, ...")

        st.markdown("#### Dates")
        t, u, v, w = st.columns(4)
        search_params_work["publication_date"] = t.text_input("Exact Published Date", placeholder="2023-01-01")
        search_params_work["from_publication_date"] = u.text_input("From Published Date", placeholder="2023-01-01")
        search_params_work["to_publication_date"] = v.text_input("To Published Date", placeholder="2023-01-01")
        search_params_work["publication_year"] = w.text_input("Published Year", placeholder="2023")

        st.markdown("#### Miscellaneous")
        j, k, l = st.columns([2, 2, 1])
        search_params_work["cited_by"] = j.text_input("Cited by (OpenAlex ID)", placeholder="W17087985, ...")
        search_params_work["cites"] = k.text_input("Cites (OpenAlex ID)", placeholder="W17087985, ...")
        search_params_work["cited_by_count"] = l.text_input("Cited by Count", placeholder="20, >10, <100, ...")

        m, n, o = st.columns(3)
        search_params_work["authors_count"] = m.text_input("Number of Authors", placeholder="1, >1, <5, ...")
        search_params_work["doi"] = n.text_input("DOI(s)", placeholder="10.7717/peerj.4375, ...")
        search_params_work["openalex"] = o.text_input("OpenAlex ID(s)", placeholder="W2741809807, ...")
        # ...
        p, q, r= st.columns(3)
        # search_params_work["is_paratext"] = str(p.checkbox("Is Paratext (like books, journals)"))
        # search_params_work["is_retracted"] = str(q.checkbox("Is Retracted"))
        # search_params_work["is_oa"] = str(r.checkbox("Is Open Access"))

        s, x = st.columns(2)
        search_params_work["oa_status"] = s.selectbox("Open Access Status", ("", "green", "gold", "hybrid", "bronze", "unknown"))
        search_params_work["type"] = x.text_input("Type", placeholder="article, book, ...")


        submit_basic = st.form_submit_button(label="Submit")    



    if submit_basic:
        with st.spinner("Performing custom search..."):
            result = multiple_entry_search(search_params_work, polite_email)
            if result == None:
                st.error("No results found")
            else:    
                st.success("Found " + str(result["meta"]["count"]) + " results, first 100 are available to download. For all results, use OpenAlex Snapshots.")
                json_result = json.dumps(result)
                st.download_button("Download Results as JSON", file_name="openalex_search_results.json", mime="application/json", data=json_result, key="download_results")