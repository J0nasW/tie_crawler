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
import pydeck as pdk
import pandas as pd

import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

### STREAMLIT Init:

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="AI Competence Radar", page_icon=":earth:")

# Start of the page

st.title("🌍 AI Competence Radar")
st.write("An AI Radar of Germany and the US.")

max_entries = 600

if st.button("Show Data"):
    st.spinner("Showing Data")

    locator = Nominatim(user_agent="TIE_GeoCoder")

    # location = locator.geocode("Frankfurt am Main, Germany")
    # location = locator.geocode("8222 Douglas Avenue, Dallas, United States")
    # st.write("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))

    pitchbook_data = pd.read_csv("../.local_dev/Company.csv")

    # pitchbook_data["full_address"] = pitchbook_data["HQAddressLine1"] + ", " + pitchbook_data["HQPostCode"] + ", " + pitchbook_data["HQCity"] + ", " + pitchbook_data["HQState_Province"] + ", " + pitchbook_data["HQCountry"]
    pitchbook_data["full_address"] = pitchbook_data["HQPostCode"] + ", " + pitchbook_data["HQCity"] + ", " + pitchbook_data["HQCountry"]

    # Limit the entries to 3 for testing

    pitchbook_data_germany = pitchbook_data[pitchbook_data["HQCountry"].isin(["Germany"])]
    pitchbook_data_lite = pitchbook_data_germany.head(max_entries)

    # 1 - conveneint function to delay between geocoding calls
    geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
    # 2- - create location column
    pitchbook_data_lite['geolocation'] = pitchbook_data_lite['full_address'].apply(geocode)
    # 3 - create longitude, laatitude and altitude from location column (returns tuple)
    pitchbook_data_lite['point'] = pitchbook_data_lite['geolocation'].apply(lambda loc: tuple(loc.point) if loc else None)
    # 4 - split point column into latitude, longitude and altitude columns
    pitchbook_data_lite[['latitude', 'longitude', 'altitude']] = pd.DataFrame(pitchbook_data_lite['point'].tolist(), index=pitchbook_data_lite.index)

    st.write(pitchbook_data_lite)
    st.session_state.geocode_df = pitchbook_data_lite

    st.success("Done! Found " + str(len(pitchbook_data_germany)) + " entries. Limited to " + str(max_entries) + " entries for testing.")

manual_override = st.checkbox("Override for manual upload")
if manual_override:
    manual_csv = st.file_uploader("Upload a file", type=["csv"], accept_multiple_files=False)

if st.button("Show Map"):

    if manual_override:
        pitchbook_data_lite = pd.read_csv(manual_csv)
    else:
        pitchbook_data_lite = st.session_state.geocode_df
    pitchbook_data_lite = pitchbook_data_lite[["latitude", "longitude"]]

    pitchbook_data_lite["lat"]=pd.to_numeric(pitchbook_data_lite["latitude"]) 
    pitchbook_data_lite["lon"]=pd.to_numeric(pitchbook_data_lite["longitude"])

    pitchbook_data_lite = pitchbook_data_lite.dropna()

    st.map(pitchbook_data_lite, zoom=5, use_container_width=True)

    # Define a layer to display on a map
    layer = pdk.Layer(
        "HexagonLayer",
        data=pitchbook_data_lite,
        get_position=['lon', 'lat'],
        auto_highlight=True,
        elevation_scale=100,
        pickable=True,
        elevation_range=[0, 3000],
        extruded=True,
        coverage=1,
    )

    # Set the viewport location
    view_state = pdk.ViewState(
        longitude=10,
        latitude=50,
        zoom=5,
        min_zoom=1,
        max_zoom=20,
        pitch=40.5,
        bearing=-27.36,
    )

    # Render
    r = pdk.Deck(layers=[layer], initial_view_state=view_state)
    st.pydeck_chart(r)

    if not manual_override:
        st.download_button(
        label="Download data as CSV",
        data=st.session_state.geocode_df.to_csv().encode('utf-8'),
        file_name='Pitchbook_Dataset.csv',
        mime='text/csv',
        )