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
            embedding = ollama.embeddings(
                model="nomic-embed-text", prompt=x["subject"] + " " + x["predicate"]
            )["embedding"]

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


from stqdm import stqdm


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

    file_name_db.insert({"doc_id": doc_id, "metadata": file_info["metadata"]})
    loader = Loader("Adding to DB...", "Done!").start()
    print("Loading")
    for chunk in stqdm(
        text_chunks, desc="Extracting Relations", backend=False, frontend=True
    ):
        relations = text_to_relations([chunk])
        filtered_facts = db_ready_facts(relations, doc_id)

        # Add filtered facts to scrapp_db

        for subject in filtered_facts:
            existing_entry = scrapp_db.get(Query().subject == subject)
            if existing_entry:  # case sensitive, is this a good choice?
                temp_facts = ""
                if "facts" in existing_entry:
                    temp_facts = (
                        existing_entry["facts"] if existing_entry["facts"] else ""
                    )
                else:
                    print("Warning: 'facts' key not found in existing_entry")
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


"""
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
"""

from langchain_text_splitters import NLTKTextSplitter
from maverick import Maverick
import spacy
from detokenize.detokenizer import detokenize
from tqdm import tqdm
from pprint import pprint
import json

import PyPDF2
import ollama

nlp_lg = spacy.load("en_core_web_lg")
model = Maverick(device="cuda")

text = """Mindfulness is in a category all by itself, as it can potentially balance and perfect the remaining four spiritual faculties. This does not mean that we shouldn't be informed by the other two pairs, but that mindfulness is extremely important. 
Mindfulness means knowing what is as it is right now. It is the quality of mind that knows things as they are. Really, it is the quality of sensations manifesting as they are, where they are, and on their own. However, initially
it appears to be something we create and cultivate, and that is okay for the time being.4
 If you
are trying to perceive the sensations that make up your experience clearly and to know what
they are, you are balancing energy and concentration, and faith and wisdom. Due to energy, the
mind is alert and attentive. Due to concentration, it is stable. Faith here may also mean acceptance, and wisdom here is clear comprehension.
Notice that this has nothing to do with some vague spacing out in which we wish that reality
would go away and our thoughts would never arise again. I don't know where people get the
notion that vague and escapist aversion to experience and thought are related to insight practice, but it seems to be a common one. Mindfulness means being very clear about our human,
mammalian reality as it is. It is about being here now. Truth is found in the ordinary sensations
that make up our experience. If we are not mindful of them or reject them because we are looking for “progress”, “depth”, or “transcendence”, we will be unable to appreciate what they have
to teach, and be unable to do insight practices.
The five spiritual faculties have also been presented in another order that can be useful:
faith, energy, mindfulness, concentration, and wisdom. In this order, they apply to each of the
three trainings, the frst of which, as discussed earlier, is morality. We have faith that training
in morality is a good idea and that we can do it, so we exert energy to live up to a standard of
clear and skillful living. We realize that we must pay attention to our thoughts, words, and
deeds in order to do this, so we try to be mindful of them. We realize that we often fail to pay
attention, so we try to increase our ability to concentrate on how we live our life. In this way,
through experience, we become wiser in a relative sense, learning how to live a good and useful life. Seeing our skill improve and the benefts it has for our life, we generate more faith,
and so on.
With respect to training in concentration, we may have faith that we might be able to attain
high states of consciousness, so we sit down on a cushion and energetically try to stabilize our
attention and tune in to skillful qualities. We realize that we cannot stabilize our attention without mindfulness of our object and of the qualities of the state we wish attain. We develop strong
concentration by consistently stabilizing our attention. We attain high states of concentration
and thus gain a direct understanding of how to navigate in that territory and the meaning and
purpose of doing so. Our success creates more faith, and so we apply energy to further develop
our concentration abilities.
With the faith borne of the experience yielded by strong concentration, we begin to think it
might be possible to awaken, so we energetically explore all the sensations that make up our
world. With an alert and energetic mind, we mindfully explore this heart, mind, and body just
as it is now. Reality becomes more and more interesting, so our concentration grows, and this
combination of the first four produces fundamental wisdom. Wisdom leads to more faith, and
the cycle goes around again.    """

