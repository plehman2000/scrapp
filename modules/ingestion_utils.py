import requests
from typing import Dict, Any
from difflib import SequenceMatcher

def decode_google_scholar_response(paper: Dict[str, Any]) -> Dict[str, Any]:
    """
    Decode the Google Scholar API response for a single paper and extract relevant information.
    
    Args:
    paper (Dict[str, Any]): The paper data dictionary from the API response.
    
    Returns:
    Dict[str, Any]: A dictionary containing the decoded information.
    """
    publication_info = paper.get('publication_info', {})
    inline_links = paper.get('inline_links', {})
    cited_by = inline_links.get('cited_by', {})

    # Extract authors
    authors = publication_info.get('authors', [])
    author_names = [author.get('name') for author in authors] if isinstance(authors, list) else []

    # Extract year from summary if available
    summary = publication_info.get('summary', '')
    year = summary.split('-')[1].strip() if '-' in summary else 'N/A'

    decoded_info = {
        "paper": paper,
        "title": paper.get('title', 'N/A'),
        "authors": ', '.join(author_names) if author_names else 'N/A',
        "year": year,
        "citations": cited_by.get('total', 0),
        "url": paper.get('link', 'N/A'),
        "abstract": paper.get('snippet', 'N/A'),
        "type": paper.get('type', 'N/A'),
        "position": paper.get('position', 'N/A'),
        "result_id": paper.get('result_id', 'N/A')
    }

    return decoded_info


api_key = "b22b00a41c6fccc31a439f32361283540e1d39f6ea30ef0b06ed5e9d441b73e5"

def find_paper_by_name(paper_name: str, api_key = api_key) -> Dict[str, Any]:
    """
    Search for a paper by name using the Google Scholar API via SerpApi.
    
    Args:
    paper_name (str): The name of the paper to search for.
    api_key (str): Your SerpApi key.
    
    Returns:
    Dict[str, Any]: A dictionary containing the decoded information of the best matching paper.
    """
    base_url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_scholar",
        "q": f'"{paper_name}"',  # Use quotes for exact match
        "api_key": api_key,
        "num": 10  # Fetch top 10 results to find the best match
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        organic_results = data.get('organic_results', [])
        
        if not organic_results:
            return {"error": "No results found"}
        
        # Find the best matching paper
        best_match = max(organic_results, key=lambda x: SequenceMatcher(None, x.get('title', '').lower(), paper_name.lower()).ratio())
        
        return decode_google_scholar_response(best_match)
    
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {str(e)}"}


import ollama
import json
def extract_title(text):

    schema = """ {"title": ""}"""
    input_llm = f"""
    You extract the title from the first part of this chunk, ignoring the author names afterward### Template:
    {json.dumps(json.loads(schema), indent=4)}
    ### Example:
    {{"title": "Amazing new discovery"}}
    ### Text:
    {text}
"""

    response = ollama.chat(model='nuextract', messages=[ #llama3
    {
    'role': 'user',
    'content': input_llm}])#, options={"temperature":.5}

    output = response['message']['content']
    
    return output.replace("<|end-output|>","")#output[output.find("<|end-output|>"):]





import json
def extract_caption(text):

    

    schema = """ {"caption": ""}"""
    input_llm = f"""
    You extract the image caption from the following chunk of text### Template:
    {json.dumps(json.loads(schema), indent=4)}
    ### Example:
    {{"title": "Amazing new discovery"}}
    ### Text:
    {text}
"""

    response = ollama.chat(model='nuextract', messages=[ #llama3
    {
    'role': 'user',
    'content': input_llm}])#, options={"temperature":.5}

    output = response['message']['content']
    
    return output.replace("<|end-output|>","")#output[output.find("<|end-output|>"):]



def summarize(text, num_sentences=1):

    schema = """ {"title": ""}"""
    input_llm = f"""
    Only return your summary. Summarize the following text in {num_sentences} sentence(s).
    ### Text:
    {text}
"""

    response = ollama.chat(model='llama3.1', messages=[ #llama3
    {
    'role': 'user',
    'content': input_llm}])#, options={"temperature":.5}

    output = response['message']['content']
    while output.replace("<|end-output|>","").replace(" ", "") == "":
        response = ollama.chat(model='llama3.1', messages=[ #llama3
        {
        'role': 'user',
        'content': input_llm}])#, options={"temperature":.5}

        output = response['message']['content']
    
    return output


def extract_details(text, model='llama3.1'):


    input_llm  = '''
    Please extract important details from the given text and return them in a JSON object with a "details" key. Focus on key concepts, findings, and insights. 

    Guidelines:

    1. Identify crucial information that summarizes the main points. Authors are unimportant
    2. Exclude unnecessary details and examples.
    3. Use concise language and avoid lengthy descriptions.
    4. Prioritize accuracy and relevance.
    5. Ensure the detail forms a complete thought that is meaningful on it's own

    Return format:
    {
    "details": [
    "Important detail 1",
    "Important detail 2",
    "Important detail 3",
    ...
    ]
    }

    Input: 
    ''' +  text


    response = ollama.chat(model= model, messages=[ #llama3
    {
    'role': 'user',
    'content': input_llm}])#, options={"temperature":.5}

    output = response['message']['content']
    while output.replace("<|end-output|>","").replace(" ", "") == "":
        response = ollama.chat(model='llama3.1', messages=[ #llama3
        {
        'role': 'user',
        'content': input_llm}])#, options={"temperature":.5}

        output = response['message']['content']
    
    return output



