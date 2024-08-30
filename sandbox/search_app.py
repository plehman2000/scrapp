import streamlit as st
import json
from tinydb import TinyDB, Query
import re
import os
from modules.ingest_docs import search_db, file_name_db,ingest_document_prototype, get_scrapp_db
from rapidfuzz import fuzz
import uuid

SAVE_DIR = "./documents/"
st.session_state.ingesting = False

def search_page():
    st.title("Database Search App")

    # search_term = st.text_input("Enter search term here")
    from streamlit_searchbox import st_searchbox

    # function with list of labels
    suggestions = get_scrapp_db()

    def get_suggestions(searchterm: str) -> list[any]:
        all_subjects = sorted(suggestions, key=lambda x: fuzz.partial_ratio(searchterm,x), reverse=True)[:5]
        return all_subjects if searchterm else []


    # pass search function to searchbox
    search_term = st_searchbox(
        get_suggestions,
        key="searchbox",
    )

    if search_term:
        results = search_db(search_term)
        results = [x[0] for x in json.loads(results)['facts']]
        if results:
            st.subheader("Search Results:")
            # Display buttons and check which one was clicked
            for label in results:
                if st.button(label, key=uuid.uuid4()):

                    st.write(f"You clicked: {label}")
        else:
            st.info("No results found.")

def upload_page():
    
    st.title("File Upload")
    st.write("Upload files to the DB")

    uploaded_files = st.file_uploader("Choose a file", type=None, accept_multiple_files=True)
        
        
    from modules.ingest_docs import read_file_with_metadata
    if st.button("Ingest", disabled=st.session_state.ingesting):
        st.session_state.ingesting = True
        if uploaded_files is not None:
            for uploaded_file in uploaded_files:
                save_path = os.path.join(SAVE_DIR, uploaded_file.name)
                
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                read_file_with_metadata(save_path)
                with st.spinner('Ingesting...'):
                    ingest_document_prototype(save_path)
                st.success("Ingested!")


page_names_to_funcs = {
    "Search": search_page,
    "Upload Files": upload_page
}

def main():
    st.sidebar.title("Navigation")
    page_name = st.sidebar.radio("Go to", list(page_names_to_funcs.keys()))
    page_names_to_funcs[page_name]()

if __name__ == "__main__":
    main()