import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import ollama
    import json
    # text = ""
    # schema = """ {"title": ""}"""
    # input_llm = f""" 
    # You extract the title from the first part of this chunk, ignoring the author names afterward### Template:
    # {json.dumps(json.loads(schema), indent=4)}
    # ### Example:
    # {{"title": "Amazing new discovery"}}
    # ### Text:
    # {text}
    # """

    # response = ollama.chat(model='nuextract', messages=[ #llama3
    # {
    # 'role': 'user',
    # 'content': input_llm}])#, options={"temperature":.5}

    # output = response['message']['content']

    # x = output.replace("<|end-output|>","")#output[output.find("<|end-output|>"):]
    # print(x)

    return json, ollama


@app.cell
def _(json, ollama):
    MODEL = 'gemma3:12b'


    def extract_entities(text):
        input_llm = f"""
        Extract all entites from this chunk of text, return as a json:
        ### Text:
        {text}
        """

        response = ollama.chat(model=MODEL, messages=[ #llama3
        {
        'role': 'user',
        'content': input_llm}])#, options={"temperature":.5}

        output = response['message']['content']

        # x = output.replace("<|end-output|>","")#output[output.find("<|end-output|>"):]
        # print(x)
        return output

    def extract_facts(text):
        schema = """ {"entity1": ["fact1", "fact2"]}"""
        # input_llm = f"""{json.dumps(json.loads(schema), indent=4)}

        """    Using the following list of entities:
        {entities}
        """

        input_llm = f"""
        Collect all the atomic propositions about the entities in this list and put them in a json of the following form, returning only this json. Word each fact such that is uses the entity as the first word in the sentence:
        {json.dumps(json.loads(schema), indent=4)}

        Here's the text:

        {text}
        """
        #dolphin-llama3
        response = ollama.chat(model=MODEL, messages=[ #llama3
        {
        'role': 'user',
        'content': input_llm}])#, options={"temperature":.5}

        output = response['message']['content']

        # x = output.replace("<|end-output|>","")#output[output.find("<|end-output|>"):]
        # print(x)
        return output


    return (extract_facts,)


@app.cell
def _():
    from langchain_text_splitters import RecursiveCharacterTextSplitter 


    chunk_size = 1000
    splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=1000,
        chunk_overlap=int( chunk_size * 0.1),
        length_function=len,
        is_separator_regex=False,
    )
    # Split the content into chunks
    # chunks = splitter.chunks(content)



    return (splitter,)


@app.cell
def _():
    all_text = open(r"docs\rando.txt", encoding="utf8").read()
    return (all_text,)


@app.cell
def _(all_text, splitter):
    chunks = splitter.split_text(all_text)
    print(chunks[1])
    return (chunks,)


@app.cell
def _(chunks, extract_facts):
    # ents = extract_entities(chunks[0])
    facts = extract_facts(chunks[0])
    # entities_json = json.loads(ents[7t:-3])

    return (facts,)


@app.cell
def _(facts, json):
    facts_json = json.loads(facts[7:-3])

    return (facts_json,)


@app.cell
def _(facts_json):
    facts_json
    return


@app.cell
def _():
    """
    1. extract all entities, use coreference resolution
    2. Resolve entities
        1. check for plurality? string matching
        2. cosine similarity of embedding



    [17`68yxdj17g] = ["[viral biology]" , "[the study of viruses]"]


    1. "[viral biology] is a branch of [biology]"
    2.                             "[Biology] is the science that studies life"

    3. [Virology] is a branch of "the science that studies life"

    """
    return


@app.cell
def _(entities_json):
    import pytholog as pl
    bio_kb = pl.KnowledgeBase("biology")
    fs = [f"type({x['entity']}, { x['type']})".lower() for x in entities_json['entities']]
    bio_kb(fs)
    print(fs)
    return


if __name__ == "__main__":
    app.run()