def extract_attributes(text):

    input_llm = '''
    Please process the given text and extract useful attributes in the following structured JSON format:

    {
        "entities": [
            {
                "name": "Entity Name",
                "relations": [
                    {"relation": "is/has/are/was/etc.", "attribute": "informative and relevant associated attribute, action, or description"}
                ]
            }
        ]
    }

    Guidelines:

    1. Identify key concepts, terms, and phrases in the text, including but not limited to proper nouns.
    2. For each entity, list attributes, actions, or descriptions that provide meaningful context and insights.
    3. Ensure each entity-attribute pair forms a grammatically complete and informative sentence.
    4. Prioritize accuracy and relevance, focusing on essential information.
    5. Use lowercase for relation words and capitalize the first letter of entity names.
    6. Avoid redundancy, obvious information, and overly general statements.
    7. List multiple related attributes separately for each entity.
    8. Ensure the output is valid JSON.

    Input: 
    '''  + text


    response = ollama.chat(model='llama3.1', messages=[ #llama3
    {
    'role': 'user',
    'content': input_llm}])#, options={"temperature":.5}

    output = response['message']['content']
    while output.replace("<|end-output|>","").replace(" ", "") == "":
        response = ollama.chat(model='llama3.1', messages=[ #llama3
        {
        'role': 'user',
        'content': input_llm}])#, options={"temperature":.5}

        output = response['message']['content']
    
    return output



import ollama
import os
from tqdm import tqdm
from semantic_text_splitter import TextSplitter
from transformers import PreTrainedTokenizerFast
from tokenizers import Tokenizer
import PyPDF2
from langchain_text_splitters import RecursiveCharacterTextSplitter 
import ollama

def ingest_text(file_path, max_tokens=100, overlap_ratio=0.50):
    # Determine file extension
    _, file_extension = os.path.splitext(file_path)

    # Read the content based on file type
    if file_extension.lower() == '.pdf':
        content = read_pdf(file_path)
    else:  # Assume it's a text file for other extensions
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

    # Initialize tokenizer and splitter
    # tokenizer = Tokenizer.from_pretrained("bert-base-uncased")
    # text_splitter = TextSplitter.from_huggingface_tokenizer(tokenizer, max_tokens, overlap=int(max_tokens * overlap_ratio))

    splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=max_tokens,
        chunk_overlap=int(max_tokens * overlap_ratio),
        length_function=len,
        is_separator_regex=False,
    )
    # Split the content into chunks
    # chunks = splitter.chunks(content)

    chunks = splitter.split_text(content)

    return chunks

def read_pdf(file_path):
    content = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in tqdm(pdf_reader.pages):
            content += page.extract_text()
    return content




import os

def create_folder_if_not_exists(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        # If not, create the folder
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")
    else:
        print(f"Folder '{folder_path}' already exists.")


import io
import fitz  # PyMuPDF
from PIL import Image

def extract_images_with_captions(pdf_path):
    # Open the PDF file
    pdf_file = fitz.open(pdf_path)
    results = []

    # Iterate over all pages
    for page_index in range(len(pdf_file)):
        # Get the page
        page = pdf_file[page_index]
        image_list = page.get_images()

        # Printing number of images found in this page
        if image_list:
            print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
        else:
            print("[!] No images found on page", page_index)

        # Iterate over all images on the page
        for image_index, img in enumerate(image_list, start=1):
            # Get the XREF of the image
            xref = img[0]
            # Extract the image bytes
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]
            # Get the image extension
            image_ext = base_image["ext"]
            # Load it to PIL
            image = Image.open(io.BytesIO(image_bytes))
            # Save it to the local disk
            # image_filename = f"image{page_index+1}_{image_index}.{image_ext}"
            # image.save(open(image_filename, "wb"))

            # Extract text from the page to find captions
            text = page.get_text("text")
            # print(f"Text on page {page_index}: {text}")
            results.append([image, text])
            # Here you could implement logic to identify captions, e.g., based on proximity
            # to images or specific keywords, if the PDF structure allows it.



    images_with_captions = []

    for result in results:

        if "Figure" in result[1]:
            temp = result[1][result[1].find("Figure") + 6:][:result[1][result[1].find("Figure"):].find("Downloaded")]
            # temp = json.loads(extract_caption(result[1]))['caption']
            
        # else:
            # try:
            #     temp = json.loads(extract_caption(result[1]))['caption']
            # except json.JSONDecodeError:
            #     print("JSON decoding error when trying to generate caption, trying again...")
            #     temp = json.loads(extract_caption(result[1]))['caption']
            minicaption = summarize(temp)
            images_with_captions.append({"image":result[0], "caption":temp, "minicaption": minicaption})


    return images_with_captions

# get title
import json
def get_paper_info(file_name):
    chunks = ingest_text(file_name,max_tokens=700)
    title = json.loads(extract_title(chunks[0]))['title']
    paper_info = find_paper_by_name(title)
    return {"title":title, "paper_info":paper_info, "chunks":chunks}



import re

def wrap_text(text, width=20):
    pattern = r'(.{' + str(width) + r',}?)(\s+|$)'
    return re.sub(pattern, lambda m: m.group(1) + '\n', text)



def extract_info(text):
    

    schema = """ {
            "": ""
    }"""
    input_llm = f"""
    Given a full text of a research paper, return a dictionary of the section names and each of the sections of text. If no title is easily found, create a sensible one### Template:
    {json.dumps(json.loads(schema), indent=4)}
    ### Example:
 {{
            "Section Name": "Here is all the text in the section "Section Name." I think it will prove important"
    }}
    ### Text:
    {text}
"""

    response = ollama.chat(model='nuextract', messages=[ #llama3
    {
    'role': 'user',
    'content': input_llm}])#, options={"temperature":.5}

    output = response['message']['content']
    
    return output.replace("<|end-output|>","")#output[output.find("<|end-output|>"):]
