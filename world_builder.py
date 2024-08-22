import marimo

__generated_with = "0.6.25"
app = marimo.App(width="medium")


@app.cell
def __():
    import ollama
    def extract_info(text):

        PROMPT = f"""<|im_start|>system
    You are a helpful assistant. Your task is to translate natural language statements about family relationships into a list of facts and rules for a knowledge base.
     Provide only the list, without additional explanations.
    <|im_end|>

    <|im_start|>user
    Translate the following sentences into a list of facts and rules for a knowledge base:

    {text}
    Format your response as a list, with each item starting with a hyphen (-). Include both facts and rules. 
    Use the format "predicate(subject, object)" for facts and "conclusion :- condition1, condition2" for rules.
    <|im_end|>"""


        response = ollama.chat(model='llama3.1', messages=[ #llama3
        {
        'role': 'user',
        'content': PROMPT}])#, options={"temperature":.5}

        output = response['message']['content']

        return output
    # out = extract_info(input_sentence)

    # text = "Alice is married to Bob, Alice and Bob have two children: Charlie and Diana, Charlie is 10 years old and Diana is 8 years old, Bob's parents are Edward and Fiona."
    # print(extract_info(text))





    import json

    def to_pytholog(text):
        schema = {
            "": [
                ["", ""]
            ]
        }

        template = json.dumps(schema, indent=4)
        input_llm = f"""
        Extract relationships from the text, transforming each relationship into a knowledge base entry in the format you provided. 
        The output should consist of valid predicates with corresponding arguments. Ensure that every entity and relationship is correctly formatted, 
        returning a comma separated list of strings. Only reply with this list.


        ### Example:
        ### Text:
        -Diana has two parents :- Alice, Bob
        ### Response (produce the response in the format below):
        parent(Alice, Diana),
        parent(Bob, Diana)

        ### Text:
        {text}
        """

        response = ollama.chat(model='nuextract', messages=[{
            'role': 'user',
            'content': input_llm
        }])

        output = response['message']['content']
        return output.replace("<|end-output|>", "")





    import pytholog as pl

    def convert_facts_to_pytholog_kb(facts):
        # Create a new knowledge base
        kb = pl.KnowledgeBase("KBase")

        # Convert the list of facts into a Prolog-like format suitable for Pytholog
        formatted_facts = [fact.strip() + '.' for fact in facts]

        # Add the facts to the knowledge base
        kb(formatted_facts)

        return kb
    return (
        convert_facts_to_pytholog_kb,
        extract_info,
        json,
        ollama,
        pl,
        to_pytholog,
    )


@app.cell
def __(ollama):



    def NL_to_pylog_query(text):

        log_prompt = f"""You are an AI designed to convert natural language statements into queries that can be executed on a Pytholog knowledge base. The knowledge base contains facts and relationships, such as family connections, ages, and other personal information.
        Guidelines:
        
        Identify the entities and relationships described in the natural language statement.
        Map them to the appropriate predicates and variables in the Pytholog query.
        Ensure the query is syntactically correct and can be executed directly within a Pytholog environment.
        Given a natural language statement, generate the corresponding Pytholog query.
        Only return the query
        
        Examples:
        
        Input: "Who are the parents of Charlie?"
        Output: parent(X, Charlie)
        
        Input: "What is Diana's age?"
        Output: age(Diana, X)
        
        Input: "List all children of Alice."
        Output: parent(Alice, X)
        
        Input: "Who is Bob's father?"
        Output: father(X, Bob)
        

        Input:
        {text}
        
        Output:"""


        response = ollama.chat(model='llama3.1', messages=[ #llama3
        {
        'role': 'user',
        'content': log_prompt}])#, options={"temperature":.5}

        output = response['message']['content']

        return output

        
    return NL_to_pylog_query,


@app.cell
def __(to_pytholog):
    # Example input
    input_text = """
    - Alice is married to Bob.
    - Charlie is a child of Alice and Bob.
    - Diana is a child of Alice and Bob.
    - The age of Charlie is 10 years old.
    - The age of Diana is 8 years old.
    - Edward is the father of Bob.
    - Fiona is the mother of Bob.
    - Charlie has two parents :- Alice, Bob
    - The age of Adam is 12 years old.
    - Diana has two parents :- Alice, Bob
    """



    # Extracted information
    extracted_info = to_pytholog(input_text)
    print(extracted_info)

    d = ")"
    facts = []
    for line in extracted_info.split("),"):
        line = line.replace("\n", "")
        line = line.replace(" ", "")
        s =  [e+d for e in line.split(d) if e][0]
        facts.append(s)
    return d, extracted_info, facts, input_text, line, s


@app.cell
def __(convert_facts_to_pytholog_kb, facts):
    knowledge_base = convert_facts_to_pytholog_kb(facts)
    print(knowledge_base)
    return knowledge_base,


@app.cell
def __(NL_to_pylog_query):
    query = NL_to_pylog_query("How old  is diana?")
    print(query)
    return query,


@app.cell
def __(knowledge_base, pl, query):
    knowledge_base.query(pl.Expr(query), cut=True)
    return


@app.cell
def __(knowledge_base, pl):
    # Query the age of a person, e.g., Charlie
    result = knowledge_base.query(pl.Expr("age(Diana, X)"))

    # Output the result
    print(result)

    return result,


if __name__ == "__main__":
    app.run()
