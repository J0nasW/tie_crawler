###
# Analysis, whether OpenAlex contains all publications from arXiv
#
###

import streamlit as st
import pandas as pd
import time

import requests
from bs4 import BeautifulSoup

import arxiv

# Own Modules
from endpoints.arxiv import get_arxiv_results

### STREAMLIT Init:

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="arXiv to OpenAlex Comparison", page_icon="🔎")

# Session States
if "arxiv_crawl" not in st.session_state:
    st.session_state.arxiv_crawl = False

if "arxiv_crawl_v2" not in st.session_state:
    st.session_state.arxiv_crawl_v2 = False

if "oalex_crawl" not in st.session_state:
    st.session_state.oalex_crawl = False

if "arxiv_queries" not in st.session_state:
    st.session_state.arxiv_queries = {}

if "arxiv_results" not in st.session_state:
    st.session_state.arxiv_results = {}

if "df_arxiv_results" not in st.session_state:
    st.session_state.df_arxiv_results = pd.DataFrame()

if "arxiv_ids" not in st.session_state:
    st.session_state.arxiv_ids = pd.DataFrame()

# Start of the page

st.title("🔎 arXiv to OpenAlex Comparison")
st.write("Compare the arXiv API with the OpenAlex API.")
st.markdown("For Category search on arXiv, see [arXiv Category Taxonomy](https://arxiv.org/category_taxonomy). Asterisk (*) can be used as a wildcard.")

arxiv_crawl = st.session_state.arxiv_crawl
arxiv_crawl_v2 = st.session_state.arxiv_crawl_v2
arxiv_queries = {}
arxiv_results = {}

def get_arxiv_doi(arxiv_url, limit=0):
    arxiv_html = requests.get(arxiv_url).text
    arxiv_soup = BeautifulSoup(arxiv_html, "html.parser")
    try:
        arxiv_doi = arxiv_soup.find_all("a", attrs={"data-doi":True})[0]["data-doi"]
        print("DOI: " + arxiv_doi)
        return arxiv_doi
    except:
        return "no_doi"

def fetch_arxiv_doi(query, limit=100):
    search = arxiv.Search(
        query = query,
        max_results = limit,
        sort_by = arxiv.SortCriterion.SubmittedDate
    )
    return search.results()


with st.expander("#1 arXiv Crawl", expanded=not arxiv_crawl):
    st.write("First, we crawl the arXiv API for given search queries.")
    with st.form("arXiv Crawl Input"):
        a, b = st.columns([8, 1])
        arxiv_queries["query_1"] = a.text_input("arXiv Query #1", value="cat:cs.*")
        arxiv_queries["query_1_limit"] = b.number_input("Limit Query #1", value=100, min_value=1, max_value=1000, step=1)

        c, d = st.columns([8, 1])
        arxiv_queries["query_2"] = c.text_input("arXiv Query #2", value="cat:math.*")
        arxiv_queries["query_2_limit"] = d.number_input("Limit Query #2", value=100, min_value=1, max_value=1000, step=1)

        e, f = st.columns([8, 1])
        arxiv_queries["query_3"] = e.text_input("arXiv Query #3", value="cat:eess.*")
        arxiv_queries["query_3_limit"] = f.number_input("Limit Query #3", value=100, min_value=1, max_value=1000, step=1)

        g, h = st.columns([8, 1])
        arxiv_queries["query_4"] = g.text_input("arXiv Query #4", value="cat:q-bio.*")
        arxiv_queries["query_4_limit"] = h.number_input("Limit Query #4", value=100, min_value=1, max_value=1000, step=1)

        i, j = st.columns([8, 1])
        arxiv_queries["query_5"] = i.text_input("arXiv Query #5", value="cat:q-fin.*")
        arxiv_queries["query_5_limit"] = j.number_input("Limit Query #5", value=100, min_value=1, max_value=1000, step=1)

        k, l = st.columns([8, 1])
        arxiv_queries["query_6"] = k.text_input("arXiv Query #6", value="cat:econ.*")
        arxiv_queries["query_6_limit"] = l.number_input("Limit Query #6", value=100, min_value=1, max_value=1000, step=1)

        submit_button = st.form_submit_button(label='Submit')

    # if submit_button:
    #     st.spinner("Crawling arXiv API...")
    #     arxiv_crawl = True
    #     st.session_state.arxiv_queries = arxiv_queries
    #     st.session_state.arxiv_crawl = arxiv_crawl
    #     arxiv_results["result_1"] = get_arxiv_results(raw_query=str(arxiv_queries["query_1"]) + "&max_results=" + str(arxiv_queries["query_1_limit"]) + "&sortBy=submittedDate&sortOrder=descending")
    #     time.sleep(5)
    #     arxiv_results["result_2"] = get_arxiv_results(raw_query=str(arxiv_queries["query_2"]) + "&max_results=" + str(arxiv_queries["query_2_limit"]) + "&sortBy=submittedDate&sortOrder=descending")
    #     time.sleep(5)
    #     arxiv_results["result_3"] = get_arxiv_results(raw_query=str(arxiv_queries["query_3"]) + "&max_results=" + str(arxiv_queries["query_3_limit"]) + "&sortBy=submittedDate&sortOrder=descending")
    #     time.sleep(5)
    #     arxiv_results["result_4"] = get_arxiv_results(raw_query=str(arxiv_queries["query_4"]) + "&max_results=" + str(arxiv_queries["query_4_limit"]) + "&sortBy=submittedDate&sortOrder=descending")
    #     time.sleep(5)
    #     arxiv_results["result_5"] = get_arxiv_results(raw_query=str(arxiv_queries["query_5"]) + "&max_results=" + str(arxiv_queries["query_5_limit"]) + "&sortBy=submittedDate&sortOrder=descending")
    #     time.sleep(5)
    #     arxiv_results["result_6"] = get_arxiv_results(raw_query=str(arxiv_queries["query_6"]) + "&max_results=" + str(arxiv_queries["query_6_limit"]) + "&sortBy=submittedDate&sortOrder=descending")
    #     st.session_state.arxiv_results = arxiv_results
    #     st.experimental_rerun()


        if submit_button:
            st.spinner("Crawling arXiv API...")
            arxiv_crawl_v2 = True
            st.session_state.arxiv_queries = arxiv_queries
            st.session_state.arxiv_crawl_v2 = arxiv_crawl_v2
            arxiv_results["result_1"] = fetch_arxiv_doi(str(arxiv_queries["query_1"]), arxiv_queries["query_1_limit"])
            time.sleep(5)
            arxiv_results["result_2"] = fetch_arxiv_doi(str(arxiv_queries["query_2"]), arxiv_queries["query_2_limit"])
            time.sleep(5)
            arxiv_results["result_3"] = fetch_arxiv_doi(str(arxiv_queries["query_3"]), arxiv_queries["query_3_limit"])
            time.sleep(5)
            arxiv_results["result_4"] = fetch_arxiv_doi(str(arxiv_queries["query_4"]), arxiv_queries["query_4_limit"])
            time.sleep(5)
            arxiv_results["result_5"] = fetch_arxiv_doi(str(arxiv_queries["query_5"]), arxiv_queries["query_5_limit"])
            time.sleep(5)
            arxiv_results["result_6"] = fetch_arxiv_doi(str(arxiv_queries["query_6"]), arxiv_queries["query_6_limit"])
            st.session_state.arxiv_results = arxiv_results
            st.experimental_rerun()

