####################################################################################
# Helper Functions
# by JW
#
# A collection of helper functions
# 
# helpers / helper_functions.py
####################################################################################

# IMPORT STATEMENTS ----------------------------------------------------------------
import datetime

# Streamlit Web App
import streamlit as st


def rel_to_abs_date(days):
    if days == None:
        return (datetime.date(day=1, month=1, year=1970),)
    return datetime.date.today() - datetime.timedelta(days=days)

def display_dict(dict):
    for k, v in dict.items():
        a, b = st.columns([1, 4])
        a.write(f"**{k}:**")
        b.write(v)

def paginator(values, state_key, page_size, btn_key_next, btn_key_prev):
    curr_page = getattr(st.session_state, state_key)

    a, b, c = st.columns(3)

    def decrement_page():
        curr_page = getattr(st.session_state, state_key)
        if curr_page > 0:
            setattr(st.session_state, state_key, curr_page - 1)

    def increment_page():
        curr_page = getattr(st.session_state, state_key)
        if curr_page + 1 < len(values) // page_size:
            setattr(st.session_state, state_key, curr_page + 1)

    def set_page(new_value):
        setattr(st.session_state, state_key, new_value - 1)

    a.write(" ")
    a.write(" ")
    a.button("Previous page", on_click=decrement_page, key=btn_key_next)

    b.write(" ")
    b.write(" ")
    b.button("Next page", on_click=increment_page, key=btn_key_prev)

    c.selectbox(
        "Select a page",
        range(1, len(values) // page_size + 1),
        curr_page,
        on_change=set_page,
    )

    curr_page = getattr(st.session_state, state_key)

    page_start = curr_page * page_size
    page_end = page_start + page_size

    return values[page_start:page_end]