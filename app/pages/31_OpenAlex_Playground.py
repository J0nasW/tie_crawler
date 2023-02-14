###
# OpenAlex Playground
#
###

import streamlit as st
import pandas as pd
from pyalex import Works, Authors, Venues, Institutions, Concepts
import pyalex
pyalex.config.email = "jonas.wilinski@tuhh.de"

import matplotlib.pyplot as plt

from collections import defaultdict

import networkx as nx


### STREAMLIT Init:

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="OpenAlex playground", page_icon="🔎")

if st.button("Works highest cited"):
    works = (Works() \
    .filter(concepts={"id": "C41008148"}, publication_year=2018) \
    .sort(cited_by_count="desc") \
    .get())

    works_df = pd.DataFrame(works)

    st.write(works_df.head(10))


title_search = st.text_input("Title Search")
if title_search:
    works = (Works() \
    .search_filter(title="*"+title_search+"*") \
    .get())

    works_df = pd.DataFrame(works)

    st.write(works_df.head(10))
    works_dict = works_df.head(10).to_dict(orient="records")
    st.write(works_dict)

    for work in works_dict:
        st.write(work["title"])
        st.write(work["referenced_works"])
        st.write(work["related_works"])


work_list = st.text_area("Work List (separate with comma, group with semicolon)", placeholder="W1097231, W1097232, W1097233, ...")

works_cleaned = {}

