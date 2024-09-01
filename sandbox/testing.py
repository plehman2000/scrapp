import marimo

__generated_with = "0.6.25"
app = marimo.App(width="medium")


@app.cell
def __():
    from modules.ingest_docs import search_db, ingest_document_prototype, scrapp_db, file_name_db
    # ingest_document_prototype("./test_inputs/info1.txt")
    # search_db("Kamala D. Harris")
    return file_name_db, ingest_document_prototype, scrapp_db, search_db


@app.cell
def __():
    # need something to scan db and collect entities that are the same
    return


@app.cell
def __():
    import PyPDF2
    import re

    def extract_text_from_pdf(pdf_path):
        # Open the PDF file
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)

            # Initialize an empty string to store the extracted text
            extracted_text = ""

            # Iterate through each page in the PDF
            for page in pdf_reader.pages:
                # Extract text from the page
                page_text = page.extract_text()

                # Remove any potential table-like structures
                # This regex looks for patterns of repeated whitespace that might indicate a table
                page_text = re.sub(r'\s{2,}', ' ', page_text)

                # Append the cleaned text to our result
                extracted_text += page_text + "\n\n"

        return extracted_text.strip()

    pdf_path = ".\documents\mctb2.pdf"
    text = extract_text_from_pdf(pdf_path)
    print(text)
    return PyPDF2, extract_text_from_pdf, pdf_path, re, text


@app.cell
def __():
    from text_chunker import TextChunker

    with open("./documents/info1.txt", 'r', encoding='utf-8') as file:
        text = file.read()

    from textsplitter import TextSplitter


    text_splitter = TextSplitter(max_token_size=200, end_sentence=True, preserve_formatting=True,
                                 remove_urls=True, replace_entities=True, remove_stopwords=True, language='english')

    chunks = text_splitter.split_text(text)

    for i, chunk in enumerate(chunks):
        print(f"Chunk {i + 1}:\n{chunk}")
    return (
        TextChunker,
        TextSplitter,
        chunk,
        chunks,
        file,
        i,
        text,
        text_splitter,
    )


@app.cell
def __(scrapp_db):
    from rapidfuzz import fuzz
    all_docs = scrapp_db.all()
    all_subjects = [doc['subject'] for doc in all_docs]
    # for s in all_subjects:
    #     print(s)
    entity_to_mathc = "Kamala Harris"
    all_subjects = sorted(all_subjects, key=lambda x: fuzz.partial_ratio(entity_to_mathc,x), reverse=True)
    print(all_subjects)
    return all_docs, all_subjects, entity_to_mathc, fuzz


@app.cell
def __():
    from stqdm import stqdm


    stqdm
    return stqdm,


@app.cell
def __():
    import html_text
    import os

    def extract_text_from_html_file(file_path, guess_layout=True):
        try:
            # Check if the file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"The file {file_path} does not exist.")

            # Open and read the HTML file
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Extract text from the HTML content
            extracted_text = html_text.extract_text(html_content, guess_layout=guess_layout)

            return extracted_text

        except FileNotFoundError as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"An error occurred while processing the file: {e}")
            return None

    # Example usage
    file_path = ".\documents\en.wikipedia.org_wiki_Edsger_W._Dijkstra__09a889b9-.html"

    # Extract text with layout guessing (default)
    text_with_layout = extract_text_from_html_file(file_path)
    if text_with_layout:
        print("Extracted text (with layout guessing):")
        print(text_with_layout[:500])  # Print first 500 characters
    return (
        extract_text_from_html_file,
        file_path,
        html_text,
        os,
        text_with_layout,
    )


@app.cell
def __(all_subjects):
    import json
    import ollama

    def identify_synonyms(terms):
        input_llm = """
        Please analyze the following list of terms and identify which terms are synonymous with each other. Return the result in the following JSON format. Each term can have at most one set of synonyms, and many terms may have no synonyms. Use the longest term as the "entity" and list its synonyms. If a term has no synonyms, include it as an entity with an empty list of synonyms.

        ### Template:
        {
          "synonym_groups": [
            {
              "entity": "",
              "synonyms": []
            },
            {
              "entity": "",
              "synonyms": ["", ""]
            }
          ]
        }

        ### Example:
        {
          "synonym_groups": [
            {
              "entity": "Barack Hussein Obama",
              "synonyms": ["B. Obama", "barack obama"]
            },
            {
              "entity": "Donald J. Trump",
              "synonyms": ["Trump"]
            },
            {
              "entity": "Joe Biden",
              "synonyms": ["Biden"]
            }
          ]
        }

        ### Terms:
        """

        terms_string = ", ".join(terms)

        response = ollama.chat(model='llama3.1:8b',
                               format="json",
                               messages=[
                                   {
                                       'role': 'user',
                                       'content': input_llm + terms_string
                                   }
                               ])

        output = response['message']['content']
        output = output.replace("<|end-output|>", "")

        try:
            parsed_output = json.loads(output)
        except json.JSONDecodeError as json_error:
            print(f"JSON parsing error: {json_error}")
            print(f"Problematic output: {output}")
            return None
        except Exception as e:
            print(f"Error processing output: {e}")
            return None

        return parsed_output

    # Example usage
    grouped_synonyms = identify_synonyms(all_subjects)

    print(json.dumps(grouped_synonyms, indent=2))
    return grouped_synonyms, identify_synonyms, json, ollama


@app.cell
def __():
    return


@app.cell
def __():
    from modules.db import search_db

    search_db("nigga")

    return search_db,


if __name__ == "__main__":
    app.run()
