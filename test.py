import marimo

__generated_with = "0.6.25"
app = marimo.App(width="medium")


@app.cell
def __():
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

    return (
        BeautifulSoup,
        RecursiveCharacterTextSplitter,
        fuzz,
        get_embeddings,
        get_similarity,
        get_urls,
        get_webpage_info,
        html_text,
        max_tokens,
        nlp,
        np,
        ollama,
        os,
        overlap_ratio,
        requests,
        search,
        spacy,
        splitter,
        summarize,
        time,
        tqdm,
        url_has_file_extension,
    )


@app.cell
def __(get_webpage_info):
    get_webpage_info("https://apnews.com/article/israel-palestinians-hamas-war-news-08-27-2024-696f8ee830207815efd31320976ef118")
    return


if __name__ == "__main__":
    app.run()
