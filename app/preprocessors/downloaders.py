####################################################################################
# Preprocessors for downloading Files from the internet
# by JW
#
# A powerful collection of utilities to download files from the internet. 
# 
# preprocessors / downloaders.py
####################################################################################

# IMPORT STATEMENTS ----------------------------------------------------------------
import pandas as pd
import requests
from io import BytesIO

# Own functions
from preprocessors.text_extraction import read_pdf, clean_text

# Download PDFs from URL List - returns a DataFrame with the PDFs and a list of URLs that could not be downloaded
def download_pdfs_from_urls(urls, proxies=[]):
    """Download PDFs from URLs"""
    pdf_df = pd.DataFrame(columns=["pdf_url", "pdf_file"])
    error_links = []
    if proxies == []:
        for url in urls:
            print("Downloading " + str(url) + "...")
            pdf = requests.get(url)
            if pdf.status_code == 200:
                pdf_df.loc[len(pdf_df)] = [url, pdf.content]
            else:
                error_links.append(url)
    else:
        for url in urls:
            pdf = requests.get(url, proxies=proxies)
            if pdf.status_code == 200:
                pdf_df.loc[len(pdf_df)] = [url, pdf.content]
            else:
                error_links.append(url)
    return pdf_df, error_links

def get_text_from_pdf_url(urls, proxies=[]):
    df = pd.DataFrame(columns=["pdf_url", "pdf_text"])
    error_files = []

    pdf_df, error_links = download_pdfs_from_urls(urls, proxies)

    for index, row in pdf_df.iterrows():
        print("Reading " + row["pdf_url"] + "...")
        try:
            pdf_text = read_pdf(BytesIO(row["pdf_file"]))
            cleaned_file_text = clean_text(pdf_text)
            df.loc[len(df)] = [row["pdf_url"], cleaned_file_text]
        except Exception as e:
            print(e)
            error_files.append(row["pdf_url"])

    return df, error_links, error_files