####################################################################################
# Text Extractor
# by JW
#
# A simple python tool to extract text from websites, PDFs, and other file formats.
# 
# pages / Text_Extractor.py
####################################################################################

# IMPORT STATEMENTS ----------------------------------------------------------------
import streamlit as st
import validators
import json
from preprocessors.text_extraction import (
    clean_text,
    fetch_article_text,
    preprocess_text_for_abstractive_summarization,
    read_text_from_file,
    format_url
)

### STREAMLIT Init:

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="Text Extractor", page_icon="📝")

# Start of the page

st.title("📝 Text Extractor")

st.write("A simple python tool to extract text from websites, PDFs, and other file formats.")
# st.info("Still in development")

text_extracted = st.session_state["text_extracted"]
url_text = st.session_state["url_text"]
cleaned_raw_text = st.session_state["cleaned_raw_text"]
uploaded_files_infos = st.session_state["uploaded_files_infos"]
url_infos = st.session_state["url_infos"]



with st.expander("Text / File Input", expanded=not text_extracted):

    with st.form("text_extractor_form"):
        text_input = st.text_area("Enter text or URL here", height=100)
        st.markdown(
            "<h3 style='text-align: center; color: green;'>OR</h3>",
            unsafe_allow_html=True,
        )
        
        uploaded_file = st.file_uploader(
            "Upload a .txt, .pdf, .docx or .pptx file for summarization.", type=["txt", "pdf", "docx", "pptx"], accept_multiple_files=True
        )
        st.markdown(
            "<h3 style='text-align: center; color: green;'>OR</h3>",
            unsafe_allow_html=True,
        )
        uploaded_list_of_urls = st.file_uploader(
            "Upload a list of URLs in .txt format for summarization.", type="txt", accept_multiple_files=False
        )
        submit_text_extract = st.form_submit_button(label="Extract Text")    

if submit_text_extract:
    text_extracted = False
    try:
        if validators.url(text_input):
            url_text = []
            st.session_state["url_text"] = []
            url_raw_text, url_sentences = fetch_article_text(url=text_input)
            cleaned_url_text = clean_text(url_raw_text)
            url_dict = {'url': text_input, 'url_text': url_raw_text, 'cleaned_url_text': cleaned_url_text, 'url_text_chunks': url_sentences}
            url_text.append(url_dict)
            text_extracted = True
            st.session_state["url_text"] = url_text
            st.success("Text extracted successfully")
        elif uploaded_file:
            if uploaded_file is not None and uploaded_file:
                uploaded_files_infos = []
                st.session_state["uploaded_files_infos"] = []
                for i in range(len(uploaded_file)):
                    file_text = read_text_from_file(uploaded_file[i])
                    cleaned_file_text = clean_text(file_text)
                    file_dict = {'file_name': uploaded_file[i].name, 'file_type': uploaded_file[i].type, 'file_size': uploaded_file[i].size, 'file_text': file_text, 'cleaned_file_text': cleaned_file_text}
                    uploaded_files_infos.append(file_dict)
            text_extracted = True
            st.session_state["uploaded_files_infos"] = uploaded_files_infos
            st.success("Text extracted successfully")
        elif text_input:
            cleaned_raw_text = ""
            st.session_state["cleaned_raw_text"] = ""
            cleaned_raw_text = clean_text(text_input)
            text_extracted = True
            st.session_state["cleaned_raw_text"] = cleaned_raw_text
            st.success("Text extracted successfully")
        elif uploaded_list_of_urls:
            if uploaded_list_of_urls is not None:
                    url_infos = []
                    st.session_state["url_infos"] = []
                    st.write("Extracting text from URLs...")
                    progress_bar = st.progress(0)
                    list_of_urls = uploaded_list_of_urls.read().decode('utf-8')
                    list_of_urls = list_of_urls.splitlines()
                    total_url_count = len(list_of_urls)
                    for url in list_of_urls:
                        try:
                            url = format_url(url)
                            if validators.url(url):
                                article_text, article_text_chunks = fetch_article_text(url=url)
                                cleaned_article_text = clean_text(article_text)
                                file_dict = {'url': url, 'article_text': article_text, 'cleaned_article_text': cleaned_article_text, 'article_text_chunks': article_text_chunks}
                                url_infos.append(file_dict)
                            else:
                                st.error(f"Invalid URL: {url}")
                        except Exception as e:
                            st.error("Invalid URL" + url)
                        progress_bar.progress(len(url_infos) / total_url_count)
            text_extracted = True
            st.session_state["url_infos"] = url_infos
            st.success("Text extracted successfully")
        else:
            st.error("No Text, URL or file uploaded")
            text_extracted = False

    except Exception as e:
        st.error("Invalid URL or file")
        st.write(e)
 
if text_extracted:
    st.write("## Extracted Text")
    if validators.url(text_input):
        # st.write("### Article Text")
        # st.write(url_text)
        # st.write("### Cleaned Article Text")
        # st.write(cleaned_url_text)
        # st.write("### Article Text Chunks")
        # st.write(url_sentences)
        json_result = json.dumps(st.session_state["url_text"])
        st.download_button("Download URL Text", data=json_result, file_name="url_text.json", mime="application/json")
    elif uploaded_file:
        # st.write("### File Text")
        # st.write(uploaded_files_infos)
        json_result = json.dumps(st.session_state["uploaded_files_infos"])
        st.download_button("Download File Text", data=json_result, file_name="file_text.json", mime="application/json")
    elif uploaded_list_of_urls:
        # st.write("### URLs Text")
        # st.write(url_infos)
        json_result = json.dumps(st.session_state["url_infos"])
        st.download_button("Download URLs Text", data=json_result, file_name="urls_text.json", mime="application/json")
    else:
        # st.write("### Cleaned Raw Text")
        # st.write(cleaned_raw_text
        st.download_button("Download Raw Text", data=st.session_state["cleaned_raw_text"], file_name="raw_text.txt", mime="text/plain")