def llm_facts_to_formatted_facts(facts):
    raw_facts = []

    prompt = """
    Task: Rewrite each fact in the provided list using the format 'Proper Noun Verbs Object,' 
    following these guidelines:

    - Noun: Identify the subject of the original fact and use it as the noun. Do not replace it with a pronoun.
    - Verb/Object: Choose a verb that captures the primary action or state described in the fact and object with key details from the original fact.

    All facts should be formatted as grammatically correct, complete sentences. If needed, split sentences 
    into smaller ones to maintain clarity and accuracy.

    Instructions: Apply this structure to each fact in the list, always following noun -> verb -> object. 
    Ensure the rewritten facts are clear, accurate, and maintain the same form and information of the original information.
    Use full names or specific descriptors instead of pronouns.


    """

    response = ollama.chat(
        model="dolphin-llama3"
        # model='gemma2:27b'
        ,
        messages=[{"role": "user", "content": prompt + facts}],  # llama3
    )
    output = response["message"]["content"]
    return output
def extract_relations_formatted(text, msubjects):

    input_llm = """
    
    Please extract all relations betweens proper nouns and predicates and return this information only in the following JSON template. 
    Only put proper nouns in the subject field, the subject field must be populated.
    Valid relations are verbs like is/has/created/taken etc. THE SUBJECT + RELATION PREDICATE should form a complete sentence as close to how it appears in the text as possible
    Use only the following list of main subjects as subjects :""" + ",".join(msubjects) +     """
    ### Template:
     {
      "facts": [
         {
          "subject": "",
          "predicate": ""
         },
         {
          "subject": "",
          "predicate": ""
         }
      ]
     }

    ### Example:
     {
      "facts": [
         {
          "subject": "Adriaan van Wijngaarden",
          "predicate": "employed Dijkstra as the first computer programmer in the Netherlands at the Mathematical Centre in Amsterdam (1952-1962)"
         },
         {
          "subject": "Dijkstra",
          "predicate": "formulated the shortest path problem in 1956"
         }
         {
          "subject": "Dijkstra",
          "predicate": "solved the shortest path problem in 1956"
         }
                  {
          "subject": "John",
          "predicate": "is reknowned for his Computer Science contributions"
         }
      ]
     }

    ### Text:
    """

    response = ollama.chat(
        model="dolphin-llama3",
        format="json",
        messages=[{"role": "user", "content": input_llm + text}],  # llama3
    )  # , options={"temperature":.5}

    output = response["message"]["content"]
    output = output.replace("<|end-output|>", "")
    try:
        parsed_output = json.loads(output)

    except json.JSONDecodeError as json_error:
        print(f"JSON parsing error in chunk")
        print(f"Problematic output")
        # Optionally, you can add the error to raw_facts or handle it differently

    except Exception as e:
        print(f"Error processing chunk")

    return parsed_output


def llm_chunks_to_facts(chunk):

    prompt = f"""Extract a list of independent  facts from the following text.Each fact should:
1. Be as close to as it is directly stated in the text, not inferred
2. Use full names or specific descriptors instead of pronouns. Do not use compound subjects
3. Be meaningful and understandable on its own, without context from other facts
4. Be phrased as a complete, grammatically correct sentence
5. Not include subjective interpretations or opinions
6. Do not include any information that seems to be formatting artifacts
7. Try to use simple subjects
Please present the facts as a  bulleted list. Do not include any additional commentary or explanation beyond the list of facts. """
    response = ollama.chat(
        model="dolphin-llama3"
        # model='gemma2:27b'
        ,
        messages=[{"role": "user", "content": prompt + chunk}],  # llama3
    )
    output = response["message"]["content"]
    return output


def read_pdf(file_path):
    content = ""
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in tqdm(pdf_reader.pages):
            content += page.extract_text()
    return content


def read_pdf(file_path):
    content = ""
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in tqdm(pdf_reader.pages):
            content += page.extract_text()
    return content


def get_best_noun(
    cluster, offsets
):  # gets best Noune from a cluster, if all pronoiuns return none
    ls = []
    for noun, offset in zip(cluster, offsets):
        pos = nlp_lg(noun)[0].pos_
        # print(f"POS: {noun} {pos}")
        if pos in ["DET", "PROPN", "VERB"]:
            # print(noun, pos)
            ls.append([noun, offset])

    if len(ls) == 0:
        return None, None
    ls = sorted(ls, key=lambda x: len(x[0]), reverse=False)
    # TODO need better heuristic here, just picks first, should be informed by prior selections (search db for terms, select ones that are the same?)
    # print(f"Picked {ls[0][0]}!")
    return ls[0][0], ls[0][1]


