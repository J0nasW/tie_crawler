import pandas as pd
import requests
import xmltodict
import json
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

import subprocess
import time

# Analyzation Libraries
import pyLDAvis.gensim_models

#import en_core_web_md
from gensim.corpora.mmcorpus import MmCorpus
from gensim.models import LdaModel
from gensim.models import CoherenceModel

import streamlit as st
import streamlit.components as components

from preprocessors.downloaders import (
    get_text_from_pdf_url,
)

from nlp.similarity import (
    calc_similarity,
    calc_similarity_multicore,
)

### STREAMLIT Init:

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="arXiv API", page_icon="📄")

submit_lda_button = False

with st.sidebar:
    st.write("Use Proxy and IP rotation")
    use_proxy = st.checkbox("Use Proxy", value=False)
    ip_addresses = ["82.223.102.92:9443", "198.52.117.208:8080", "185.51.10.19:80", "172.177.221.87:80", "103.152.112.145:80", "5.9.149.118:40000"]
    proxy = st.selectbox("Select IP Address", ip_addresses)

arxiv_api_endpoint = "https://export.arxiv.org/api/"

# Start of the page

st.title("📄 arXiv API")

st.write("The gateway to the arXiv API.")
st.markdown("The arXiv API is a RESTful API that allows you to search for and retrieve information from the arXiv database. You can find more Information here: [arXiv Search API](https://arxiv.org/help/api/index).")

api_query_fields = {}
categories = ["cs.AI", ]

with st.form(key='my_form'):
    a, b = st.columns(2)
    api_query_fields["ti"] = str(a.text_input("Title", placeholder="AI in Medicine").replace(" ", "+"))
    api_query_fields["au"] = str(b.text_input("Author", placeholder="John Doe").replace(" ", "+"))
    api_query_fields["abs"] = str(st.text_area("Abstract", placeholder="AI in Medicine").replace(" ", "+"))
    c, d, e = st.columns(3)
    api_query_fields["co"] = str(c.text_input("Comment", placeholder="...").replace(" ", "+"))
    api_query_fields["jr"] = str(d.text_input("Journal Reference", placeholder="...").replace(" ", "+"))
    api_query_fields["cat"] = str(e.text_input("Category", placeholder="cs.AI").replace(" ", "+"))
    f, g, h, i = st.columns(4)
    api_query_fields["rn"] = str(f.text_input("Report Number", placeholder="0123").replace(" ", "+"))
    api_query_fields["id_list"] = str(g.text_input("ID", placeholder="arXiv ID").replace(" ", "+"))
    #api_query_fields["all"] = str(st.text_input("All", placeholder="All of the above").replace(" ", "+"))
    api_query_fields["doi"] = str(h.text_input("DOI", placeholder="10.1234/1234"))
    api_query_fields["max_results"] = i.number_input("Limit", min_value=1, max_value=5000, value=20)
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    st.write("arXiv API Query:")
    raw_query = "query?search_query="
    for key, value in api_query_fields.items():
        if value != "" and key != "max_results":
            raw_query = str(raw_query) + str(key) + ":" + str(value) + "+AND+"
    raw_query = raw_query[:-5] + "&max_results=" + str(api_query_fields["max_results"])

    st.write(arxiv_api_endpoint + raw_query)
    with st.spinner("Searching for Papers..."):
        if use_proxy:
            results = requests.get(arxiv_api_endpoint + raw_query, proxies=proxy, timeout=10)
        else:
            results = requests.get(arxiv_api_endpoint + raw_query, timeout=10)
    
        if results.status_code == 200:
            data = xmltodict.parse(results.text)
            st.info("Found " + data["feed"]["opensearch:totalResults"]["#text"] + " Total Results and " + data["feed"]["opensearch:itemsPerPage"]["#text"] + " Results per Page. Limit was set to " + str(api_query_fields["max_results"]) + ".", icon="ℹ️")
            #st.write(data["feed"]["entry"])
            if data["feed"]["opensearch:totalResults"]["#text"] == "0":
                st.warning("No Results Found. Try again with different search parameters.")
            else:
                st.session_state.arxiv_results = data["feed"]["entry"]

        else:
            st.error("Something went wrong. Please try again.")
            st.write(results.status_code)

