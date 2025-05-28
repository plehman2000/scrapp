from langchain_text_splitters import RecursiveCharacterTextSplitter 
import ollama
import pickle 
import json

from tqdm import tqdm
MODEL = 'gemma3:12b'

# class TruthStatement:
#     def __init__(self, statement, state):
#         self.statement = statement

#         self.state = None
        #state can be True, False, Both or Neither
        #Can this be represented continously?






def extract_facts(text):
    schema = {"entity1": ["fact1", "fact2"]}
    prompt = f"""Extract atomic facts from the following text. Each fact should be:
    - A single, complete statement
    - Non-redundant
    - Self-contained (at least partially understandable without context)
    - Begin with the main entity being described
    - Are Active Tense (He did this)
    - Avoid Passive Tense (This he did)

    Avoid repeating phrases or creating multiple similar facts. If multiple related facts exist, express them as distinct statements without repetitive phrasing.

    Text: {text}

    Respond in JSON format matching this schema:
    {json.dumps(schema, indent=2)}

    Example of good atomic facts:
    - "Photosynthesis converts sunlight into chemical energy"
    - "Chloroplasts contain chlorophyll and other pigments"

    Example of redundant facts to avoid:
    - "Photosynthesis requires sunlight for plants"
    - "Photosynthesis requires water for plants"
    - "Photosynthesis requires carbon dioxide for plants"
    """

    #dolphin-llama3
    response = ollama.chat(model=MODEL, messages=[ #llama3
    {
    'role': 'user',
    'content': prompt}])#, options={"temperature":.5}

    output = response['message']['content']

    # x = output.replace("<|end-output|>","")#output[output.find("<|end-output|>"):]
    # print(x)
    return output

def parse_json_response(txt):
    return json.loads(txt[7:-3])

import time




import random;random.seed(42)

chunk_size = 500
splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=int(chunk_size * 0.1),
    length_function=len,
    is_separator_regex=False
)
all_text = open(r"docs\mahs.txt", encoding="utf8").read()
chunks = splitter.split_text(all_text)
print(chunks[0])


knowledge_base = {}#pickle.load(open("kbase.pkl", "rb"))
for i,chunk in enumerate(tqdm(chunks)):
    print(f"On Chunk {i},,,")

    # start_time = time.time()
    facts = extract_facts(chunk)
    # end_time = time.time()
    # print(f"LLM Execution time: {end_time - start_time} seconds")
    new_parsed_facts = parse_json_response(facts)


    for k in new_parsed_facts:
        if k in knowledge_base:
            for c in new_parsed_facts[k]:
                knowledge_base[k].append(c)
        else:
            knowledge_base[k] = new_parsed_facts[k]


    pickle.dump(knowledge_base, open("kbase.pkl", "wb"))



#All propositions have 2 dichotomies 
# apriority or aposteriority (logic v experience) (indeterminateness v determinateness)
# Analytic or Synthetic (Based on Meanings of words alone v how the words in the proposition relate to the world) (Immutability v Mutability)

# APPROACH EACH OF THESE 4 POSSIBLE PROPOSITION CATEGORIES WITH DIFF STRAT
#what are cheap word manipulation methods that avoid using llms?


#All ontological objects have 2 dichotomies
#Concreteness vs Abstractness (causally efficacious vs not located in space/time) (determinate v indeterminate)
#Universality vs Particularity (Redness vs A Example object that is a particular type of red) (immutable vs mutable) (Note that it is only in reference to universals can we see how things are alike)

"""

ROOT, acl, acomp, advcl, advmod, agent, amod, appos, attr, aux, auxpass, case, cc, ccomp, compound, conj,
 csubj, csubjpass, dative, dep, det, dobj, expl, intj, mark, meta
, neg, nmod, npadvmod, nsubj, nsubjpass, nummod,
 oprd, parataxis, pcomp, pobj, poss, preconj, predet, prep, prt, punct, quantmod, relcl, xcomp
"""