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
def _(pickle):
    kbase  = pickle.load(open("kbase.pkl", "rb"))

    return (kbase,)


@app.cell
def _(full, kbase, ollama, spacy):
    from tqdm import tqdm
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
                all_trips.append([[s,r,o],[sdoc, rdoc, odoc]])

            # print(f"[{s}][{ r}][{o}] ||| {c}")
        # if temp_list != []:

        #     kbase_trips[k] = temp_list
        #     nlp(r)
        #     print([ type(o)])
        #     print([ o])
    # pprint(list_of_all_statements)

    return all_trips, c


@app.cell
def _(all_trips):
    all_trips# niuce, now SEARCH?
    return


@app.cell
def _(all_trips):
    vec_pairs = [[i,x] for i,x in enumerate(all_trips)]
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    # for ch in token.children:
    #     # print(ch, ch.dep_)
    #     print(f"child is {ch.text} at {ch.i}, dep = {ch.dep_}")
    #     for chunkidx,possible_noun_chunk in enumerate(noun_chunks):
    #         # print(f"checking {possible_noun_chunk.start} - {possible_noun_chunk.end}")
    #         if ch.i >= possible_noun_chunk.start and ch.i <= possible_noun_chunk.end:
    #             print(f"member of {possible_noun_chunk}")
    #             noun_chunks.pop(chunkidx)
    #             break
    # print(noun_chunks)
    # break
    return


@app.cell
def _(c, nlp):
    from spacy import displacy


    displacy.render(nlp(c), style="dep", jupyter=True)
    return


@app.cell
def _():
    # doc[0].dep_ = None # DELETE RELATIONS WHEN DONE
    return


@app.cell
def _():
    return


@app.cell
def _():

    # # Finding a verb with a subject from below — good
    # verbs = set()
    # for possible_subject in doc:
    #     # print(possible_subject.dep_)
    #     # print(possible_subject.head.pos_)
    #     if possible_subject.dep_ == "nsubj" and possible_subject.head.pos_ == "VERB":
    #         verbs.add(possible_subject.head)
    # print(verbs)

    # verbs = list(verbs)
    return


if __name__ == "__main__":
    app.run()
