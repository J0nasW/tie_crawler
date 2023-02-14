###
# XML to DICT
#
###

import streamlit as st
import pandas as pd
import xmltodict
import xml.etree.cElementTree as ET
import re
from bs4 import BeautifulSoup

### STREAMLIT Init:

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="XML to DICT", page_icon="🔎")


xml_file = st.file_uploader("Upload XML File", type="xml")
xml_dir = "tmp/ipg130730.xml"

if st.button("Convert XML to DICT"):
    st.write(xml_file)
    soup = BeautifulSoup(xml_file,'xml')
    st.write(soup)
    #tree = ET.fromstring(re.sub(r"(<\?xml[^>]+\?>)", r"\1<root>", xml) + "</root>")
    data = xmltodict.parse(soup)

    data_df = pd.DataFrame(data)

    st.write(data_df)

if st.button("ET"):
    tree = ET.parse(xml_dir)
    root = tree.getroot()

    st.write(root)