import streamlit as st
import json
from tinydb import TinyDB, Query
import re
import os
from modules.ingest_docs import search_db, file_name_db, ingest_document_prototype, get_scrapp_db, ingest_document_prototype3,download_webpage_html
from rapidfuzz import fuzz
import uuid
import base64
from streamlit_searchbox import st_searchbox

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




def get_fonted_text(text,size=24, body=False):
    extra = "letter-spacing: -2px;"

    if body==True:
        extra = ""
    
    return f'<p style="font-family: \'DepartureMono\', monospace; font-size: {size}px;{extra}">{text}</p>'
def search_page():
    st.markdown(font_info, unsafe_allow_html=True)

    st.markdown(get_fonted_text("Entity Search", size=48), unsafe_allow_html=True)
    # Add custom CSS to load the font

    from modules.db import search_db, search_db_id  

    def get_suggestions(searchterm: str) -> list[any]:
        if searchterm == "":
            return []
        all_subjects = [x['metadata']['subject'] for x in search_db_id(searchterm,n_results=10)]
        return all_subjects if searchterm else []

    search_term = st_searchbox(
        get_suggestions,
        key="searchbox",
    )

    if search_term and st.button("GO"):
        results = search_db(search_term)
        if results:
            st.markdown(get_fonted_text("Search Results",size=24,body=True), unsafe_allow_html=True)


            texts = results 
            images = ["https://via.placeholder.com/150"] * len(results)

            for label in results:
                col1, col2  = st.columns([2, 1])

                with col1:
                    # st.write(f"{label} clicked!")
                    st.markdown(get_fonted_text(f"\"{label[0]}\"",size=16,body=True), unsafe_allow_html=True)

                    # if st.button(label[0]):
                    #     st.write(f"{label} clicked!")

                with col2:
                    file_info = file_name_db.get(Query().doc_id == label[1])['metadata']
                    del file_info["file_size"]
                    del file_info["modification_time"]

                    source = file_info['file_name']

                    if "url" in file_info.keys():
                        source = file_info['url']
                    
                    # st.write(f"File Name: \"{file_info['file_name']}\"")
                    # st.write(f"Collection Time: {file_info['creation_time']}")
                    # st.write(f"Source: {source}")

                    st.markdown(get_fonted_text(f"File Name: \"{file_info['file_name']}\"",size=16,body=True), unsafe_allow_html=True)
                    st.markdown(get_fonted_text(f"Collection Time: {file_info['creation_time']}",size=16,body=True), unsafe_allow_html=True)
                    st.markdown(get_fonted_text(f"Source: {source}",size=16,body=True), unsafe_allow_html=True)
                # with col3:
                #     st.write("NEEd to add deleting")
                #     if st.button("Delete", key=uuid.uuid4()):
                #         st.success(f"Deleted entry: {label[0]}")




                st.markdown("---")
        else:
            st.info("No results found.")

def upload_page():

    # st.title("File Upload")
    st.markdown(get_fonted_text("File Upload",size=48), unsafe_allow_html=True)
    st.markdown(get_fonted_text("Upload files to the DB",body=True), unsafe_allow_html=True)
    # st.markdown("<a href="file:///C:\Programs\sort.mw">Link 1</a>")

    uploaded_files = st.file_uploader("", type=None, accept_multiple_files=True)
        
    from modules.ingest_docs import read_file_with_metadata
    # st.markdown(font_info, unsafe_allow_html=True)

    if st.button("Go", disabled=st.session_state.ingesting):
        st.session_state.ingesting = True
        if uploaded_files is not None:
            for uploaded_file in uploaded_files:
                save_path = os.path.join(SAVE_DIR, uploaded_file.name)
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                # read_file_with_metadata(save_path)
                with st.spinner('Ingesting...'):
                    metadata = ingest_document_prototype3(save_path)
                st.success("Ingested!")
                # st.sucess(metadata)
import validators

def webcrawl_page():
    url = st.text_input("Enter URL")
    file_path = None
    if validators.url(url):
        if st.button("Go", disabled=st.session_state.ingesting):
            file_path = download_webpage_html(url)
    else:
        st.text("Invalid URL")
    # uploaded_files = st.file_uploader("", type=None, accept_multiple_files=True)
        
    # from modules.ingest_docs import read_file_with_metadata
    # # st.markdown(font_info, unsafe_allow_html=True)
    if file_path is not None:
        st.session_state.ingesting = True
        with st.spinner('Ingesting...'):
            metadata = ingest_document_prototype3(file_path, url=url)

        st.success("Ingested!")
        st.success(metadata)
page_names_to_funcs = {
    "Search": search_page,
    "Upload Files": upload_page,
    "Download Websites": webcrawl_page
}

def main():
    st.markdown(font_info, unsafe_allow_html=True)

    # st.sidebar.title("Navigation")
    st.sidebar.markdown(get_fonted_text("Navigation",body=True), unsafe_allow_html=True)

    page_name = st.sidebar.radio("Go to", list(page_names_to_funcs.keys()))
    page_names_to_funcs[page_name]()

if __name__ == "__main__":
    main()