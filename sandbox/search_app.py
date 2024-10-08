import streamlit as st
import json
from tinydb import TinyDB, Query
import re
import os
from modules.ingest_docs import (
    search_db,
    file_name_db,
    ingest_document_prototype,
    get_scrapp_db,
    ingest_document_prototype3,
    download_webpage_html,
)
from rapidfuzz import fuzz
import uuid
import base64
from streamlit_searchbox import st_searchbox
from modules.scrapper import extract_info

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


def search_page():
    st.markdown(font_info, unsafe_allow_html=True)

    st.markdown(get_fonted_text("Entity/Facts Search", size=48), unsafe_allow_html=True)
    # Add custom CSS to load the font

    scrapp_copy = get_scrapp_db()
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


def upload_page():
    if 'facts' not in st.session_state:
        st.session_state.facts = []
    # st.title("File Upload")
    st.markdown(get_fonted_text("File Upload", size=48), unsafe_allow_html=True)
    st.markdown(
        get_fonted_text("Upload files to the DB", body=True), unsafe_allow_html=True
    )
    # st.markdown("<a href="file:///C:\Programs\sort.mw">Link 1</a>")
    uploaded_files = st.file_uploader("", type=None, accept_multiple_files=True)

    st.markdown(get_fonted_text("Or, enter a URL", body=True), unsafe_allow_html=True)
    url = st.text_input("")
    file_path = None
    if validators.url(url):
        if st.button("Go", disabled=st.session_state.ingesting):
            file_path = download_webpage_html(url)
    elif url:
        st.text("Invalid URL")
    # from modules.ingest_docs import read_file_with_metadata

    filtered_facts = None
    if st.button("Go", disabled=st.session_state.ingesting):
        st.session_state.ingesting = True
        if uploaded_files is not None:
            for uploaded_file in uploaded_files:
                save_path = os.path.join(SAVE_DIR, uploaded_file.name)
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                # read_file_with_metadata(save_path)
                with st.spinner("Ingesting..."):
                    filtered_facts = ingest_document_prototype3(save_path)
                    # filtered_facts = {
                    #     "facts": [
                    #         {
                    #             "subject": "The original Pali word for this training",
                    #             "predicate": "is sila.",
                    #         },
                    #         {
                    #             "subject": "People",
                    #             "predicate": "translate the term in various ways.",
                    #         },
                    #         {
                    #             "subject": "Living a good life in the conventional sense",
                    #             "predicate": "involves honing one's moral compass through sila training.",
                    #         },
                    #         {
                    #             "subject": "Enhancing physical, emotional, and mental health through self-care",
                    #             "predicate": "also entails engaging in sila training.",
                    #         },
                    #         {
                    #             "subject": "Delving into philosophy",
                    #             "predicate": "falls within the sphere of sila training.",
                    #         },
                    #         {
                    #             "subject": "Engaging in regular exercise",
                    #             "predicate": "can be viewed as partaking in sila training.",
                    #         },
                    #     ]
                    # }
                st.success("Ingested!")
                st.session_state.facts = filtered_facts

                # Addl logic here to remove junk subjects/facts

                # Display facts with toggles

                # st.sucess(metadata)
        elif file_path is not None:
            st.session_state.ingesting = True
            with st.spinner("Ingesting..."):
                metadata = ingest_document_prototype3(file_path, url=url)

            st.success("Ingested!")
            st.sucess(metadata)

    # if filtered_facts:
    #     idx_to_delete = []
    #     for i, fact in enumerate(filtered_facts):
    #         col1, col2, col3 = st.columns([2, 1, 1])

    #         with col3:
    #             tgg = st.toggle("Delete", key=str(uuid.uuid4()))
    #             if tgg:
    #                 idx_to_delete.append(i)
    #             else:
    #                 if i in set(idx_to_delete):
    #                     idx_to_delete.remove(i)
    #         with col1:
    #             st.write(fact["subject"] + ": " + fact["predicate"])

        # # Add to DB button
        # if st.button("Add to DB"):
        #     # Remove facts marked for deletion
        #     # st.session_state.facts = [
        #     #     fact
        #     #     for i, fact in enumerate(st.session_state.facts["facts"])
        #     #     if i not in idx_to_delete
        #     # ]
        #     st.success("Facts updated!")
        #     st.write(st.session_state.facts)
        #     add_facts_to_db(st.session_state.facts['facts'])


