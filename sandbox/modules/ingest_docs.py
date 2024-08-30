import os
import datetime
from .scrapper import text_to_relations 
from tinydb import TinyDB, Query
from tqdm import tqdm
import uuid




global scrapp_db
global file_name_db
scrapp_db = TinyDB('./databases/scrapps_db.json')
file_name_db = TinyDB('./databases/files_db.json')


from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep


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



def read_file_with_metadata(file_path):
    result = {}

    # Get file metadata
    file_stats = os.stat(file_path)
    result['metadata'] = {
        'file_name': os.path.basename(file_path),
        'file_size': file_stats.st_size,
        'creation_time': datetime.datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
        'modification_time': datetime.datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
        # 'access_time': datetime.datetime.fromtimestamp(file_stats.st_atime).isoformat(),
    }

    # Read file content
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            result['content'] = file.read()
    except UnicodeDecodeError:
        # If UTF-8 decoding fails, try reading as binary
            result['content'] = file.read().decode('utf-8', errors='replace')

    return result

#:now to combine the relations based on the same subjects, thwen storee the docs and scrapps
def db_ready_facts(relations, doc_id):
    temp_facts = relations['facts']
    filtered_facts = {}
    for x in temp_facts:
        if x['subject'] not in filtered_facts:
            filtered_facts[x['subject']] = [] 
        filtered_facts[x['subject']].append([ x['predicate'], doc_id]) 
    return filtered_facts

def ingest_document_prototype(file_path): #need to add work for using webpages
    global scrapp_db 
    global file_name_db
    # Read file and process content
    file_info = read_file_with_metadata(file_path)

    # add source like URL or title
    doc_id = str(uuid.uuid4())
    relations = text_to_relations(file_info['content'])
    filtered_facts = db_ready_facts(relations, doc_id)
    
    # Add file name to file_name_db
    file_name_db.insert({'doc_id': doc_id, 'metadata': file_info['metadata']})
    
    # Add filtered facts to scrapp_db
    loader = Loader("Adding to DB...", "Done!").start()
    
    for subject in filtered_facts:
        existing_entry = scrapp_db.get(Query().subject == subject)
        if existing_entry: # case sensitive, is this a good choice? 
            updated_facts = existing_entry['facts'] + filtered_facts[subject]
            scrapp_db.update({'facts': updated_facts}, Query().subject == subject)
        else:
            scrapp_db.insert({'subject': subject, 'facts': filtered_facts[subject]})
    
    loader.stop()





from tinydb import TinyDB, Query
from rapidfuzz import fuzz



import json

# Get all documents
def search_db(query):
    all_docs = scrapp_db.all()
    all_subjects = [doc['subject'] for doc in all_docs]
    # for s in all_subjects:
    #     print(s)
    all_subjects = sorted(all_subjects, key=lambda x: fuzz.partial_ratio(query,x), reverse=True)
    q = Query()
    output = scrapp_db.search(q.subject == all_subjects[0])

    return  json.dumps(output[0], indent=4)


def get_scrapp_db():
    all_docs = scrapp_db.all()
    all_subjects = [doc['subject'] for doc in all_docs]
    return all_subjects


