import os
import datetime
from .scrapper import text_to_relations
from tinydb import TinyDB, Query
from tqdm import tqdm
import uuid
import ollama
from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep


global scrapp_db
global file_name_db
scrapp_db = TinyDB("./databases/scrapps_db.json")
file_name_db = TinyDB("./databases/files_db.json")


class Loader:
    def __init__(self, desc="Loading...", end="Done!", timeout=0.1):
        """
        A loader-like context manager

        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            end (str, optional): Final print. Defaults to "Done!".
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
        """
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()


def read_file_with_metadata(file_path, url=None):
    result = {}

    # Get file metadata
    file_stats = os.stat(file_path)
    result["metadata"] = {
        "file_name": os.path.basename(file_path),
        "file_size": file_stats.st_size,
        "creation_time": datetime.datetime.fromtimestamp(
            file_stats.st_ctime
        ).isoformat(),
        "modification_time": datetime.datetime.fromtimestamp(
            file_stats.st_mtime
        ).isoformat(),
        # 'access_time': datetime.datetime.fromtimestamp(file_stats.st_atime).isoformat(),
    }

    if url is not None:
        result["metadata"]["source"] = url
    return result


#:now to combine the relations based on the same subjects, thwen storee the docs and scrapps
def db_ready_facts(relations, doc_id):
    filtered_facts = {}
    for temp_facts in relations:
        temp_facts = temp_facts["facts"]

        for x in temp_facts:
            embedding = ollama.embeddings(model="nomic-embed-text", prompt=x["subject"] + " " + x["predicate"])["embedding"]

            if x["subject"] not in filtered_facts:
                filtered_facts[x["subject"]] = []
            filtered_facts[x["subject"]].append([x["predicate"], doc_id, embedding])
    return filtered_facts


def ingest_document_prototype(file_path):  # need to add work for using webpages
    global scrapp_db
    global file_name_db
    # Read file and process content
    file_info = read_file_with_metadata(file_path)
    # add source like URL or title
    doc_id = str(uuid.uuid4())
    chunk_relations = text_to_relations(file_info["content"])
    filtered_facts = db_ready_facts(chunk_relations, doc_id)

    # Add file name to file_name_db
    file_name_db.insert({"doc_id": doc_id, "metadata": file_info["metadata"]})

    # Add filtered facts to scrapp_db
    loader = Loader("Adding to DB...", "Done!").start()

    for subject in filtered_facts:
        existing_entry = scrapp_db.get(Query().subject == subject)
        if existing_entry:  # case sensitive, is this a good choice?
            updated_facts = existing_entry["facts"] + filtered_facts[subject]
            scrapp_db.update({"facts": updated_facts}, Query().subject == subject)
        else:
            scrapp_db.insert({"subject": subject, "facts": filtered_facts[subject]})

    loader.stop()
    return file_info["metadata"]


import PyPDF2
import re


def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    with open(pdf_path, "rb") as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)

        # Initialize an empty string to store the extracted text
        extracted_text = ""

        # Iterate through each page in the PDF
        for page in pdf_reader.pages:
            # Extract text from the page
            page_text = page.extract_text()

            # Remove any potential table-like structures
            # This regex looks for patterns of repeated whitespace that might indicate a table
            page_text = re.sub(r"\s{2,}", " ", page_text)

            # Append the cleaned text to our result
            extracted_text += page_text + "\n\n"

    return extracted_text.strip()


from textsplitter import TextSplitter

import streamlit as st
import requests
import os
from urllib.parse import urlparse
import uuid


def download_webpage_html(url, save_folder="./documents/"):
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Raise an exception for bad status codes
        response.raise_for_status()

        # Get the HTML content
        html_content = response.text

        # If save_path is not provided, create a filename based on the URL
        parsed_url = urlparse(url)
        filename = parsed_url.netloc + parsed_url.path
        if filename.endswith("/"):
            filename += "index"
        filename = filename.replace("/", "_") + "__" + str(uuid.uuid4())[:9] + ".html"
        save_path = os.path.join(save_folder, filename)

        # Save the HTML content to a file
        with open(save_path, "w", encoding="utf-8") as file:
            file.write(html_content)

        print(f"HTML content saved successfully to: {save_path}")
        return save_path

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading the webpage: {e}")
        return None
    except IOError as e:
        print(f"An error occurred while saving the file: {e}")
        return None


import html_text


def extract_text_from_html_file(file_path, guess_layout=True):
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        # Open and read the HTML file
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        # Extract text from the HTML content
        extracted_text = html_text.extract_text(html_content, guess_layout=guess_layout)

        return extracted_text

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")
        return None


def ingest_document_prototype2(
    file_path, url=None
):  # need to add work for using webpages
    global scrapp_db
    global file_name_db
    # Read file and process content
    file_info = read_file_with_metadata(file_path)
    # add source like URL or title
    doc_id = str(uuid.uuid4())
    text_splitter = TextSplitter(
        max_token_size=300,
        end_sentence=True,
        preserve_formatting=True,
        remove_urls=False,
        replace_entities=True,
        remove_stopwords=False,
        language="english",
    )

    text = None
    if file_path.endswith(".txt"):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

        except UnicodeDecodeError:
            # If UTF-8 decoding fails, try reading as binary
            text = file.read().decode("utf-8", errors="replace")
    elif file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
        print(f"text: {text[:50]}")
    elif file_path.endswith(".html"):
        text = extract_text_from_html_file(file_path)
    text_chunks = text_splitter.split_text(text)
    for chunk in text_chunks[:5]:
        chunk = chunk.lstrip()
        label = ""
        if len(chunk) > 40:
            # Find the last space or period within the 40-50 character range
            for i in range(100, 39, -1):
                if i >= len(chunk):
                    continue
                if chunk[i] == " " or chunk[i] == ".":
                    label = chunk[: i + 1].rstrip()
                    break

        with st.expander('"' + label[:50] + '"' + "..."):
            st.write(str(chunk))

    relations = text_to_relations(text_chunks)
    filtered_facts = db_ready_facts(relations, doc_id)

    # Add file name to file_name_db
    file_name_db.insert({"doc_id": doc_id, "metadata": file_info["metadata"]})

    # Add filtered facts to scrapp_db
    loader = Loader("Adding to DB...", "Done!").start()

    for subject in filtered_facts:
        existing_entry = scrapp_db.get(Query().subject == subject)
        if existing_entry:  # case sensitive, is this a good choice?
            updated_facts = existing_entry["facts"] + filtered_facts[subject]
            scrapp_db.update({"facts": updated_facts}, Query().subject == subject)
        else:
            scrapp_db.insert({"subject": subject, "facts": filtered_facts[subject]})

    loader.stop()
    return file_info["metadata"]


from tinydb import TinyDB, Query
from rapidfuzz import fuzz


import json


# Get all documents
def search_db(query):
    all_docs = scrapp_db.all()
    all_subjects = [doc["subject"] for doc in all_docs]
    # for s in all_subjects:
    #     print(s)
    all_subjects = sorted(
        all_subjects, key=lambda x: fuzz.partial_ratio(query, x), reverse=True
    )
    q = Query()
    output = scrapp_db.search(q.subject == all_subjects[0])

    return json.dumps(output[0], indent=4)


def get_scrapp_db():
    all_docs = scrapp_db.all()
    return all_docs
