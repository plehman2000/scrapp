import marimo

__generated_with = "0.9.9"
app = marimo.App(width="medium")


@app.cell
def __():
    from premiser import get_conclusion_premise, get_inversion
    return get_conclusion_premise, get_inversion


@app.cell
def __():
    from web_funcs import download_webpage_html
    return (download_webpage_html,)


@app.cell
def __():
    def trim_leading_whitespace(s):
        lines = s.splitlines()
        if lines and lines[0].strip() == '':
            return '\n'.join(lines[1:])
        return s.lstrip()
    return (trim_leading_whitespace,)


@app.cell
def __(get_conclusion_premise, get_inversion, trim_leading_whitespace):
    import json
    def get_premises(conclusion):
        premises = get_conclusion_premise(conclusion)
        inverted_premises = get_inversion(conclusion, premises)
        premises_list = [trim_leading_whitespace(x) for x in list(json.loads(premises).values())]
        inverted_premises_list = [trim_leading_whitespace(x) for x in list(json.loads(inverted_premises).values())]
        return premises_list, inverted_premises_list
    return get_premises, json


@app.cell
def __():
    from pymojeek import Search

    def reword_query(naive_claim):
        #reword logic
        query = naive_claim
        return query

    claim = "Why is Donald Trump a bad candidate for president?"


    query = reword_query(claim)
    client = Search(api_key="HNJaxYzYNVImfHCaLJzohRSJnoKofi")
    results = client.search(query)

    print(f"Found {len(results)} for query '{results.query}'")
    return Search, claim, client, query, results, reword_query


@app.cell
def __(download_webpage_html, results):
    from tqdm import tqdm
    for x in tqdm(results):
        print(download_webpage_html(x.url, title=x.title.replace(" ", "").replace("\\", "").replace("/", "")))

    return tqdm, x


@app.cell
def __():
    import os
    from web_funcs import extract_text_from_html_file
    filedir = "./documents/"
    for file in os.listdir(filedir):
        text = extract_text_from_html_file(filedir + file)
        print(text)
        break
    return extract_text_from_html_file, file, filedir, os, text


if __name__ == "__main__":
    app.run()