import validators


def webcrawl_page():
    url = st.text_input("Enter URL")
    # file_path = None
    # if validators.url(url):
    #     if st.button("Go", disabled=st.session_state.ingesting):
    #         file_path = download_webpage_html(url)
    # elif url:
    #     st.text("Invalid URL")
    # # uploaded_files = st.file_uploader("", type=None, accept_multiple_files=True)

    # # from modules.ingest_docs import read_file_with_metadata
    # # # st.markdown(font_info, unsafe_allow_html=True)
    # if file_path is not None:
    #     st.session_state.ingesting = True
    #     with st.spinner('Ingesting...'):
    #         metadata = ingest_document_prototype3(file_path, url=url)

    #     st.success("Ingested!")
    #     st.sucess(metadata)


def combine_page():
    st.markdown(font_info, unsafe_allow_html=True)

    if "entries_to_combine" not in st.session_state:
        st.session_state.entries_to_combine = []

    if "selected_toggles" not in st.session_state:
        st.session_state.selected_toggles = set()

    st.markdown(get_fonted_text("Combine Facts", size=48), unsafe_allow_html=True)

    def get_ent_suggestions(searchterm: str) -> list[any]:
        all_subjects = sorted(
            ent_suggestions,
            key=lambda x: fuzz.partial_ratio(searchterm, x[1]),
            reverse=True,
        )[:8]
        return all_subjects if searchterm else []

    scrapp_copy = get_scrapp_db()
    ent_suggestions = [doc["subject"] for doc in scrapp_copy]
    ent_suggestions = [x for x in ent_suggestions if x != ""]

    print("Entity SEARCH")
    st.session_state.title = "Entity Search"

    search_term = st_searchbox(
        get_ent_suggestions,
        key="searchbox",
    )
    results = json.loads(search_db(search_term))["facts"]

    top_container = st.container()
    if search_term:
        if results:
            st.markdown(
                get_fonted_text("Search Results", size=24, body=True),
                unsafe_allow_html=True,
            )

            for label in results:
                col1, col2, col3 = st.columns([3, 2, 1])

                with col1:
                    st.markdown(
                        get_fonted_text(f'"{label[0]}"', size=16, body=True),
                        unsafe_allow_html=True,
                    )

                with col2:
                    file_info = file_name_db.get(Query().doc_id == label[1])["metadata"]
                    del file_info["file_size"]
                    del file_info["modification_time"]

                    source = file_info["file_name"]
                    if "url" in file_info.keys():
                        source = file_info["url"]

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

                with col3:
                    # Create a unique key for each search term and result combination
                    toggle_key = f"toggle_{search_term}_{label[1]}"
                    add_str = f"{search_term}: {label[0]}"

                    if st.toggle(
                        "Select",
                        key=toggle_key,
                        value=st.session_state.selected_toggles[toggle_key],
                    ):
                        st.session_state.selected_toggles[toggle_key] = True
                        if add_str not in st.session_state.entries_to_combine:
                            st.session_state.entries_to_combine.append(add_str)
                            st.session_state.selected_toggles.add(toggle_key)
                    else:
                        st.session_state.selected_toggles[toggle_key] = False
                        if add_str in st.session_state.entries_to_combine:
                            st.session_state.entries_to_combine.remove(add_str)
                            st.session_state.selected_toggles.discard(toggle_key)

                st.markdown("---")
        else:
            st.info("No results found.")

    if st.button("Clear All Selections"):
        st.session_state.entries_to_combine = []
        st.session_state.selected_toggles = set()
    with top_container:
        st.markdown(
            get_fonted_text("Current selections:", size=24), unsafe_allow_html=True
        )
        for i, item in enumerate(st.session_state.entries_to_combine):
            st.write(f"{i+1}. " + item)


page_names_to_funcs = {
    "Combine": combine_page,
    "Search": search_page,
    "Upload Files": upload_page,
    "Download Websites": webcrawl_page,
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
