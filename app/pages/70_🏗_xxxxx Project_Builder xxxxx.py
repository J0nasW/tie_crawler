####################################################################################
# Postgres Admin Tool
# by JW
#
# For some Postgres admin actions and testing purposes
# 
# Home.py / Postgres_Admin_Tool.py
####################################################################################

# IMPORT STATEMENTS ----------------------------------------------------------------
import streamlit as st
from datetime import datetime as dt

# Own Functions
from helpers.db_functions import *


# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="Project Builder", page_icon="🏗")

project_submit = st.session_state["project_submit"]

st.title("🏗 Project Builder")

st.write("A simple tool to build projects.")

# SIDEBAR -----------------------------------------

with st.sidebar:
    st.header("Configurations")

    if st.session_state.db_connection_status:
        st.success("Your Database is connected!", icon="✅")
    else:
        st.warning("It seems, that your Database is not connected yet.", icon="⚠️")
        # if st.session_state.postgres_cred != {}:
        #     st.write("But there are some database information stored in the session. You can try to connect with these:")
        #     st.button(label="Connect with session credentials", on_click=postgres_init(st.session_state.postgres_cred))

    # with st.expander("Postgres DB Connection"):
    #     with st.form("postgres_connect_sidebar"):

    #         postgres_cred = st.session_state.postgres_cred

    #         st.write("Provide Postgres DB Infos here:")

    #         postgres_cred["name"] = st.text_input(label="Name of Connection", value="MyServer")
    #         postgres_cred["host"] = st.text_input(label="Postgres DB Host", value="localhost")
    #         postgres_cred["port"] = st.number_input(label="Postgres DB Port", value=15433)
    #         postgres_cred["db_name"] = st.text_input(label="DB Name", value="tie_crawler")
    #         postgres_cred["db_user"] = st.text_input(label="DB User", value="tie")
    #         postgres_cred["db_password"] = st.text_input(label="DB Password", value="iPkt9FsmoQ7*xdGr")

    #         # Every form must have a submit button.
    #         submitted = st.form_submit_button("Submit")

# ----------------------------------------------------



# if submitted:
#     st.session_state.postgres_cred = postgres_cred
#     with st.spinner('Wait while we connect your databse...'):
#         try:
#             db_engine, db_connection = postgres_init(postgres_cred)
#             st.session_state.db_engine = db_engine
#             st.session_state.db_connection_status = True
#             st.session_state.db_connection = db_connection
#             st.success("Connection to Database " + postgres_cred["host"] + ":" + str(postgres_cred["port"]) + " successful!")
#         except Exception as e:
#             st.error("There was an unexpected error while connecting to your Postgres DB. Please try again and double check your DB credentials.")
#             st.write(e)
#             st.session_state.db_connection_status = False


if st.session_state.db_connection_status:
    with st.form("new_project", clear_on_submit=True):

        project = {}

        st.write("Create a new project inside the tie database:")

        project["name"] = st.text_input(label="Name of the Project", placeholder="My first project")
        project["description"] = st.text_area(label="Description", placeholder="Some facts about your project")
        project["creationdate"] = dt.now()
        st.write("Choose the services that are activated for your project:")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            project["use_twitter"] = st.checkbox("Use Twitter")
        with col2:
            project["use_oalex"] = st.checkbox("Use OpenALEX")
        with col3:
            project["use_scopus"] = st.checkbox("Use Scopus")
        with col4:
            project["use_arxiv"] = st.checkbox("Use arXiv")
        st.write("")
        col1, col2, = st.columns(2)
        with col1:
            project["startdate"] = st.date_input("Start date",)
        with col2:
            project["enddate"] = st.date_input("End date", dt.now())
        st.write("")
        st.write("Now you can choose, if you want your project to stream data in the future or if you just want a normal crawl. Note, that when streaming, you must provide an end date that lies in the future. (EXPERIMENTAL)")
        col1, col2, = st.columns(2)
        with col1:
            project["streaming"] = st.checkbox("Stream data from the future")
        with col2:
            option = st.selectbox(
                        'Crawl frequency in the future',
                        ("", 'Every 15min', 'Every 30min', 'Every hour', "Once per day", "Once per week", "Once per month"))
            if option == "Every 15min":
                project["crawl_frequency"] = "15"
            elif option == "Every 30min":
                project["crawl_frequency"] = "30"
            elif option == "Every hour":
                project["crawl_frequency"] = "hourly"
            elif option == "Once per day":
                project["crawl_frequency"] = "daily"
            elif option == "Once per week":
                project["crawl_frequency"] = "weekly"
            elif option == "Once per month":
                project["crawl_frequency"] = "monthly"
            else:
                project["crawl_frequency"] = ""

        # Every form must have a submit button.
        project_submit = st.form_submit_button("Submit")
        st.session_state.project_submit = True

if project_submit:
    with st.spinner('Wait while we create your project...'):
        try:
            project_created, result = project_init(project)
            
            st.success("The project " + project["name"] + " has been created successfully! The UUID is: " + str(project["uuid"]))
            if project["name"] not in st.session_state:
                st.session_state[project["name"]] = project
        except Exception as e:
            st.error("There was an unexpected error while creating your project. Please try again or check the error messages below.")
            st.write(e)