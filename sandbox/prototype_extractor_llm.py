import marimo

__generated_with = "0.6.25"
app = marimo.App(width="medium")


@app.cell
def __():

    from langchain_text_splitters import NLTKTextSplitter
    from maverick import Maverick
    import spacy
    from detokenize.detokenizer import detokenize
    from tqdm import tqdm
    from pprint import pprint
    import json

    import PyPDF2
    import ollama
    nlp_lg = spacy.load('en_core_web_lg')
    model = Maverick(device='cuda')

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


    def extract_relations_formatted(text):

        input_llm = """
        
        Please extract all relations betweens proper nouns and predicates and return this information only in the following JSON template. 
        Only put proper nouns in the subject field, the subject field must be populated.
        Valid relations are verbs like is/has/created/taken etc. THE SUBJECT + RELATION PREDICATE should form a complete sentence as close to how it appears in the text as possible
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

    def llm_chunks_to_facts(chunk,msubjects):

        prompt = f"""Extract a list of independently verifiable facts from the following text.Each fact should:
    1. Be as close to as it is directly stated in the text, not inferred
    2. Use full names or specific descriptors instead of pronouns. Do not use compound subjects
    3. Be meaningful and understandable on its own, without context from other facts
    4. Be phrased as a complete, grammatically correct sentence
    5. Not include subjective interpretations or opinions
    6. Do not include any information that seems to be formatting artifacts
    Please present the facts as a  bulleted list. Do not include any additional commentary or explanation beyond the list of facts. use only the following list of main subjects:{msubjects}"""
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
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in tqdm(pdf_reader.pages):
                content += page.extract_text()
        return content


    def read_pdf(file_path):
        content = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in tqdm(pdf_reader.pages):
                content += page.extract_text()
        return content


    def get_best_noun(cluster, offsets): #gets best Noune from a cluster, if all pronoiuns return none
        ls = []
        for noun, offset in zip(cluster, offsets):
            pos = nlp_lg(noun)[0].pos_
            # print(f"POS: {noun} {pos}")
            if pos in ["DET", "PROPN", "VERB"]:
                # print(noun, pos)
                ls.append([noun, offset])

        if len(ls) == 0:
            return None, None
        ls = sorted(ls, key=lambda x : len(x[0]),reverse=False)
        #TODO need better heuristic here, just picks first, should be informed by prior selections (search db for terms, select ones that are the same?)
        # print(f"Picked {ls[0][0]}!")
        return ls[0][0], ls[0][1]


    #https://stackoverflow.com/questions/56977820/better-way-to-use-spacy-to-parse-sentences
    def get_pro_nsubj(token):
        # get the (lowercased) subject pronoun if there is one
        pro_nsubj_list = [child for child in token.children if child.dep_ == 'nsubj'] 
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
            if token.pos_ in ['NOUN', 'ADJ']:
                if token.dep_ in ['attr', 'acomp'] and token.head.lower_ in ['is', 'was']: #TODO MAKE MORE ALL_ENCOMPASSING, probably use nested for loops? should apply to has, was etc
                    # to test for lemma 'be' use token.head.lemma_ == 'be'
                    nsubj = get_pro_nsubj(token.head)
                    if nsubj:
                        # get the text of each token in the constituent and join it all together
                        factoid =  [nsubj," " + token.head.lower_ + " "+ ' '.join([t.text for t in token.subtree])]
                        incomplete_facts.append(factoid)
        return incomplete_facts














    return (
        Maverick,
        NLTKTextSplitter,
        PyPDF2,
        detokenize,
        extract_relations_formatted,
        get_best_noun,
        get_declarations,
        get_pro_nsubj,
        json,
        llm_chunks_to_facts,
        model,
        nlp_lg,
        ollama,
        pprint,
        print_nicely_formatted,
        read_pdf,
        spacy,
        text,
        tqdm,
    )


@app.cell
def __():
    return


@app.cell
def __():
    return


@app.cell
def __(
    NLTKTextSplitter,
    detokenize,
    extract_relations_formatted,
    get_best_noun,
    llm_chunks_to_facts,
    model,
    text,
    tqdm,
):


    # text = read_pdf(r"C:\GH\scrapp\sandbox\documents\mctb2.pdf")




    text_splitter = NLTKTextSplitter(chunk_size=1000)
    chunks = text_splitter.split_text(text)

    all_facts = {}
    for chunk in tqdm(chunks):
        pronoun_results = model.predict(chunk)
        pron_tokenized = pronoun_results['tokens']
        offs_to_pron = {}
        main_subjects = []
        for i,(clusters, offsets) in enumerate(zip(pronoun_results['clusters_token_text'], pronoun_results['clusters_token_offsets'])):
            best_noun, best_noun_offset = get_best_noun(clusters, offsets)
            if best_noun != None:
                # print(f"CLUSTERS: {clusters}")
                # print(f"\nBEST NOUN: {best_noun, best_noun_offset }")
                for cl, off in zip(clusters, offsets):
                    # if cl != best_noun and off != best_noun_offset:
                    #     print(cl,off)

                    for i in range(off[0],off[1]+1):
                        # print(i)
                        if i == off[0]:
                            pron_tokenized[i] = best_noun

                            # pron_tokenized[i] = "\"" +  best_noun + "\""
                            # pron_tokenized[i] = "\"" +  best_noun + "(" + pron_tokenized[i] + ")\""

                        else:
                            pron_tokenized[i] = ''
                main_subjects.append(best_noun)
                    

            # print(temp_cl)
        # print(pron_tokenized)
        detokenized_chunk= detokenize(pron_tokenized)
        facts = llm_chunks_to_facts(detokenized_chunk, main_subjects)
        relations = extract_relations_formatted(facts)
        # relations = extract_relations_formatted(detokenized_chunk, main_subjects)
        print(detokenized_chunk)
        for f in relations['facts']:
            print(f)
        break


    return (
        all_facts,
        best_noun,
        best_noun_offset,
        chunk,
        chunks,
        cl,
        clusters,
        detokenized_chunk,
        f,
        facts,
        i,
        main_subjects,
        off,
        offs_to_pron,
        offsets,
        pron_tokenized,
        pronoun_results,
        relations,
        text_splitter,
    )


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