if work_list:
    work_groups = work_list.split("; ")

    for work in work_groups:
        works = (Works()[work.split(", ")])
        #st.write(works)

        work_group_name = works[0]["title"]
        
        works_df = pd.DataFrame(works)

        works_cleaned[work_group_name] = {
            "ids": works_df["id"].tolist(),
            "dois": works_df["doi"].drop_duplicates().reset_index(drop=True).tolist(),
            "publication_year": works_df["publication_year"].drop_duplicates().reset_index(drop=True).tolist(),
            "authorships": works_df["authorships"].drop_duplicates().reset_index(drop=True).tolist(),
            "concepts": works_df["concepts"].drop_duplicates().reset_index(drop=True).tolist(),
            "referenced_works": works_df["referenced_works"].drop_duplicates().reset_index(drop=True).tolist(),
            "related_works": works_df["related_works"].drop_duplicates().reset_index(drop=True).tolist(),
            "cited_by_api_url": works_df["cited_by_api_url"].drop_duplicates().reset_index(drop=True).tolist(),
            "cited_by_count": works_df["cited_by_count"].sum(),
            "counts_by_year": works_df["counts_by_year"].drop_duplicates().reset_index(drop=True).tolist(),
        }

        # Merging counts_by_year
        sum_dict = defaultdict(int)
        for year_data in works_cleaned[work_group_name]["counts_by_year"]:
            for d in year_data:
                sum_dict[d['year']] += d['cited_by_count']
        works_cleaned[work_group_name]["counts_by_year"] = [{"year": k, "cited_by_count": v} for k, v in sum_dict.items()]

        # Merging referenced works and getting rid of duplicates
        referenced_works = []
        for referenced_works_data in works_cleaned[work_group_name]["referenced_works"]:
            for d in referenced_works_data:
                referenced_works.append(d)
        works_cleaned[work_group_name]["referenced_works"] = list(set(referenced_works))

        # Merging related works
        related_works = []
        for related_works_data in works_cleaned[work_group_name]["related_works"]:
            for d in related_works_data:
                related_works.append(d)
        works_cleaned[work_group_name]["related_works"] = list(set(related_works))

        # Merging concepts dict and getting rid of duplicates
        concept_dict = defaultdict(dict)
        for concept_data in works_cleaned[work_group_name]["concepts"]:
            for d in concept_data:
                concept_dict[d['id']].update(d)
        works_cleaned[work_group_name]["concepts"] = list(concept_dict.values())

        works_cleaned_df = pd.DataFrame(works_cleaned)

    with st.expander("Works", expanded=False):
        st.write(works_cleaned_df)

    with st.expander("Custom Names for Work Groups", expanded=False):
        with st.form("Name the work groups"):
            for work_group in works_cleaned:
                works_cleaned[work_group]["name"] = st.text_input(work_group, value=work_group)
            submit_button = st.form_submit_button(label='Submit')

    with st.expander("Cites per Year Plots", expanded=True):
        # Plot counts_by_year of all works in a 2x2 grid as bar plots and with the custom name, x-axis is year, y-axis is count
        fig, axs = plt.subplots(2, 2)
        fig.set_size_inches(18.5, 10.5)
        fig.suptitle('Counts by year')
        for i, work_group in enumerate(works_cleaned):
            axs[i%2, i//2].bar([d["year"] for d in works_cleaned[work_group]["counts_by_year"]], [d["cited_by_count"] for d in works_cleaned[work_group]["counts_by_year"]])
            axs[i%2, i//2].set_title(works_cleaned[work_group]["name"])
            axs[i%2, i//2].set(xlabel='Year', ylabel='Cited by count')
        st.pyplot(fig)

        # Plot counts_by_year of all works combined as one bar plot, x-axis is year, y-axis is count
        fig, ax = plt.subplots()
        fig.set_size_inches(18.5, 10.5)
        fig.suptitle('Counts by year')
        for work_group in works_cleaned:
            ax.bar([d["year"] for d in works_cleaned[work_group]["counts_by_year"]], [d["cited_by_count"] for d in works_cleaned[work_group]["counts_by_year"]], label=works_cleaned[work_group]["name"])
        ax.set(xlabel='Year', ylabel='Cited by count')
        ax.legend()
        st.pyplot(fig)

    with st.expander("Concepts and their scores", expanded=True):
        st.write("Concepts and their scores are plotted as a network graph. The size of the node is proportional to the score of the concept. Note: Concepts with a score less than 0.2 are not plotted.")
        # Plot the work and its concepts of all works using networkx as separate plots, node size is proportional to score, node color is proportional to level, node shape is square for work and circle for concept
        for work_group in works_cleaned:
            G = nx.Graph()

            # Draw the center point (WORK)
            G.add_node(work_group,
                label=works_cleaned[work_group]["name"],
                level=0,
                score=1,
                color="blue",
                size=1000,
                shape="s",
                style="filled",
                fillcolor="red",
                font_color="white",
                font_size=14,
                font_weight="bold"
            )

            # Draw the concepts
            for concept in works_cleaned[work_group]["concepts"]:
                if float(concept["score"]) > 0.2:
                    # print(concept["score"])
                    G.add_node(concept["id"],
                        label=concept["display_name"],
                        level=concept["level"],
                        score=float(concept["score"]),
                        color="lightblue",
                        size=float(concept["score"])*2000,
                        shape=".",
                        style="filled",
                        fillcolor="blue",
                        font_color="black",
                        font_size=10,
                        font_weight="regular"
                    )
                    G.add_edge(
                        work_group,
                        concept["id"],
                        weight=float(concept["score"]),
                    )
            fig, ax = plt.subplots(figsize=(10,8))
            fig.suptitle('Concepts')

            # Layout
            pos = nx.spring_layout(G,
                k=0.3,
                iterations=20,
                seed=42,
                scale=1,
                center=(0,0),
                dim=2,
                weight="weight",
                pos=None,
                fixed=None,
                threshold=0.0001
            )

            # Draw lables
            labels = nx.get_node_attributes(G, 'label')
            text_objects = nx.draw_networkx_labels(
                G,
                pos,
                labels=labels,
                font_color="black",
                font_weight="regular",
                font_family="sans-serif",
                ax=None,
                horizontalalignment="center",
                verticalalignment="center",
                clip_on=True)
            
            for node, text_obj in text_objects.items():
                #text_obj.set_position((pos[node][0], pos[node][1] + 0.06))
                text_obj.set_alpha(G.nodes[node]["score"])
                text_obj.set_bbox(dict(boxstyle='round', facecolor=G.nodes[node]["color"], alpha=G.nodes[node]["score"]))
                text_obj.set_fontsize(G.nodes[node]["font_size"])
                text_obj.set_fontweight(G.nodes[node]["font_weight"])
                text_obj.set_color(G.nodes[node]["font_color"])

            # Draw nodes
            # nx.draw_networkx_nodes(
            #     G,
            #     pos,
            #     ax=ax,
            #     node_color=[d[1]["color"] for d in G.nodes(data=True)],
            #     node_size=[d[1]["size"] for d in G.nodes(data=True)],
            #     #node_shape=[d[1]["shape"] for d in G.nodes(data=True)]
            #     node_shape=".",
            #     alpha=[d[1]["score"] for d in G.nodes(data=True)],
            # )
            
            # Draw edges
            nx.draw_networkx_edges(
                G,
                pos,
                ax=ax,
                width=[d[2]["weight"] for d in G.edges(data=True)]*100,
                alpha=[d[2]["weight"] for d in G.edges(data=True)],
                arrows=True,
                arrowsize=10,
                arrowstyle="-|>",
                connectionstyle="arc3,rad=0.1"
            )

            plt.tight_layout()
            plt.margins(x=0.1)

            st.pyplot(fig)
    
    with st.expander("Cites", expanded=True):
        # Display all referenced works of all works in a dataframe and crawl these works from OpenAlex API using pyAlex
        st.write("Cites are displayed as a dataframe. The dataframe is sorted by the number of times the work is cited by other works.")
        for work in works_cleaned:
            st.write(work["referenced_works"])
            #cited_works = (Works()[work["referenced_works"]])
            #st.write(cited_works)
            break    
    
        # Display all referenced works of all works in a dataframe and crawl these works from OpenAlex API using pyAlex







