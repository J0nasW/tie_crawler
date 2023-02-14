### Arxiv API Endpoint


import requests
import xmltodict

def get_arxiv_results(raw_query, arxiv_api_endpoint="https://export.arxiv.org/api/", use_proxy=False, proxy=None):
    print("arXiv API Query: " + arxiv_api_endpoint + "query?search_query=" + raw_query)
    if use_proxy:
        results = requests.get(arxiv_api_endpoint + "query?search_query=" + raw_query, proxies=proxy, timeout=10)
    else:
        results = requests.get(arxiv_api_endpoint + "query?search_query=" + raw_query, timeout=10)

    if results.status_code == 200:
        data = xmltodict.parse(results.text)
        #st.write(data["feed"]["entry"])
        if data["feed"]["opensearch:totalResults"]["#text"] == "0":
            print("No Results Found. Try again with different search parameters.")
            return None
        else:
            print("Found " + data["feed"]["opensearch:totalResults"]["#text"] + " Total Results and " + data["feed"]["opensearch:itemsPerPage"]["#text"] + " Results per Page.")
            return data["feed"]["entry"]
    else:
        print("Something went wrong. Please try again.")
        print(results.status_code)
        return None