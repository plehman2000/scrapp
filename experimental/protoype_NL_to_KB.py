import marimo

__generated_with = "0.6.25"
app = marimo.App(width="medium")


@app.cell
def __():

    # def extract_info(text):

    #     PROMPT = f"""<|im_start|>system
    # You are a helpful assistant. Your task is to filter and translate useful natural language statements into a list of facts and rules for a knowledge base. The output should convey meaningful information on it's own. If this cannot be done, return an empty message, otherwise provide only the list, without additional explanations. For example:
    # Input: Alice is married to Bob and they have three lovely kids
    # Output: 
    # Alice and Bob are married
    # Alice has three kids
    # Translate the following sentences into a list of facts and rules for a knowledge base:
    # {text}
    # Format your response as a list, with each item starting with a hyphen (-). Include both facts and rules. 
    # <|im_end|>"""


    #     response = ollama.chat(model='llama3.1:8b', messages=[ #llama3
    #     {
    #     'role': 'user',
    #     'content': PROMPT}])#, options={"temperature":.5}

    #     output = response['message']['content']

    #     return output
    # # out = extract_info(input_sentence)

    # # text = "Alice is married to Bob, Alice and Bob have two children: Charlie and Diana, Charlie is 10 years old and Diana is 8 years old, Bob's parents are Edward and Fiona."
    # # print(extract_info(text))





    # def to_pytholog(text):
    #     input_llm = f"""
    #     Extract relationships from the text, transforming each relationship into a knowledge base entry in the format you provided. 
    #     The output should consist of valid predicates with corresponding arguments. Ensure that every entity and relationship is correctly formatted, 
    #     returning a comma separated list of strings. Only reply with this list.


    #     ### Example:
    #     ### Text:
    #     -Diana has two parents, Alice and Bob
    #     ### Response (produce the response in the format below):
    #     parent(Alice, Diana),
    #     parent(Bob, Diana)

    #     ### Text:
    #     {text}
    #     """

    #     response = ollama.chat(model='llama3.1:8b', messages=[{
    #         'role': 'user',
    #         'content': input_llm
    #     }])

    #     output = response['message']['content']
    #     return output.replace("<|end-output|>", "")


    # import pytholog as pl

    # def convert_facts_to_pytholog_kb(facts):
    #     # Create a new knowledge base
    #     kb = pl.KnowledgeBase("KBase")

    #     # Convert the list of facts into a Prolog-like format suitable for Pytholog
    #     formatted_facts = [fact.strip() + '.' for fact in facts]

    #     # Add the facts to the knowledge base
    #     kb(formatted_facts)

    #     return kb
    return


@app.cell
def __(mo):
    mo.md("# Prototype 1")
    return


@app.cell
def __(mo):
    mo.md("## Part 1: Natural Language to Facts/relations")
    return


