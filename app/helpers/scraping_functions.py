####################################################################################
# Scraping Functions
# by JW
#
# A helper script to initialize the DB and other things at first boot of the
# container cluster.
#
# helpers / scraping_functions.py
####################################################################################

# IMPORT STATEMENTS ----------------------------------------------------------------
import requests
from bs4 import BeautifulSoup

def get_proxy_list():
    """Get a list of proxies from https://free-proxy-list.net/"""
    proxy_list = []
    res = requests.get('https://free-proxy-list.net/', headers={'User-Agent':'Mozilla/5.0'})
    soup = BeautifulSoup(res.text,"lxml")
    for items in soup.select("#proxylisttable tbody tr"):
        proxy_list.append(':'.join([item.text for item in items.select("td")[:2]]))
    return proxy_list