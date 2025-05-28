import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import pickle 
    import ollama
    from langchain_text_splitters import RecursiveCharacterTextSplitter 
    from pprint import pprint
    import spacy


    def embedding(text):
        #dolphin-llama3
        response = ollama.chat(model="nomic-embed-text:latest", messages=[ #llama3
        {
        'role': 'user',
        'content': text}])#, options={"temperature":.5}
        output = response['message']['content']
        return output

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

    return nlp, ollama, pickle, spacy


@app.cell
def _():
    return


@app.cell
def _():


    return


@app.cell
def _(nlp, spacy):

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
            # print(token, token.pos_)
            if token.pos_ in ["VERB", "AUX"]:
                # print(token,token.pos_)
                # print(f"[{token}] is a relation")
                potential_relation_tokens.append(token)
        #find main relation
        main_relation = None
        if len(potential_relation_tokens) == 0:
            return None,None,None
        if len(potential_relation_tokens) == 1:
            main_relation = potential_relation_tokens[0]
        # elif potential_relation_tokens[0].pos_ == "AUX":
        #     main_relation = potential_relation_tokens[0]
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
            # print(child, child.dep_)
            if child.dep_ in ["nsubj", "ROOT"]:
                base_subject = child
                break
        if not base_subject:
            return None, None, None

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
        # print(main_relation_final_list_sorted[-1])

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


        if not base_object:
            return None, None, None
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
            if node and node not in visited_objects:
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
        obj = " ".join([x.text for x in visited_objects])

        # print(visited_objects)


        # Print visited objects for debugging

        # If obj is a spaCy Span, convert it to a string
        if obj and isinstance(obj, spacy.tokens.Span):
            obj = obj.text  # simpler than joining tokens manually


        if subject and isinstance(subject, spacy.tokens.Span):
            subject = subject.text  # simpler than joining tokens manually

        if relation and isinstance(relation, spacy.tokens.Span):
            relation = relation.text  # simpler than joining tokens manually

        # Return the extracted components
        return subject, relation, obj




    # sentence = "cool organisms rapidly share jungle organisms"# as a key characteristic commonly"
    # sentence = "Biology can wrestle with questions about life"
    # sentence = "Sweat is a way to be cooler"
    # sentence = "Slimy sweat currently acts nicely as a cooling mechanism for pipes."
    #START

    import re
    def full(sentence):
        # sentence = re.sub(r'[.!?;:]+$', '', sentence.strip())

        doc = nlp(sentence)

        subject, relation, obj = get_Sub_Rel_Obj(doc)
        # print(f"[{subject}][{ relation}][{object}]")
        return doc,subject, relation, obj


    # doc,subject, relation, object = full(sentence)

    return (full,)


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(pickle):
    kbase  = pickle.load(open("kbase.pkl", "rb"))

    return (kbase,)


@app.cell
def _(full, kbase, ollama, spacy):
    from tqdm import tqdm
    import time
    list_of_all_statements = []
    all_trips = []
    kbase_trips = {}
    for k in tqdm(kbase.keys()):
        # print(k)
        temp_list = []
        for c in kbase[k]:
            list_of_all_statements.append(c)
            # print(c)
            d,s, r, o = full(c)
            # print(type(s))
            if s and r and o:
                temp_list.append([s, r,o])
                if s and isinstance(s, spacy.tokens.Span):
                    s = s.text
                if r and isinstance(r, spacy.tokens.Span):
                    r = r.text
                if o and isinstance(o, spacy.tokens.Span):
                    o = o.text
                sdoc = ollama.embed(model='nomic-embed-text:latest', input=s)['embeddings']
                rdoc = ollama.embed(model='nomic-embed-text:latest', input=r)['embeddings']
                odoc = ollama.embed(model='nomic-embed-text:latest', input=o)['embeddings']
                all_trips.append([[s,sdoc],[r,rdoc], [o,odoc]])



    all_trips = all_trips[1:]# TODO FIX ME, why is wide_var_0 the first entry?
    return (all_trips,)


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Now we can actually start looking at our triplets. We can organize them by clustering based on the relations 

    """
    )
    return


@app.cell
def _(all_trips):
    import numpy as np
    from sklearn.cluster import HDBSCAN
    from sklearn.datasets import load_digits

    import random
    random.seed(42)
    relation_embeddings = [x[1][1][0] for x in all_trips]
    hdb = HDBSCAN(min_cluster_size=4)
    cluster_labels_relation_embeddings = hdb.fit_predict(np.array(relation_embeddings))

    # pca = PCA(n_components=2)
    # embedded_x = pca.fit_transform(z)
    return (cluster_labels_relation_embeddings,)


@app.cell
def _(all_trips, cluster_labels_relation_embeddings):
    relation_sorted_trips = {}

    for cl, x in zip(cluster_labels_relation_embeddings, all_trips):
        # print([cl,x[0][0], x[1][0],x[2][0]])
        if cl not in relation_sorted_trips:
            relation_sorted_trips[cl] = []
        relation_sorted_trips[cl].append(f"{x[0][0]} {x[1][0]} {x[2][0]}")
        relation_sorted_trips[cl] = list(set(relation_sorted_trips[cl]))
        
    return (relation_sorted_trips,)


@app.cell
def _(relation_sorted_trips):
    relation_sorted_trips
    return


@app.cell
def _(mo):
    mo.md(
        rf"""
    Now we can focus in on individual relation groups to see what kind of entities tend to be related by these things
    # I do not like that the statements are fairly inexpressive. There must be a better way to ingest
    """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""# So next step, run this on a giant book or something and see if we can find meta-relations, put it in a big diagram?""")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