# https://stackoverflow.com/questions/56977820/better-way-to-use-spacy-to-parse-sentences
def get_pro_nsubj(token):
    # get the (lowercased) subject pronoun if there is one
    pro_nsubj_list = [child for child in token.children if child.dep_ == "nsubj"]
    if len(pro_nsubj_list) == 0:
        return None
    return pro_nsubj_list[0]


def print_nicely_formatted(data):
    for key, values in data.items():
        print(f"'{key}': [")
        for value in values:
            print(f"    '{value}',")
        print("],\n")


def get_declarations(doc):
    incomplete_facts = []
    for token in doc:
        if token.pos_ in ["NOUN", "ADJ"]:
            if token.dep_ in ["attr", "acomp"] and token.head.lower_ in [
                "is",
                "was",
            ]:  # TODO MAKE MORE ALL_ENCOMPASSING, probably use nested for loops? should apply to has, was etc
                # to test for lemma 'be' use token.head.lemma_ == 'be'
                nsubj = get_pro_nsubj(token.head)
                if nsubj:
                    # get the text of each token in the constituent and join it all together
                    factoid = [
                        nsubj,
                        " "
                        + token.head.lower_
                        + " "
                        + " ".join([t.text for t in token.subtree]),
                    ]
                    incomplete_facts.append(factoid)
    return incomplete_facts


def ingest_document_prototype3(
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

    file_name_db.insert({"doc_id": doc_id, "metadata": file_info["metadata"]})
    # loader = Loader("Adding to DB...", "Done!").start()
    print("Loading")
    pronoun_results_list = []
    for chunk in stqdm(text_chunks, desc="Getting parts of speech...", backend=False, frontend=True):
        pronoun_results_list.append(model.predict(chunk))
    print("Done")
    zix = 0
    for chunk in stqdm(
        text_chunks, desc="Extracting Relations", backend=False, frontend=True
    ):
        pronoun_results = pronoun_results_list[zix]  # model.predict(chunk)
        zix +=1
        pron_tokenized = pronoun_results["tokens"]
        main_subjects = []
        relations_list = []
        for i, (clusters, offsets) in enumerate(
            zip(
                pronoun_results["clusters_token_text"],
                pronoun_results["clusters_token_offsets"],
            )
        ):
            best_noun, _ = get_best_noun(clusters, offsets)
            if best_noun != None:
                for cl, off in zip(clusters, offsets):
                    for i in range(off[0], off[1] + 1):
                        if i == off[0]:
                            pron_tokenized[i] = best_noun
                        else:
                            pron_tokenized[i] = ""
                main_subjects.append(best_noun)

            # print(temp_cl)
        # print(pron_tokenized)
        detokenized_chunk = detokenize(pron_tokenized)
        facts = llm_chunks_to_facts(detokenized_chunk)
        formatted_facts = llm_facts_to_formatted_facts(facts)
        relations = extract_relations_formatted(formatted_facts, main_subjects)

        # facts = llm_chunks_to_facts(text)
        # formatted_facts = llm_facts_to_formatted_facts(facts)
        # relations = extract_relations_formatted(formatted_facts)



        print(relations)
        relations_list.append(relations)
    filtered_facts = db_ready_facts(relations_list, doc_id)

    # Add filtered facts to scrapp_db
    print(filtered_facts)
    for subject in filtered_facts:
        existing_entry = scrapp_db.get(Query().subject == subject)
        if existing_entry:  # case sensitive, is this a good choice?
            temp_facts = ""
            if "facts" in existing_entry:
                temp_facts = existing_entry["facts"] if existing_entry["facts"] else ""
            else:
                print("Warning: 'facts' key not found in existing_entry")
            updated_facts = existing_entry["facts"] + filtered_facts[subject]
            scrapp_db.update({"facts": updated_facts}, Query().subject == subject)
        else:
            scrapp_db.insert({"subject": subject, "facts": filtered_facts[subject]})

    return file_info["metadata"]