if arxiv_crawl:
    st.success("arXiv Crawl done.", icon="✅")
    arxiv_queries = st.session_state.arxiv_queries
    arxiv_results = st.session_state.arxiv_results
    df_arxiv_results = pd.DataFrame(columns="id search_category categories".split())
    # st.write(arxiv_results["result_1"])
    for key, value in arxiv_results.items():
        # st.write(len(value))
        for i in range(0, len(value)):
            # st.write(value[i]["id"])
            categories = []
            # st.write(value[i]["category"])
            # st.write(len(value[i]["category"]))
            try:
                if value[i]["category"]["@term"]:
                    categories.append(value[i]["category"]["@term"])
            except:
                for j in range(len(value[i]["category"])):
                    categories.append(value[i]["category"][j]["@term"])
            # st.write(categories)
            df_arxiv_results = df_arxiv_results.append({"id": value[i]["id"], "search_category": arxiv_queries["query_" + key[7:]], "categories": categories}, ignore_index=True)
    df_arxiv_results.drop_duplicates(subset="id", inplace=True)
    st.write(df_arxiv_results)
    st.session_state.df_arxiv_results = df_arxiv_results

if arxiv_crawl_v2:
    st.success("arXiv Crawl done.", icon="✅")
    arxiv_queries = st.session_state.arxiv_queries
    arxiv_results = st.session_state.arxiv_results
    for key, value in arxiv_results.items():
        for results in arxiv_results[key]:
            try: 
                st.write(results.doi)
            except:
                st.write("No DOI found.")

# if st.session_state.df_arxiv_results.empty == False:
#     st.success("arXiv ID extraction done.", icon="✅")
#     doi_list = []
#     df_arxiv_results = st.session_state.df_arxiv_results
#     if st.button("Retrieve DOIs from arXiv IDs"):
#         st.spinner("Retrieving DOIs from arXiv IDs...")
#         for id in df_arxiv_results["id"].head(100):
#             doi = get_arxiv_doi(id)
#             doi_list.append(doi)
#             time.sleep(1)
#             #df_arxiv_results.loc[df_arxiv_results["id"] == id, "doi"] = doi
#         #df_arxiv_results["doi"] = df_arxiv_results["id"].apply(lambda x: get_arxiv_doi(x))
#         df_doi_list = pd.DataFrame(doi_list, columns=["doi"])
#         df_doi_list.remove_duplicates(subset="doi", inplace=True)
#         st.write(doi_list)
#         # st.session_state.arxiv_dois = df_arxiv_results
#         # st.experimental_rerun()