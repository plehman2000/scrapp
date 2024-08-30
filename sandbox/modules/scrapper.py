import ollama


def extract_relations_formatted(text):

    input_llm = """
    Please extract all relations betweens proper nouns and predicates and return in the following JSON template. Valid relations are verbs like is/has/created/taken etc. THE SUBJECT + RELATION PREDICATE should form a complete sentence as close to how it appears in the text as possible
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

    response = ollama.chat(model='dolphin-llama3',
                           format="json",messages=[ #llama3
    {
    'role': 'user',
    'content': input_llm + text}])#, options={"temperature":.5}

    output = response['message']['content']
    output = output.replace("<|end-output|>","")
    try:
        parsed_output = json.loads(output)

    except json.JSONDecodeError as json_error:
        print(f"JSON parsing error in chunk")
        print(f"Problematic output")
        # Optionally, you can add the error to raw_facts or handle it differently

    except Exception as e:
        print(f"Error processing chunk")


    return parsed_output

import spacy
import json
def get_entities(text):


    nlp = spacy.load("en_core_web_trf")
    doc = nlp(text)

    # entities = [(ent.text, ent.label_) for ent in doc.ents 
    entities = [ent.text for ent in doc.ents 
                if ent.label_ not in ["MONEY", "TIME", "DATE", "CARDINAL", "PERCENT", "QUANTITY", "ORDINAL"]]

    return entities



# def llm_replace_pronouns
def llm_chunks_to_facts(chunk):
    raw_facts = []

    prompt = """Extract a list of independently verifiable facts from the following text. Each fact should:
1. Be as close to as it is directly stated in the text, not inferred
2. Use full names or specific descriptors instead of pronouns
3. Be meaningful and understandable on its own, without context from other facts
4. Be phrased as a complete, grammatically correct sentence
5. Not include subjective interpretations or opinions
Please present the facts as a  bulleted list. Do not include any additional commentary or explanation beyond the list of facts."""
    response = ollama.chat(
        model='dolphin-llama3'
        # model='gemma2:27b'
        , messages=[ #llama3
    {
    'role': 'user',
    'content': prompt + chunk}])
    output = response['message']['content']
    return output


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
    model='dolphin-llama3'
    # model='gemma2:27b'
    , messages=[ #llama3
    {
    'role': 'user',
    'content': prompt + facts}])
    output = response['message']['content']
    return output


# def chunk_to_ents(text):
#     entities = set()
#     result = get_entities(text)
#     [entities.add(r) for r in result]
#     entities = list(entities)
#     facts = llm_chunks_to_facts( chunks)
#     all_out = [p['facts'] for p in facts]
#     return sum(all_out, [])




import spacy

# Load the English language model
nlp = spacy.load("en_core_web_sm")

def parse_sentence(sentence):
    # Process the sentence
    doc = nlp(sentence)
    
    # Initialize variables
    subject = ""
    verb = ""
    predicate = ""
    
    # Find the root of the sentence (usually the main verb)
    root = None
    for token in doc:
        if token.dep_ == "ROOT":
            root = token
            verb = token.text
            break
    
    # Find the subject and its modifiers
    if root:
        for child in root.children:
            if child.dep_ in ["nsubj", "nsubjpass"]:
                subject_token = child
                subject = ' '.join([token.text for token in subject_token.subtree 
                                    if token.dep_ in ["amod", "compound"] or token == subject_token])
                break
    
    # Construct the predicate (everything except the subject)
    if root:
        predicate_tokens = [token for token in doc if token.i < subject_token.i or token.i > subject_token.i]
        predicate = ' '.join([token.text for token in predicate_tokens if token != root])
    
    return {
        "subject": subject.strip(),
        "verb": verb,
        "predicate": predicate.strip()
    }

# Example usage


sample = """Born in Rotterdam, the Netherlands, Dijkstra studied mathematics and physics and then theoretical physics at the University of Leiden. Adriaan van Wijngaarden offered him a job as the first computer programmer in the Netherlands at the Mathematical Centre in Amsterdam, where he worked from 1952 until 1962. He formulated and solved the shortest path problem in 1956, and in 1960 developed the first compiler for the programming language ALGOL 60 in conjunction with colleague Jaap A. Zonneveld. In 1962 he moved to Eindhoven, and later to Nuenen, where he became a professor in the Mathematics Department at the Technische Hogeschool Eindhoven. In the late 1960s he built the THE multiprogramming system, which influenced the designs of subsequent systems through its use of software-based paged virtual memory. Dijkstra joined Burroughs Corporation as its sole research fellow in August 1973. The Burroughs years saw him at his most prolific in output of research articles. He wrote nearly 500 documents in the "EWD" series, most of them technical reports, for private circulation within a select group.

