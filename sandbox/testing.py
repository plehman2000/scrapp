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

    import marimo as mo
    return mo,


@app.cell
def __(mo):
    mo.md("# Pronoun Algorithm")
    return


@app.cell
def __():
    import spacy
    nlp = spacy.load("en_core_web_lg")
    return nlp, spacy


@app.cell
def __(nlp):
    import networkx as nx
    def generate_ast(sentence):
        doc = nlp(sentence)
        ast = nx.DiGraph()
        def traverse_tree(node):
            nonlocal ast
            for child in node.children:
                ast.add_edge(node.text.replace("|", " "), child.text.replace("|", " "), pos=node.pos_,edge_label = str(child.dep_))
                traverse_tree(child)

        root = [token for token in doc if token.head == token][0]
        ast.add_node(root.text.replace("|", " "))
        traverse_tree(root)

        return ast





    import networkx as nx
    import matplotlib.pyplot as plt
    def visualize_ast(ast):
        pos = nx.spring_layout(ast)

        plt.figure(figsize=(10, 10))
        edge_labels = nx.get_edge_attributes(ast, 'edge_label')

        num_nodes = len(ast.nodes)
        node_size = 4000 / num_nodes  # Adjust the constant multiplier as needed
        font_size = 36 / (num_nodes ** 0.5)  # Adjust the constant divisor as needed
        nx.draw_networkx(
            ast, with_labels=True, node_size=node_size, node_color="lightblue", font_size=font_size,pos=pos,arrows=True
        )
        nx.draw_networkx_edge_labels(ast, pos, edge_labels=edge_labels)
        plt.title("Abstract Syntax Tree (AST)")
        plt.axis("off")
        plt.show()
    return generate_ast, nx, plt, visualize_ast


@app.cell
def __(generate_ast):
    ast = generate_ast("The Waystone Inn lay in silence: and it was a silence of three parts.")
    return ast,


@app.cell
def __(ast, visualize_ast):
    visualize_ast(ast)

    return


@app.cell
def __():
    from nltk import tokenize
    f = open(".\documents\info2.txt").read()
    sentences = tokenize.sent_tokenize(f)

    return f, sentences, tokenize


@app.cell
def __(sentences):
    sentences
    return


if __name__ == "__main__":
    app.run()
