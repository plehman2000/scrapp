import marimo

__generated_with = "0.6.25"
app = marimo.App(width="medium")


@app.cell
def __():
    # from modules.ingest_docs import search_db, ingest_document_prototype, scrapp_db, file_name_db
    # # ingest_document_prototype("./test_inputs/info1.txt")
    # # search_db("Kamala D. Harris")
    # # need something to scan db and collect entities that are the same
    # import PyPDF2
    # import re

    # def extract_text_from_pdf(pdf_path):
    #     # Open the PDF file
    #     with open(pdf_path, 'rb') as file:
    #         # Create a PDF reader object
    #         pdf_reader = PyPDF2.PdfReader(file)

    #         # Initialize an empty string to store the extracted text
    #         extracted_text = ""

    #         # Iterate through each page in the PDF
    #         for page in pdf_reader.pages:
    #             # Extract text from the page
    #             page_text = page.extract_text()

    #             # Remove any potential table-like structures
    #             # This regex looks for patterns of repeated whitespace that might indicate a table
    #             page_text = re.sub(r'\s{2,}', ' ', page_text)

    #             # Append the cleaned text to our result
    #             extracted_text += page_text + "\n\n"

    #     return extracted_text.strip()

    # pdf_path = ".\documents\mctb2.pdf"
    # text = extract_text_from_pdf(pdf_path)
    # print(text)
    # from text_chunker import TextChunker

    # with open("./documents/info1.txt", 'r', encoding='utf-8') as file:
    #     text = file.read()

    # from textsplitter import TextSplitter


    # text_splitter = TextSplitter(max_token_size=200, end_sentence=True, preserve_formatting=True,
    #                              remove_urls=True, replace_entities=True, remove_stopwords=True, language='english')

    # chunks = text_splitter.split_text(text)

    # for i, chunk in enumerate(chunks):
    #     print(f"Chunk {i + 1}:\n{chunk}")



    # from rapidfuzz import fuzz
    # all_docs = scrapp_db.all()
    # all_subjects = [doc['subject'] for doc in all_docs]
    # # for s in all_subjects:
    # #     print(s)
    # entity_to_mathc = "Kamala Harris"
    # all_subjects = sorted(all_subjects, key=lambda x: fuzz.partial_ratio(entity_to_mathc,x), reverse=True)
    # print(all_subjects)
    return


@app.cell
def __():
    import marimo as mo
    return mo,


@app.cell
def __(mo):
    mo.md("# Pronoun Algorithm")
    return


@app.cell
def __():
    from nltk import tokenize
    f =  """Mindfulness is in a category all by itself, as it can potentially balance and perfect the remaining four spiritual faculties. This does not mean that we shouldn’t be informed by the other
    two pairs, but that mindfulness is extremely important. Mindfulness means knowing what is
    as it is right now. It is the quality of mind that knows things as they are. Really, it is the quality of sensations manifesting as they are, where they are, and on their own. However, initially
    it appears to be something we create and cultivate, and that is okay for the time being.4
     If you
    are trying to perceive the sensations that make up your experience clearly and to know what
    they are, you are balancing energy and concentration, and faith and wisdom. Due to energy, the
    mind is alert and attentive. Due to concentration, it is stable. Faith here may also mean acceptance, and wisdom here is clear comprehension.
    Notice that this has nothing to do with some vague spacing out in which we wish that reality
    would go away and our thoughts would never arise again. I don’t know where people get the
    notion that vague and escapist aversion to experience and thought are related to insight practice, but it seems to be a common one. Mindfulness means being very clear about our human,
    mammalian reality as it is. It is about being here now. Truth is found in the ordinary sensations
    that make up our experience. If we are not mindful of them or reject them because we are looking for “progress”, “depth”, or “transcendence”, we will be unable to appreciate what they have
    to teach, and be unable to do insight practices.
    The fve spiritual faculties have also been presented in another order that can be useful:
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
    combination of the frst four produces fundamental wisdom. Wisdom leads to more faith, and
    the cycle goes around again.    The Waystone Inn lay in silence: and it was a silence of three parts."""
    sentences = tokenize.sent_tokenize(f)
    return f, sentences, tokenize


