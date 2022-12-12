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

# For Postgres DB Connection
from sqlalchemy import create_engine, schema, insert, MetaData, Table, Column, Integer, String, VARCHAR, Date, Boolean, select
from sqlalchemy.dialects.postgresql import UUID


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

    if 

    try:
        conn_str = "postgresql://" + postgres_cred["db_user"] + ":" + postgres_cred["db_password"] + "@" + postgres_cred["host"] + ":" + str(postgres_cred["port"]) + "/" + postgres_cred["db_name"]

        engine = create_engine(conn_str)
        connection = engine.connect()

        meta = MetaData()

        db_connection = True
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
            meta.create_all(engine)

            # OpenALEX Services
            # tbc

            # Scopus Services
            # tbc

            # arXiv Services
            # tbc


            services_created = True
        except Exception as e:
            print(e)
            services_created = False    

    return db_connection, schema_created, project_created, services_created

def list_projects():
    stmt = select("projects").where()
    list_of_projects = 
    return list_of_projects

def schema_init(connection, schema_name):
    schema_created = False
    
    try:
        if schema_name not in connection.dialect.get_schema_names(connection):
            connection.execute(schema.CreateSchema(schema_name))
        schema_created = True
    except Exception as e:
        schema_created = False

    return schema_created

def project_init(project, db, connection):
    project_created = False
    
    try:
        project["uuid"] = uuid.uuid4()
        if project["streaming"]:
            project["running"] = True
        elif project["streaming"] == False:
            project["running"] = False

        meta = MetaData()

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
        meta.create_all(db)
        # db.execute("CREATE TABLE IF NOT EXISTS " + schema_name + ".projects (id uuid NOT NULL, name varchar(100) NOT NULL, description varchar(255), creationdate date NOT NULL, use_twitter boolean DEFAULT FALSE NOT NULL, use_oalex boolean DEFAULT FALSE NOT NULL, use_scopus boolean DEFAULT FALSE NOT NULL, use_arxiv boolean DEFAULT FALSE NOT NULL, streaming boolean DEFAULT FALSE NOT NULL, startdate date, enddate date, running boolean, crawl_frequency char(50), CONSTRAINT pk_projects PRIMARY KEY ( id ))")
        
        insert_project = projects.insert().values(
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
        # db.execute("INSERT INTO " + schema_name + ".projects (id, name, description, creationdate, use_twitter, use_oalex, use_scopus, use_arxiv, streaming, startdate, enddate, running, crawl_frequency) VALUES(" + str(project["uuid"]) + "," + project["name"] + "," + project["description"] + "," + str(project["creationdate"]) + "," + str(project["use_twitter"]) + "," + str(project["use_oalex"]) + "," + str(project["use_scopus"]) + "," + str(project["use_arxiv"]) + "," + str(project["streaming"]) + "," + str(project["startdate"]) + "," + str(project["enddate"]) + "," + str(project["running"]) + "," + project["crawl_frequency"] + ")")

        project_created = True
    except Exception as e:
        project_created = False
        result = ""
    return project_created, result

