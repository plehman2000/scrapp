import streamlit as st
import json
from tinydb import TinyDB, Query
import re
import os
from rapidfuzz import fuzz
import uuid
import base64
from streamlit_searchbox import st_searchbox
from prover import prover

st.session_state.title = "Prover"
SAVE_DIR = "./documents/"


def load_font(font_file):
    with open(font_file, "rb") as f:
        font_bytes = f.read()
    return base64.b64encode(font_bytes).decode()


# Load the font files
woff2_font = load_font("./.streamlit/font/DepartureMono-Regular.woff2")
woff_font = load_font("./.streamlit/font/DepartureMono-Regular.woff")
otf_font = load_font("./.streamlit/font/DepartureMono-Regular.otf")

font_info = f"""
    <style>
    @font-face {{
    font-family: 'DepartureMono';
    src: url(data:font/woff2;charset=utf-8;base64,{woff2_font}) format('woff2'),
        url(data:font/woff;charset=utf-8;base64,{woff_font}) format('woff'),
        url(data:font/otf;charset=utf-8;base64,{otf_font}) format('opentype');
    font-weight: normal;

    font-style: normal;
    }}

    html, body, [class*="css"] {{
    font-family: 'DepartureMono', monospace !important;
    }}
    </style>
    """


def get_fonted_text(text, size=24, body=False):
    extra = "letter-spacing: -2px;"

    if body == True:
        extra = ""

    return f"<p style=\"font-family: 'DepartureMono', monospace; font-size: {size}px;{extra}\">{text}</p>"


def prover_page():
    st.markdown(font_info, unsafe_allow_html=True)

    st.markdown(get_fonted_text("Prover", size=48), unsafe_allow_html=True)
    # Add custom CSS to load the font


    def process_text(text):
    # Replace this with your desired processing function
        return f"You entered: {text}"

    # Create text input that captures Enter key
    claim = st.text_input("Enter your provable claim:", key="text_input", 
                    on_change=None, args=None, kwargs=None)

    # Check if Enter was pressed (when text_input has a value and Enter is hit)
    opposition_claim = None

    if claim:
        out = None
        for x in prover(claim, use_small_model=True):
            # out = x
            #calculate difference between out andx
            # if "opposition_claim" in out:
            #     st.write(x['opposition_claim'])
            st.markdown(get_fonted_text(x['status'], size=16), unsafe_allow_html=True)
        arg1_w_claims = x['arg1_w_claims']
        arg2_w_claims = x['arg2_w_claims']
        st.write(arg1_w_claims, arg2_w_claims)
        st.markdown(get_fonted_text(f"Winning Claim: {x['victor']}", size=48), unsafe_allow_html=True)


    st.session_state.title = "Prover"
 

page_names_to_funcs = {
    # "History": history_page,
    "Prover": prover_page,
}


def main():
    st.markdown(font_info, unsafe_allow_html=True)

    # st.sidebar.title("Navigation")
    st.sidebar.markdown(
        get_fonted_text("Navigation", body=True), unsafe_allow_html=True
    )

    page_name = st.sidebar.radio("Go to", list(page_names_to_funcs.keys()))
    page_names_to_funcs[page_name]()


if __name__ == "__main__":
    main()