@app.cell
def __():
    import spacy
    nlp = spacy.load("en_core_web_trf")
    return nlp, spacy


@app.cell
def __(nlp):
    import networkx as nx
    import uuid
    def generate_ast(sentence):
        doc = nlp(sentence)
        ast = nx.DiGraph()
        def traverse_tree(node):
            nonlocal ast
            for child in node.children:
                ast.add_edge(node.text + f"_{node.i}", child.text + f"_{child.i}", edge_label=str(child.dep_))
                ast.nodes[node.text + f"_{node.i}"]['pos'] = node.pos_
                ast.nodes[child.text + f"_{child.i}"]['pos'] = child.pos_

                traverse_tree(child)
        root = [token for token in doc if token.head == token][0]
        ast.add_node(root.text + f"_{root.i}", pos=root.pos_)
        traverse_tree(root)
        return ast





    import networkx as nx
    import matplotlib.pyplot as plt

    def visualize_ast(ast, title="Abstract Syntax Tree (AST)"):
        # Set up the plot
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(ast, k=0.9, iterations=50)

        # Calculate dynamic sizes based on the number of nodes
        num_nodes = len(ast.nodes)
        node_size = max(300, min(3000, 8000 / num_nodes))
        font_size = max(6, min(12, 24 / (num_nodes ** 0.3)))

        # Draw nodes
        nx.draw_networkx_nodes(ast, pos, node_size=node_size, node_color="lightblue")

        # Draw edges
        nx.draw_networkx_edges(ast, pos, edge_color="gray", arrows=True, arrowsize=20)

        # Draw labels
        nx.draw_networkx_labels(ast, pos, font_size=font_size, font_weight="bold")

        # Draw edge labels
        edge_labels = nx.get_edge_attributes(ast, 'edge_label')
        nx.draw_networkx_edge_labels(ast, pos, edge_labels=edge_labels, font_size=font_size-2)

        # Set title and turn off axis
        plt.title(title, fontsize=16)
        plt.axis("off")

        # Adjust layout and display
        plt.tight_layout()
        plt.show()
    return generate_ast, nx, plt, uuid, visualize_ast


@app.cell
def __():
    # def combine_compound_nodes(ast):
    #     # Create a copy of the graph to modify
    #     new_ast = ast.copy()

    #     # Find all compound edges between proper nouns
    #     compound_edges = [(u, v) for u, v, data in new_ast.edges(data=True)
    #                       if data.get('edge_label') == 'compound'
    #                       and new_ast.nodes[u].get('pos') == 'PROPN'
    #                       and new_ast.nodes[v].get('pos') == 'PROPN']

    #     # Create a subgraph of compound relationships
    #     compound_graph = nx.Graph(compound_edges)

    #     # Find connected components (groups of related compound nouns)
    #     compound_groups = list(nx.connected_components(compound_graph))

    #     # Process each group
    #     for group in compound_groups:
    #         # Sort nodes in the group by their original index in the sentence
    #         sorted_group = sorted(group, key=lambda x: int(x.split('_')[-1]))

    #         # Create new node name
    #         new_node_name = " ".join([node.split('_')[0] for node in sorted_group])
    #         new_node = f"{new_node_name}_{uuid.uuid4().hex[:8]}"

    #         # Add the new node
    #         new_ast.add_node(new_node, pos='PROPN')

    #         # Redirect incoming edges
    #         for node in sorted_group:
    #             for predecessor in new_ast.predecessors(node):
    #                 if predecessor not in group:
    #                     edge_data = new_ast.get_edge_data(predecessor, node)
    #                     new_ast.add_edge(predecessor, new_node, **edge_data)

    #         # Redirect outgoing edges
    #         for node in sorted_group:
    #             for successor in new_ast.successors(node):
    #                 if successor not in group:
    #                     edge_data = new_ast.get_edge_data(node, successor)
    #                     new_ast.add_edge(new_node, successor, **edge_data)

    #         # Remove old nodes
    #         for node in sorted_group:
    #             new_ast.remove_node(node)

    #     return new_ast
    # ast = generate_ast(sentences[-1])
    # ast = combine_compound_nodes(ast)
    return


