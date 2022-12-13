####################################################################################
# DB Functions
# by JW
#
# A collection of powerful functions to connect and interact with Postgres Databases
# 
# helpers / db_functions.py
####################################################################################

# IMPORT STATEMENTS ----------------------------------------------------------------
import streamlit as st
import uuid
import pandas as pd 
from datetime import datetime as dt


# For Postgres DB Connection
from sqlalchemy import create_engine, schema, insert, MetaData, Table, Column, Integer, String, VARCHAR, Date, Boolean, select, exists
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import sessionmaker

# Own functions
from helpers.helper_functions import *


def postgres_init(postgres_cred):
    # INITIALIZE POSTGRES DB CONNECTION
    conn_str = "postgresql://" + postgres_cred["db_user"] + ":" + postgres_cred["db_password"] + "@" + postgres_cred["host"] + ":" + str(postgres_cred["port"]) + "/" + postgres_cred["db_name"]

    engine = create_engine(conn_str)
    connection = engine.connect()

    
    return engine, connection

def tie_init(postgres_cred, schema_name):
    db_connection = False
    schema_created = False
    project_created = False
    services_created = False

    try:
        conn_str = "postgresql://" + postgres_cred["db_user"] + ":" + postgres_cred["db_password"] + "@" + postgres_cred["host"] + ":" + str(postgres_cred["port"]) + "/" + postgres_cred["db_name"]

        engine = create_engine(conn_str)
        connection = engine.connect()
        session = sessionmaker(engine)
        session = session()

        meta = MetaData()

        db_connection = True

        st.session_state["db_engine"] = engine
        st.session_state["db_connection"] = connection
        st.session_state["db_meta"] = meta
        st.session_state["db_session"] = session
        st.session_state["db_connection_status"] = db_connection
    except Exception as e:
        print(e)
        db_connection = False
    
    if db_connection:
        try:
            if schema_name not in connection.dialect.get_schema_names(connection):
                connection.execute(schema.CreateSchema(schema_name))
            schema_created = True
        except Exception as e:
            print(e)
            schema_created = False

    if schema_created:
        try:
            projects = Table(
                "projects", meta,
                Column("id", UUID(as_uuid=True), primary_key=True),
                Column("name", VARCHAR(100)),
                Column("description", VARCHAR(255)),
                Column("creationdate", Date),
                Column("use_twitter", Boolean),
                Column("use_oalex", Boolean),
                Column("use_scopus", Boolean),
                Column("use_arxiv", Boolean),
                Column("streaming", Boolean),
                Column("startdate", Date),
                Column("enddate", Date),
                Column("running", Boolean),
                Column("crawl_frequency", String),
            )
            meta.create_all(engine)
            project_created = True

            st.session_state.db_table_projects = projects
        except Exception as e:
            print(e)
            project_created = False

    if project_created:
        try:
            # Twitter Services
            twitter_crawls = Table(
                "twitter_crawls", meta,
                Column("projectid", UUID(as_uuid=True), primary_key=True),
                Column("query", VARCHAR(255)),
                Column("ext_query", VARCHAR(255)),
                Column("last_crawl", Date),
                Column("tweet_limit", Integer),
                Column("min_replies", Integer),
                Column("min_retweets", Integer),
                Column("min_likes", Integer),
                Column("date_from", Date),
                Column("date_to", Date),
                Column("excl_replies", Boolean),
                Column("excl_retweets", Boolean),
            )
            

            # OpenALEX Services
            # tbc

            # Scopus Services
            # tbc

            # arXiv Services
            # tbc

            meta.create_all(engine)
            services_created = True

            st.session_state.db_table_twitter_crawls = twitter_crawls
        except Exception as e:
            print(e)
            services_created = False    

    return db_connection, schema_created, project_created, services_created

def project_init(project):
    project_created = False
    db_table_projects = st.session_state.db_table_projects
    connection = st.session_state.db_connection
    
    try:
        project["uuid"] = uuid.uuid4()
        if project["streaming"]:
            project["running"] = True
        elif project["streaming"] == False:
            project["running"] = False

        insert_project = db_table_projects.insert().values(
            id = project["uuid"],
            name = project["name"],
            description = project["description"],
            creationdate = project["creationdate"],
            use_twitter = project["use_twitter"],
            use_oalex = project["use_oalex"],
            use_scopus = project["use_scopus"],
            use_arxiv = project["use_arxiv"],
            streaming = project["streaming"],
            startdate = project["startdate"],
            enddate = project["enddate"],
            running = project["running"],
            crawl_frequency = project["crawl_frequency"]
        )
        result = connection.execute(insert_project)

        project_created = True
    except Exception as e:
        project_created = False
        result = ""
    return project_created, result


def list_projects():
    db_table_projects = st.session_state.db_table_projects
    connection = st.session_state.db_connection

    #list_of_projects = connection.execute(select(db_table_projects))
    list_of_projects = []
    for u in connection.execute(select(db_table_projects)):
        list_of_projects.append(u._asdict())

    return list_of_projects

def create_twitter_query(id, tw_query):
    tw_query_created = False
    db_table_twitter_crawls = st.session_state.db_table_twitter_crawls
    connection = st.session_state.db_connection
    
    try:
        insert_twitter_crawl = db_table_twitter_crawls.insert().values(
            projectid = id,
            query = tw_query["query"],
            ext_query = tw_query["ext_query"],
            last_crawl = str(dt.now().date()),
            tweet_limit = tw_query["limit"],
            min_replies = tw_query["min_replies"],
            min_retweets = tw_query["min_retweets"],
            min_likes = tw_query["min_faves"],
            date_from = str(rel_to_abs_date(tw_query["days_ago"])[0]),
            date_to = tw_query["date_to"],
            excl_replies = tw_query["exclude_replies"],
            excl_retweets = tw_query["exclude_retweets"]
        )
        result = connection.execute(insert_twitter_crawl)

        tw_query_created = True
    except Exception as e:
        tw_query_created = False
        st.write(e)
        result = ""
    return tw_query_created, result

def get_twitter_query(uuid):
    db_session = st.session_state.db_session
    db_table_twitter_crawls = st.session_state.db_table_twitter_crawls

    query_exists = False
    search_params = {}
    
    query_exists = db_session.query(db_table_twitter_crawls).filter_by(projectid=uuid).first() is not None
    if query_exists:
        search_params = (db_session.query(db_table_twitter_crawls).filter_by(projectid=uuid).first())._asdict()
    return query_exists, search_params