if st.session_state.arxiv_results:
    with st.expander("Download and Show Results"):
        st.download_button("Download Results as JSON", data=json.dumps(st.session_state.arxiv_results, indent=4), file_name="arxiv_results.json", mime="application/json")
        st.write(pd.json_normalize(st.session_state.arxiv_results))

    if st.button("Download PDFs"):
        st.spinner("Downloading PDFs...")
        urls = [st.session_state.arxiv_results[i]["link"][1]["@href"] for i in range(len(st.session_state.arxiv_results))]
        df, error_links, error_files = get_text_from_pdf_url(urls)
        st.info("Encountered " + str(len(error_links)) + " Errors while trying to download PDFs and " + str(len(error_files)) + " Errors while trying to read PDFs.", icon="ℹ️")
        st.session_state.arxiv_pdf_results = df

if st.session_state.arxiv_pdf_results.empty == False:
    with st.expander("Download and Show PDF Results"):
        st.download_button("Download PDF Contents as JSON", data=json.dumps(st.session_state.arxiv_pdf_results.to_dict()), file_name="arxiv_pdf_results.json", mime="application/json")
        st.write(st.session_state.arxiv_pdf_results)

    if st.button("Analyze PDFs with LDA"):
        st.session_state.arxiv_pdf_results["pdf_text"].to_csv("tmp/pdf_results.csv", index=False)
        lda_process = subprocess.Popen(["python", "nlp/lda.py", "--text_csv", "tmp/pdf_results.csv", "--save_dir", "tmp/", "--num_iterations", "10", "--num_topics", "3", "--num_workers", "8", "--num_passes", "10", "--dict_no_below", "2", "--dict_no_above", "0.5", "--dict_keep_n", "10000"])
        # Wait for the process to finish
        while lda_process.poll() is None:
            st.spinner('Subprocess is still running...')
            time.sleep(1)
        # The process has finished
        if lda_process.poll() == 0:
            st.success('Subprocess has finished successfully!', icon="✅")
            st.session_state.arxiv_lda_finished = True
            st.session_state.arxiv_lda_results = "tmp/lda_model.gensim"

        else:
            st.error('Subprocess has finished with an error!', icon="❌")
            st.session_state.arxiv_lda_finished = False

    if st.button("Calculate similarity"):
        # similarity, avg_similarity = calc_similarity(st.session_state.arxiv_pdf_results["pdf_text"])
        text_list = st.session_state.arxiv_pdf_results["pdf_text"].tolist()

        similarity_process = subprocess.Popen(["python", "nlp/similarity.py", "--text", text_list, "--save_dir", "tmp/", "--num_workers", "8"])
        # Wait for the process to finish
        while similarity_process.poll() is None:
            st.spinner('Subprocess is still running...')
            time.sleep(1)
        # The process has finished
        if similarity_process.poll() == 0:
            st.success('Subprocess has finished successfully!', icon="✅")
        
        similarity, avg_similarity = calc_similarity_multicore(text_list)
        st.session_state.arxiv_similarity_matrix = similarity
        with st.expander("Similarity Results"):
            st.metric("Average Similarity:", str(avg_similarity.round(2)) + "%")
            sns.heatmap(similarity, annot=True, cmap="YlGnBu")
            plt.title("Similarity Matrix")
            plt.show()

if st.session_state.arxiv_lda_finished:
    lda_model = LdaModel.load("tmp/lda_model.gensim")
    pdf_corpus = MmCorpus("tmp/corpus.mm")
    pdf_dict = Dictionary.load("tmp/dictionary.gensim")
    
    with st.expander("LDA Results"):
        lda_display = pyLDAvis.gensim_models.prepare(lda_model, pdf_corpus, pdf_dict)
        html_string = pyLDAvis.prepared_data_to_html(lda_display, template_type="general")

        components.v1.html(html_string, width=1400, height=800, scrolling=True)

