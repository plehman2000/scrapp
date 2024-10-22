import streamlit as st
import json
from tinydb import TinyDB, Query
import re
import os
from rapidfuzz import fuzz
import uuid
import base64
from streamlit_searchbox import st_searchbox

st.session_state.title = "Entity Search"
SAVE_DIR = "./documents/"
st.session_state.ingesting = False


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

    st.markdown(get_fonted_text("Entity/Facts Search", size=48), unsafe_allow_html=True)
    # Add custom CSS to load the font

    ent_suggestions = [doc["subject"] for doc in scrapp_copy]
    ent_suggestions = [x for x in ent_suggestions if x != ""]
    print(ent_suggestions)
    from scipy import spatial

    def get_ent_suggestions(searchterm: str) -> list[any]:
        all_subjects = sorted(
            ent_suggestions,
            key=lambda x: fuzz.partial_ratio(searchterm, x[1]),
            reverse=True,
        )[:8]
        return all_subjects if searchterm else []

    # fact_suggestions = [[[doc['subject'] + " " + str(x[0]), 1] for x in doc['facts']] for doc in scrapp_copy]
    # def get_fact_suggestions(searchterm: str) -> list[any]:
    #     all_subjects = sorted(fact_suggestions, key=lambda x: fuzz.partial_ratio(searchterm,x), reverse=True)[:8]
    #     return all_subjects if searchterm else []

    print("Entity SEARCH")
    st.session_state.title = "Entity Search"

    search_term = st_searchbox(
        get_ent_suggestions,
        key="searchbox",
    )
    results = json.loads(search_db(search_term))["facts"]

    if search_term:
        if results:
            st.markdown(
                get_fonted_text("Search Results", size=24, body=True),
                unsafe_allow_html=True,
            )

            texts = results
            images = ["https://via.placeholder.com/150"] * len(results)

            for label in results:
                col1, col2 = st.columns([2, 1])

                with col1:
                    # st.write(f"{label} clicked!")
                    st.markdown(
                        get_fonted_text(f'"{label[0]}"', size=16, body=True),
                        unsafe_allow_html=True,
                    )

                    # if st.button(label[0]):
                    #     st.write(f"{label} clicked!")

                with col2:
                    file_info = file_name_db.get(Query().doc_id == label[1])["metadata"]
                    del file_info["file_size"]
                    del file_info["modification_time"]

                    source = file_info["file_name"]

                    if "url" in file_info.keys():
                        source = file_info["url"]

                    # st.write(f"File Name: \"{file_info['file_name']}\"")
                    # st.write(f"Collection Time: {file_info['creation_time']}")
                    # st.write(f"Source: {source}")

                    st.markdown(
                        get_fonted_text(
                            f"File Name: \"{file_info['file_name']}\"",
                            size=16,
                            body=True,
                        ),
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        get_fonted_text(
                            f"Collection Time: {file_info['creation_time']}",
                            size=16,
                            body=True,
                        ),
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        get_fonted_text(f"Source: {source}", size=16, body=True),
                        unsafe_allow_html=True,
                    )
                    # st.markdown(get_fonted_text(f"Embedding: {label[2]}",size=16,body=True), unsafe_allow_html=True)
                # with col3:
                #     st.write("NEEd to add deleting")
                #     if st.button("Delete", key=uuid.uuid4()):
                #         st.success(f"Deleted entry: {label[0]}")

                st.markdown("---")
        else:
            st.info("No results found.")

page_names_to_funcs = {
    "History": history_page,
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