Dijkstra accepted the Schlumberger Centennial Chair in the Computer Science Department at the University of Texas at Austin in 1984, working in Austin, Texas, until his retirement in November 1999. He and his wife returned from Austin to his original house in Nuenen, where he died on 6 August 2002 after a long struggle with cancer.[3]

He received the 1972 Turing Award for fundamental contributions to developing structured programming languages. Shortly before his death, he received the ACM PODC Influential Paper Award in distributed computing for his work on self-stabilization of program computation. This annual award was renamed the Dijkstra Prize the following year, in his honor. He was later killed for saying "nigger" in front of a live studio audience"""


sample = """The Catholic Church, also known as the Roman Catholic Church, is the largest Christian church, with 1.28 to 1.39 billion baptized Catholics worldwide as of 2024.[4][5][9] It is among the world's oldest and largest international institutions and has played a prominent role in the history and development of Western civilization.[10][11][12][13] The church consists of 24 sui iuris churches, including the Latin Church and 23 Eastern Catholic Churches, which comprise almost 3,500[14] dioceses and eparchies located around the world. The pope, who is the bishop of Rome, is the chief pastor of the church.[15] The Diocese of Rome, known as the Holy See, is the central governing authority of the church. The administrative body of the Holy See, the Roman Curia, has its principal offices in Vatican City, a small independent city-state and enclave within the Italian capital city of Rome, of which the pope is head of state.

The core beliefs of Catholicism are found in the Nicene Creed. The Catholic Church teaches that it is the one, holy, catholic and apostolic church founded by Jesus Christ in his Great Commission,[16][17][note 1] that its bishops are the successors of Christ's apostles, and that the pope is the successor to Saint Peter, upon whom primacy was conferred by Jesus Christ.[20] It maintains that it practises the original Christian faith taught by the apostles, preserving the faith infallibly through scripture and sacred tradition as authentically interpreted through the magisterium of the church.[21] The Roman Rite and others of the Latin Church, the Eastern Catholic liturgies, and institutes such as mendicant orders, enclosed monastic orders and third orders reflect a variety of theological and spiritual emphases in the church.[22][23]"""








def replace_pronouns_json(text):

    input_llm = """
    Replace all pronouns in following JSON with the most appropriate proper noun available, using the context from all provided facts. Do not return pronouns, such as "he" or "she" 
    Return the modified JSON in the same format as the original, shown below. Ensure that each proper noun subject
    in the list of JSON objects is unique and not repeated. PLEASE DO NOT INCLUDE PRONOUNS LIKE HE OR SHE IN THIS OUTPUTOnly return the JSON:
    """

    response = ollama.chat(model='dolphin-llama3',
                           format="json",messages=[ #llama3
    {
    'role': 'user',
    'content': input_llm + str(text)}])#, options={"temperature":.5}

    output = response['message']['content']
    output = output.replace("<|end-output|>","")
    try:
        parsed_output = json.loads(output)

    except json.JSONDecodeError as json_error:
        print(f"JSON parsing error in chunk")
        print(f"Problematic output")
        # Optionally, you can add the error to raw_facts or handle it differently

    except Exception as e:
        print(f"Error processing chunk")


    return parsed_output



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

from time import sleep



def text_to_relations(text):
    loader = Loader("Collecting Facts...").start()
    facts = llm_chunks_to_facts(text)
    loader.stop()

    loader = Loader("Formatting Facts...").start()
    formatted_facts = llm_facts_to_formatted_facts(facts)
    loader.stop()

    loader = Loader("Extracting Relations...").start()
    relations = extract_relations_formatted(formatted_facts)
    loader.stop()

    loader = Loader("Replacing pronouns...").start()
    out = replace_pronouns_json(relations)
    loader.stop()

    return out