@app.cell
def __(json, ollama):
    def extract_relations_formatted(text):

        input_llm = """
        Please extract all relations betweens proper nouns and predicates. Valid relations are verbs like is/has/created/taken etc. THE SUBJECT + RELATION PREDICATE should form a complete sentence as close to how it appears in the text as possible
        ### Template:
         {
          "facts": [
             {
              "subject": "",
              "verb": "",
              "predicate": ""
             },
             {
              "subject": "",
              "verb": "",
              "predicate": ""
             }
          ]
         }
        
        ### Example:
         {
          "facts": [
             {
              "subject": "Adriaan van Wijngaarden",
              "verb": "employed",
              "predicate": "Dijkstra as the first computer programmer in the Netherlands at the Mathematical Centre in Amsterdam (1952-1962)"
             },
             {
              "subject": "Dijkstra",
              "verb": "formulated",
              "predicate": "the shortest path problem in 1956"
             }
             {
              "subject": "Dijkstra",
              "verb": "solved",
              "predicate": "the shortest path problem in 1956"
             }
                      {
              "subject": "John",
              "verb": "is",
              "predicate": "reknowned for his Computer Science contributions"
             }
          ]
         }
        
        ### Text:
        """

        response = ollama.chat(model='llama3.1:8b',
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
        
            
        return output


    return extract_relations_formatted,


@app.cell
def __(chunks, ollama):
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
            model='llama3.1:8b'
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
        - Verb: Choose a verb that captures the primary action or state described in the fact.
        - Object: Fill in the object with key details from the original fact.
        
        All facts should be formatted as grammatically correct, complete sentences. If needed, split sentences 
        into smaller ones to maintain clarity and accuracy.
        
        Instructions: Apply this structure to each fact in the list, always following noun -> verb -> object. 
        Ensure the rewritten facts are clear, accurate, and maintain the essence of the original information.
        
        """
        
        response = ollama.chat(
        model='llama3.1:8b'
        # model='gemma2:27b'
        , messages=[ #llama3
        {
        'role': 'user',
        'content': prompt + facts}])
        output = response['message']['content']
        return output


    def chunk_to_ents(text):
        entities = set()
        result = get_entities(text)
        [entities.add(r) for r in result]
        entities = list(entities)
        facts = llm_chunks_to_facts( chunks)
        all_out = [p['facts'] for p in facts]
        return sum(all_out, [])






    sample = """Born in Rotterdam, the Netherlands, Dijkstra studied mathematics and physics and then theoretical physics at the University of Leiden. Adriaan van Wijngaarden offered him a job as the first computer programmer in the Netherlands at the Mathematical Centre in Amsterdam, where he worked from 1952 until 1962. He formulated and solved the shortest path problem in 1956, and in 1960 developed the first compiler for the programming language ALGOL 60 in conjunction with colleague Jaap A. Zonneveld. In 1962 he moved to Eindhoven, and later to Nuenen, where he became a professor in the Mathematics Department at the Technische Hogeschool Eindhoven. In the late 1960s he built the THE multiprogramming system, which influenced the designs of subsequent systems through its use of software-based paged virtual memory. Dijkstra joined Burroughs Corporation as its sole research fellow in August 1973. The Burroughs years saw him at his most prolific in output of research articles. He wrote nearly 500 documents in the "EWD" series, most of them technical reports, for private circulation within a select group.

    Dijkstra accepted the Schlumberger Centennial Chair in the Computer Science Department at the University of Texas at Austin in 1984, working in Austin, Texas, until his retirement in November 1999. He and his wife returned from Austin to his original house in Nuenen, where he died on 6 August 2002 after a long struggle with cancer.[3]

    He received the 1972 Turing Award for fundamental contributions to developing structured programming languages. Shortly before his death, he received the ACM PODC Influential Paper Award in distributed computing for his work on self-stabilization of program computation. This annual award was renamed the Dijkstra Prize the following year, in his honor. He was later killed for saying "nigger" in front of a live studio audience"""


    sample = """The Catholic Church, also known as the Roman Catholic Church, is the largest Christian church, with 1.28 to 1.39 billion baptized Catholics worldwide as of 2024.[4][5][9] It is among the world's oldest and largest international institutions and has played a prominent role in the history and development of Western civilization.[10][11][12][13] The church consists of 24 sui iuris churches, including the Latin Church and 23 Eastern Catholic Churches, which comprise almost 3,500[14] dioceses and eparchies located around the world. The pope, who is the bishop of Rome, is the chief pastor of the church.[15] The Diocese of Rome, known as the Holy See, is the central governing authority of the church. The administrative body of the Holy See, the Roman Curia, has its principal offices in Vatican City, a small independent city-state and enclave within the Italian capital city of Rome, of which the pope is head of state.

    The core beliefs of Catholicism are found in the Nicene Creed. The Catholic Church teaches that it is the one, holy, catholic and apostolic church founded by Jesus Christ in his Great Commission,[16][17][note 1] that its bishops are the successors of Christ's apostles, and that the pope is the successor to Saint Peter, upon whom primacy was conferred by Jesus Christ.[20] It maintains that it practises the original Christian faith taught by the apostles, preserving the faith infallibly through scripture and sacred tradition as authentically interpreted through the magisterium of the church.[21] The Roman Rite and others of the Latin Church, the Eastern Catholic liturgies, and institutes such as mendicant orders, enclosed monastic orders and third orders reflect a variety of theological and spiritual emphases in the church.[22][23]"""

    return (
        chunk_to_ents,
        get_entities,
        json,
        llm_chunks_to_facts,
        llm_facts_to_formatted_facts,
        sample,
        spacy,
    )


@app.cell
def __(
    extract_relations_formatted,
    llm_chunks_to_facts,
    llm_facts_to_formatted_facts,
    sample,
):
    facts = llm_chunks_to_facts(sample)
    formatted_facts = llm_facts_to_formatted_facts(facts)
    relations = extract_relations_formatted(formatted_facts)
    # print(facts)
    # print(formatted_facts)
    print(relations)

    return facts, formatted_facts, relations


if __name__ == "__main__":
    app.run()