@app.cell
def __(generate_ast, sentences):
    sent = sentences[-1]
    sent = "The Waystone house lay in silence: and it was a silence of three parts."
    ast = generate_ast(sent)
    return ast, sent


@app.cell
def __(ast, sent):
    # def combine_compound_nodes(ast):
    #     # Create a copy of the graph to modify
    #     new_ast = ast.copy()
    #     print(new_ast.edges)
    #     return new_ast


    # ast = combine_compound_nodes(ast)

    new_ast = ast.copy()
    print(sent)
    edge_data = new_ast.edges(data=True)
    for edge in edge_data:
        # print(edge)
        # conditionals
        match edge[2]['edge_label']:
            case 'compound':
                print(edge)
                # TODO basically add nodees to each other, continuously combine nodes until no change in sentence
                if ast.nodes[edge[0]]['pos'] == "NOUN" or ast.nodes[edge[0]]['pos'] == "PROPN":
                    # print(ast.nodes[edge[1]])
                    if ast.nodes[edge[1]]['pos'] == "NOUN" or ast.nodes[edge[1]]['pos'] == "PROPN":
                        word1_and_index = [edge[0][:edge[0].rfind('_', 0, len(edge[0])-1)],edge[0][edge[0].rfind('_', 0, len(edge[0])-1):]]
                        word2_and_index = [edge[1][:edge[1].rfind('_', 0, len(edge[1])-1)],edge[1][edge[1].rfind('_', 0, len(edge[1])-1):]]
                        print(word1_and_index,word2_and_index)
                        #nodes should be combined

                        # create new node
                        
                        # get all edges pointing to nodes
                        edges_1 = ast.edges(edge[0])
                        edges_2 = ast.edges(edge[1])

                        #mak edges pointing to new node
                        for ed in edges_1:
                            print(ed)


                        #remove old edges

                # for node
    return (
        ed,
        edge,
        edge_data,
        edges_1,
        edges_2,
        new_ast,
        word1_and_index,
        word2_and_index,
    )


@app.cell
def __(new_ast, visualize_ast):
    visualize_ast(new_ast)
    return


@app.cell
def __():
    return


@app.cell
def __(nlp, sentences, spacy):
    from spacy.displacy import parse_deps
    sentence = sentences[-1]
    doc = nlp(sentence)
    print(sentence)
    for token in doc:
        print(token.text,"|", spacy.explain(token.pos_),"|", token.dep_,"| Ancestors: ",[[x.text,x.i,x.i+len(x.text_with_ws)] for x in list(token.children)])
    return doc, parse_deps, sentence, token


@app.cell
def __(doc, parse_deps, spacy):
    def process_deps_output(deps_output):
        words = deps_output['words']
        arcs = deps_output['arcs']
        for arc in arcs:
            start_word = words[arc['start']]['text']
            end_word = words[arc['end']]['text']
            dependency = f"{start_word} -> {end_word}"
            label = spacy.explain(arc['label'])
            # Add the 'dependency' key to each arc dictionary
            arc['label'] = label
            arc['dependency'] = dependency
        return deps_output

    deps_output = parse_deps(doc)
    enhanced_output = process_deps_output(deps_output)
    for arc in enhanced_output['arcs'][:5]:
        # print(f"Label: {arc['label']}, Dependency: {arc['dependency']}")
        print(arc)
    return arc, deps_output, enhanced_output, process_deps_output


@app.cell
def __(enhanced_output):
    # Print the enhanced output to verify
    enhanced_output['words'][0]
    return


if __name__ == "__main__":
    app.run()
