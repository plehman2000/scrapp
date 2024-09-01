import marimo

__generated_with = "0.6.25"
app = marimo.App(width="medium")


@app.cell
def __():
    import ollama
    import marimo as mo
    def extract_info(text):

        PROMPT = f"""<|im_start|>system
    You are a helpful assistant. Your task is to filter and translate useful natural language statements into a list of facts and rules for a knowledge base. The output should convey meaningful information on it's own. If this cannot be done, return an empty message, otherwise provide only the list, without additional explanations. For example:
    Input: Alice is married to Bob and they have three lovely kids
    Output: 
    Alice and Bob are marruied
    Alice has three kids

    Translate the following sentences into a list of facts and rules for a knowledge base:
    {text}
    Format your response as a list, with each item starting with a hyphen (-). Include both facts and rules. 
    <|im_end|>"""


        response = ollama.chat(model='llama3.1:8b', messages=[ #llama3
        {
        'role': 'user',
        'content': PROMPT}])#, options={"temperature":.5}

        output = response['message']['content']

        return output
    # out = extract_info(input_sentence)

    # text = "Alice is married to Bob, Alice and Bob have two children: Charlie and Diana, Charlie is 10 years old and Diana is 8 years old, Bob's parents are Edward and Fiona."
    # print(extract_info(text))





    def to_pytholog(text):
        input_llm = f"""
        Extract relationships from the text, transforming each relationship into a knowledge base entry in the format you provided. 
        The output should consist of valid predicates with corresponding arguments. Ensure that every entity and relationship is correctly formatted, 
        returning a comma separated list of strings. Only reply with this list.


        ### Example:
        ### Text:
        -Diana has two parents, Alice and Bob
        ### Response (produce the response in the format below):
        parent(Alice, Diana),
        parent(Bob, Diana)

        ### Text:
        {text}
        """

        response = ollama.chat(model='llama3.1:8b', messages=[{
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
        mo,
        ollama,
        pl,
        to_pytholog,
    )


@app.cell
def __(mo):
    mo.md("# Prototype 1")
    return


@app.cell
def __(tqdm):
    import PyPDF2
    import os
    def read_pdf(file_path):
        content = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in tqdm(pdf_reader.pages):
                content += page.extract_text()
        return content


    return PyPDF2, os, read_pdf


@app.cell
def __(ollama):
    from langchain_text_splitters import RecursiveCharacterTextSplitter 
    import spacy
    import json
    from tqdm import tqdm
    def split_text(text, max_tokens=100, overlap_ratio=0.50):
            splitter = RecursiveCharacterTextSplitter(
                # Set a really small chunk size, just to show.
                chunk_size=max_tokens,
                chunk_overlap=int(max_tokens * overlap_ratio),
                length_function=len,
                is_separator_regex=False,
                separators=[
            "\n\n",
            "\n",
            " ",
            ".",
            ",",]
            )
            chunks = splitter.split_text(text)
            return chunks


    def get_entities(text):


        nlp = spacy.load("en_core_web_trf")
        doc = nlp(text)
        
        entities = [ent.text for ent in doc.ents 
                    if ent.label_ not in ["MONEY", "TIME", "DATE", "CARDINAL", "PERCENT", "QUANTITY"]]
        
        return entities



    def llm_chunks_to_facts(entities, chunks):
        raw_facts = []
        for i,chunk in enumerate(tqdm(chunks)):
            prompt = """  Return individual facts that can be intererpreted context-free and independently from from the following text in ONLY this JSON format: {"facts": ["fact", "fact"]}. One key named 'facts', and a list of strings of facts. If no facts, only return {}. If I only looked at one fact from this requested list it should be meaningful.: """
            response = ollama.chat(model='llama3.1:8b', messages=[ #llama3
            {
            'role': 'user',
            'content': prompt + chunk}])
            output = response['message']['content']

            try:
                parsed_output = json.loads(output)
                raw_facts.append(parsed_output)
            except json.JSONDecodeError as json_error:
                print(f"JSON parsing error in chunk {i}: {json_error}")
                # print(f"Problematic output: {output}")
            except Exception as e:
                print(f"Error processing chunk {i}: {e}")
            # if i > 5:
            #     break
        processed_facts = raw_facts
        return processed_facts
        
    def chunks_to_ents(text):
        chunks = split_text(text, max_tokens=300, overlap_ratio=0.2)
        # a filtering step needs to occur here, otherwise we get shit like "Click here to log in" as a sentence
        #presuming we filtered it:
        entities = set()
        for chunk in tqdm(chunks):
            result = get_entities(chunk)
            [entities.add(r) for r in result]
        entities = list(entities)
        facts = llm_chunks_to_facts(entities, chunks)
        all_out = [p['facts'] for p in facts]
        
        return sum(all_out, [])






    sample = """Born in Rotterdam, the Netherlands, Dijkstra studied mathematics and physics and then theoretical physics at the University of Leiden. Adriaan van Wijngaarden offered him a job as the first computer programmer in the Netherlands at the Mathematical Centre in Amsterdam, where he worked from 1952 until 1962. He formulated and solved the shortest path problem in 1956, and in 1960 developed the first compiler for the programming language ALGOL 60 in conjunction with colleague Jaap A. Zonneveld. In 1962 he moved to Eindhoven, and later to Nuenen, where he became a professor in the Mathematics Department at the Technische Hogeschool Eindhoven. In the late 1960s he built the THE multiprogramming system, which influenced the designs of subsequent systems through its use of software-based paged virtual memory. Dijkstra joined Burroughs Corporation as its sole research fellow in August 1973. The Burroughs years saw him at his most prolific in output of research articles. He wrote nearly 500 documents in the "EWD" series, most of them technical reports, for private circulation within a select group.

    Dijkstra accepted the Schlumberger Centennial Chair in the Computer Science Department at the University of Texas at Austin in 1984, working in Austin, Texas, until his retirement in November 1999. He and his wife returned from Austin to his original house in Nuenen, where he died on 6 August 2002 after a long struggle with cancer.[3]

    He received the 1972 Turing Award for fundamental contributions to developing structured programming languages. Shortly before his death, he received the ACM PODC Influential Paper Award in distributed computing for his work on self-stabilization of program computation. This annual award was renamed the Dijkstra Prize the following year, in his honor."""

    chem_sample = """
    1
    Department of Radiation Oncology, Cancer Institute of Jiangsu University, Affiliated Hospital of Jiangsu University, Zhenjiang 212000 Jiangsu, China. 2
    Department of Thoracic
    Surgery, Affiliated Hospital of Jiangsu University, Zhenjiang 212000 Jiangsu, China. ✉email: 1000011360@ujs.edu.cn; wangxu@ujs.edu.cn
    Cancer Gene Therapy www.nature.com/cgt
    1234567890();,:
    it is in an active state, and when it binds to GDP, it is in an inactive
    state. KRAS, in its active state, binds to GTP and has an intrinsic
    enzymatic activity to cleave the terminal phosphate of nucleotides, converting it to GDP. Its conversion rate is usually slow but
    can be significantly increased with the assistance of Guanosine
    triphosphatase-activating protein (GAP). Meanwhile, KRAS can
    bind to guanine nucleotide exchange factors (GEFs) (such as SOS),
    causing the bound nucleotide (GDP) to be released and binding of
    KRAS to GTP [8]. In normal mammalian cells, endogenous KRAS
    protein mainly exists in an inactive state. However, the oncogenic
    mutation of KRAS protein interferes with GTP hydrolysis, causing
    the protein to remain in an active GTP state and continuously
    transmit signals to the downstream pathway to recruit and
    activate the proteins required for growth factor and other
    receptors (such as RAF and PI3K) signal transduction [8].
    Furthermore, with the deepening research in recent years, the
    focus of gene studies has shifted toward non-coding RNAs that
    play regulatory roles. Among them, long non-coding RNAs
    (lncRNAs) are a class of non-coding transcripts with a length
    exceeding 200 nucleotides (nt), and involved in many physiological and pathological processes. Yang et al. reported on HIF1AAs2, a KRAS-responsive long non-coding RNA (lncRNA), confirming
    its positive correlation with KRAS through RT-qPCR. Further
    experiments revealed that HIF1A-As2 guides a key member of
    the DExD/H-box helicase family, DHX9, to the promoter region of
    the oncogenic transcription factor gene MYC, thereby enhancing
    MYC signaling transduction. Activated MYC further promotes cell
    proliferation and migration in KRAS-driven NSCLC. Simultaneously,
    KRAS, through MYC, promotes HIF1A-As2, forming a positive
    feedback loop [9]. MicroRNAs (miRNAs) are another important
    class of non-coding RNAs that play a role in gene regulation by
    degrading mRNA or inhibiting translation. Shi et al. used NanoString technology and Real-time PCR to identify the most
    upregulated microRNAs (miR-30c and miR-21) in cells overexpressing KRASWT and KRASG12D. Through experiments, they
    demonstrated that miR-30c downregulates BID, NF1, RASA1, and
    RASSF8 at the transcriptional level, while miR-21 inhibits the
    protein expression of RASA1 and RASSF8 to contributes to
    tumorigenesis [10]."""



    return (
        RecursiveCharacterTextSplitter,
        chem_sample,
        chunks_to_ents,
        get_entities,
        json,
        llm_chunks_to_facts,
        sample,
        spacy,
        split_text,
        tqdm,
    )


@app.cell
def __(spacy):
    import numpy as np
    from thefuzz import fuzz
    # Load the SpaCy model with word vectors
    nlp = spacy.load("en_core_web_lg")

    def get_embeddings(text):
        # Process the text with SpaCy
        doc = nlp(text)
        # Return the vector representation of the text
        return doc.vector



    def get_similarity(a,b):
        dot_product = sum(x*y for x, y in zip(a, b))
        
        # Calculate the magnitude of each vector
        magnitude_A = sum(x*x for x in a)**0.5
        magnitude_B = sum(x*x for x in b)**0.5
        
        # Compute cosine similarity
        cosine_similarity = dot_product / (magnitude_A * magnitude_B)

        return cosine_similarity
        # return np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
    return fuzz, get_embeddings, get_similarity, nlp, np


@app.cell
def __(chem_sample, chunks_to_ents, os, read_pdf):
    file_path = "./data/mutation_paper.pdf"

    def pdf_to_facts(file_path):
        _, file_extension = os.path.splitext(file_path)
        # Read the content based on file type
        if file_extension.lower() == '.pdf':
            text = read_pdf(file_path)
        output = chunks_to_ents(chem_sample)
        return output

    fact_dict = pdf_to_facts(file_path)
        
    print(fact_dict)
    return fact_dict, file_path, pdf_to_facts


@app.cell
def __():
    #Implement fuzzy srearchinbg and clustering!
    return


@app.cell
def __(mo):
    mo.md("# Pytholog direct translation")
    return


@app.cell
def __():
    return


@app.cell
def __(mo):
    mo.md(
        """
        def NL_to_pylog_query(text):

            log_prompt = f\"""You are an AI designed to convert natural language statements into queries that can be executed on a Pytholog knowledge base. The knowledge base contains facts and relationships, such as family connections, ages, and other personal information.
            Guidelines:

            Identify the entities and relationships described in the natural language statement.
            Map them to the appropriate predicates and variables in the Pytholog query.
            Ensure the query is syntactically correct and can be executed directly within a Pytholog environment.
            Given a natural language statement, generate the corresponding Pytholog query.
            Only return the query

            Examples:

            Input: "Who are the parents of Charlie?"
            Output: parent(parent, Charlie)

            Input: "What is Diana's age?"
            Output: age(age,Diana)

            Input: "List all children of Alice."
            Output: parent(Alice, X)

            Input: "Who is Bob's father?"
            Output: father(X, Bob)


            Input:
            {text}

            Output:\"""


            response = ollama.chat(model='llama3.1:8b', messages=[ #llama3
            {
            'role': 'user',
            'content': log_prompt}])#, options={"temperature":.5}

            output = response['message']['content']

            return output
        """
    )
    return


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
def __():
    from modules import sourcer_module
    return sourcer_module,


@app.cell
def __(sourcer_module):
    hsh, website_chunks = sourcer_module.get_webpage_info([r"https://en.wikipedia.org/wiki/Battle_of_Cer"])
    return hsh, website_chunks


@app.cell
def __(website_chunks):
    chunk = website_chunks[0][1][16]
    print(chunk)
    return chunk,


app._unparsable_cell(
    r"""
    # Maybe we need a targetted summary... we need users to, at least initially indicate what important things they care about from this source

    #Or we ask the model to do this:
    /*
    - Pick the best k entities from the text
    - Mechanically, liberally filter only to text that is more likely to mention ideas related to these entities(grab 3 sentences around each mention of each entity or something heuristic)
    - Repeatedly prompt llm to rewrite each entity
    */
    """,
    name="__"
)


@app.cell
def __():
    import marimo as mo
    return mo,


if __name__ == "__main__":
    app.run()
