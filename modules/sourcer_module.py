import numpy as np
from tqdm import tqdm 
import html_text   
import requests
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
import ollama

from googlesearch import search
import os
import time
def url_has_file_extension(url):
    _, ext = os.path.splitext(url)
    return ext != ""
        
def get_urls(query, k=5):
    # Perform a Google search and get the top 5 URLs
    urls = search(query, num_results=k*5, safe=None)
    processed = []
    for url in urls:
        if not url_has_file_extension(url):
            processed.append(url)
        if len(processed) > k+1:
            return processed[:k]
    return processed[:k]



import spacy

# Load the SpaCy model with word vectors

def get_embeddings(text):
    # Process the text with SpaCy
    doc = nlp(text)
    # Return the vector representation of the text
    return doc.vector



def get_similarity(a,b):
    return np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
from thefuzz import fuzz



def summarize(text):
    response = ollama.chat(model='ALIENTELLIGENCE/contentsummarizer', messages=[ #llama3
    {
    'role': 'user',
    'content': text}])
    output = response['message']['content']
    return output
# out = extract_info(input_sentence)
# print(out)



overlap_ratio = 0.25
max_tokens = 150
splitter = RecursiveCharacterTextSplitter(
chunk_size=max_tokens,
chunk_overlap=int(max_tokens * overlap_ratio),
length_function=len,
is_separator_regex=False,
)

nlp = spacy.load("en_core_web_lg")  # or "en_core_web_lg" for larger vectors


quote_to_find = "the goddamn faggiest thing you've ever seen"


def get_webpage_info(urls):
    print(f"{len(urls)} site(s) found")
    url_to_text_hsh = {}
    web_chunks =  []
    for a in urls:
        html = requests.get(a).text
        txt = html_text.extract_text(html, guess_layout=True)
        url_to_text_hsh[a] = txt
        web_chunks.append([a,splitter.split_text(txt), a]) 
    return url_to_text_hsh, web_chunks

def get_sources(quote_to_find, k = 2, best_source = True, print_nice=True):

    if best_source:
        k = 1


    urls = get_urls(quote_to_find, k=5)

    url_to_text_hsh, web_chunks = get_webpage_info(urls)
    query_embedding = get_embeddings(quote_to_find)
    top_k = []
    k=5
    for chunk_pack in tqdm(web_chunks):
        ch = chunk_pack[1]
        for c in ch:
            similarity_results = get_similarity(query_embedding, get_embeddings(c))
            fuzz_rat = fuzz.partial_ratio(quote_to_find, c)
            similarity_results = (similarity_results*100 + fuzz_rat) /2

            full_text = chunk_pack[0]
            ind = full_text.find(c[1])

            best_quote_sentence = full_text[ind-100:ind+len(c[1]) + 100]

            if len(top_k) < k:
                top_k.append((similarity_results, c, chunk_pack[0], "..." + best_quote_sentence[:150]+ best_quote_sentence[150:-150]+ best_quote_sentence[-150:] + "..."))
                top_k.sort(reverse=True, key=lambda x: x[0])
            elif similarity_results > top_k[-1][0]:
                top_k[-1] = (similarity_results, c, chunk_pack[0], "..." + best_quote_sentence[:150]+ best_quote_sentence[150:-150]+ best_quote_sentence[-150:] + "...")
                top_k.sort(reverse=True, key=lambda x: x[0])

    #     temp = top_k[0]
    #     full_text = url_to_text_hsh[temp[2]]
    #     if print_nice:
    #         from colorama import Fore, Back, Style, init

    #         # Initialize colorama
    #         init(autoreset=True)

    #         # Print normal text
    #         print( "\n..." + best_quote_sentence[:150])

    #         # Print text with a blue background
    #         print(Back.BLUE + best_quote_sentence[150:-150])
    #         print( "\r"+ best_quote_sentence[-150:] + "...")
    #         print("\n")
    #         return
        
    if best_source:
        return top_k[0]
    else:
        return top_k


# top_k = get_sources(quote_to_find)

# for score, chunk, url in top_k:
#     print(f"Similarity: {score}, Chunk: {chunk}, Source: {url}")