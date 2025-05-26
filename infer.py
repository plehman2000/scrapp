import pickle 
import ollama
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from pprint import pprint
import spacy



def get_groundedness(ground_truth, claim):
    prompt = f"""
Document: {ground_truth}
Prompt: {claim}
    """

    #dolphin-llama3
    response = ollama.chat(model="bespoke-minicheck:7b", messages=[ #llama3
    {
    'role': 'user',
    'content': prompt}])#, options={"temperature":.5}

    output = response['message']['content']
    return output





nlp = spacy.load("en_core_web_trf")


kbase  = pickle.load(open("kbase.pkl", "rb"))

pprint(kbase)



# I want to use spacy dependency parsing to identify all possible ontological entities


def get_full_relation(relation):
    #get modifiers for relation if they exist
    main_relation_final_list = [relation]

    for child in relation.children:
        # print(child, child.dep_)
        if child.dep_ in ["advmod", "prep"]:
            #add to main relation
            main_relation_final_list.append(child)
            # print(child,child.dep_)
    main_relation_final_list.sort(key = lambda x : x.i)
    return main_relation_final_list

def get_full_subject(subject, doc):
    for possible_noun_chunk in doc.noun_chunks:
        if subject.i >= possible_noun_chunk.start and subject.i <= possible_noun_chunk.end:
            return possible_noun_chunk

    return None






# Get Relation
def get_Sub_Rel_Obj(doc):
    potential_relation_tokens = []
    for token in doc:
        # print(token, token.pos_)
        if token.pos_ in ["VERB", "AUX"]:
            # print(token,token.pos_)
            # print(f"[{token}] is a relation")
            potential_relation_tokens.append(token)
    #find main relation
    main_relation = None
    if len(potential_relation_tokens) == 0:
        return None
    if len(potential_relation_tokens) == 1:
        main_relation = potential_relation_tokens[0]
    elif potential_relation_tokens[0].pos_ == "AUX":
        main_relation = potential_relation_tokens[0]
    else:
        # if any of them are AUX
        potential_relation_tokens_pos = list(set([x.pos_ for x in potential_relation_tokens]))
        if "AUX" in potential_relation_tokens_pos:
            for tok in potential_relation_tokens:
                if tok.pos_ == "AUX":
                    main_relation = tok
                    break
        else:
            main_relation = potential_relation_tokens[0]



    #Get Subject
    base_subject = None
    for child in main_relation.children:
        if child.dep_ == "nsubj":
            base_subject = child
            break
    
    noun_chunks = list(doc.noun_chunks)
    
    # Get Full Subject
    subject = None
    for i, possible_noun_chunk in enumerate(doc.noun_chunks):
        if base_subject.i >= possible_noun_chunk.start and base_subject.i <= possible_noun_chunk.end:
            subject =  possible_noun_chunk
            noun_chunks.pop(i) # remove this chunk to leave only candidates for the object chunk
            break


    main_relation_final_list_sorted = get_full_relation(main_relation)


    relation = " ".join([x.text for x in main_relation_final_list_sorted])
    print(main_relation_final_list_sorted[-1])

    if len(noun_chunks) == 1:
        return subject, relation, noun_chunks[0]




    base_object = None
    for child in main_relation_final_list_sorted[-1].children:
        # print(child, child.dep_)
        if child.dep_ in ["pobj"]:
            #add to main relation
            # print(child,child.dep_)
            base_object = child
            break



        #TODO ADD COMPLEX LOGIC
    remove_dep_for_these = main_relation_final_list_sorted
    [main_relation_final_list_sorted.append(x) for x in subject]
    # for remove_tok in remove_dep_for_these:
    #     remove_tok.dep_ = None
    #     remove_tok.ancestors = None

    #Now perform BFS on this token base_object
    #has attributes of .children and .ancestor, collect all connected tokens in a list
    visited_objects = set(remove_dep_for_these)

    def bfs(node):
        if node not in visited_objects:
            visited_objects.add(node)
            for child in node.children:
                bfs(child)
            for child in node.ancestors:
                bfs(child)
        else:
            return

    bfs(base_object)
    for x in remove_dep_for_these:
        visited_objects.remove(x)

    visited_objects = list(visited_objects)
    visited_objects.sort(key = lambda x : x.i)
    object = " ".join([x.text for x in visited_objects])
    
    print(visited_objects)

    # now combine remove dependencies inplace and return text
    # for t in main_relation_final_list:
    #     t.dep_ = None

    return subject, relation, object




# sentence = "cool organisms rapidly share jungle organisms"# as a key characteristic commonly"
# sentence = "Biology can wrestle with questions about life"
# sentence = "Sweat is a way to be cooler"
# sentence = "Slimy sweat currently acts nicely as a cooling mechanism for pipes."
#START

import re
def full(sentence):
    sentence = re.sub(r'[.!?;:]+$', '', sentence.strip())
    
    doc = nlp(sentence)
    
    subject, relation, object = get_Sub_Rel_Obj(doc)
    return doc,subject, relation, object




list_of_all_statements = []
for k in kbase:
    for c in kbase[k]:
        list_of_all_statements.append(c)
        x = full(c)
        print(x)
        doc,subject, relation, object = x
        print(f"[{subject}][{ relation}][{object}] ||| {c}")

# pprint(list_of_all_statements)






