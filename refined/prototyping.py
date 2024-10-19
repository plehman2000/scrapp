import marimo

__generated_with = "0.9.9"
app = marimo.App(width="medium")


@app.cell
def __():
    from premiser import get_conclusion_premise, get_inversion
    from llm_funcs import reword_query
    from text_utils import chunk_text
    return chunk_text, get_conclusion_premise, get_inversion, reword_query


@app.cell
def __():
    from web_funcs import download_webpage_html
    return (download_webpage_html,)


@app.cell
def __():
    claim = "Donald Trump a bad candidate for president"
    return (claim,)


@app.cell
def __(claim, reword_query):
    from pymojeek import Search





    query = reword_query(claim)
    client = Search(api_key="")
    results = client.search(query)

    print(f"Found {len(results)} for query '{results.query}'")
    return Search, client, query, results


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
    return extract_text_from_html_file, filedir, os


@app.cell
def __(chunk_text, extract_text_from_html_file, filedir, os):
    from tqdm import tqdm
    all_chunks = []

    num_files = 0
    for file in tqdm(os.listdir(filedir)):
        text = extract_text_from_html_file(filedir + file)
        num_files = num_files +1
        chunks = chunk_text(text)
        for c in chunks:
            all_chunks.append(c)
    return all_chunks, c, chunks, file, num_files, text, tqdm


@app.cell
def __():
    # import spacy
    # from maverick import Maverick
    # from detokenize.detokenizer import detokenize

    # model = Maverick(device="cuda")
    # nlp_lg = spacy.load("en_core_web_lg")

    # def get_best_noun(
    #     cluster, offsets
    # ):  # gets best Noune from a cluster, if all pronoiuns return none
    #     ls = []
    #     for noun, offset in zip(cluster, offsets):
    #         pos = nlp_lg(noun)[0].pos_
    #         # print(f"POS: {noun} {pos}")
    #         if pos in ["DET", "PROPN", "VERB"]:
    #             # print(noun, pos)
    #             ls.append([noun, offset])

    #     if len(ls) == 0:
    #         return None, None
    #     ls = sorted(ls, key=lambda x: len(x[0]), reverse=False)
    #     # TODO need better heuristic here, just picks first, should be informed by prior selections (search db for terms, select ones that are the same?)
    #     # print(f"Picked {ls[0][0]}!")
    #     return ls[0][0], ls[0][1]
    return


@app.cell
def __():
    #DEPROUNOUNINg TOO SLOW - need vllm or ollama optimization - takes 2s per chunk

    # final_chunks = []
    # print("Loading")

    # prev_chunk = claim
    # zix = 0
    # for chunk in tqdm(
    #     all_chunks, desc="Ess"
    # ):
    #     pronoun_results = model.predict(prev_chunk + "||-||" +chunk)
    #     pron_tokenized = pronoun_results["tokens"]
    #     main_subjects = []
    #     relations_list = []
    #     for i, (clusters, offsets) in enumerate(
    #         zip(
    #             pronoun_results["clusters_token_text"],
    #             pronoun_results["clusters_token_offsets"],
    #         )
    #     ):
    #         best_noun, _ = get_best_noun(clusters, offsets)
    #         if best_noun != None:
    #             for cl, off in zip(clusters, offsets):
    #                 for i in range(off[0], off[1] + 1):
    #                     if i == off[0]:
    #                         pron_tokenized[i] = best_noun
    #                     else:
    #                         pron_tokenized[i] = ""
    #             main_subjects.append(best_noun)

    #         # print(temp_cl)
    #     # print(pron_tokenized)
    #     detokenized_chunk = detokenize(pron_tokenized)
    #     final_chunks.append(detokenized_chunk)
    #     prev_chunk = detokenized_chunk[detokenized_chunk.find("||-||")+5:]
    return


@app.cell
def __(all_chunks, tqdm):
    import ollama
    all_chunk_vector_pairs = []
    for chunk in tqdm(all_chunks):
        if len(chunk) > 15:
            embedding = ollama.embeddings(model="nomic-embed-text", prompt=chunk)["embedding"]
            all_chunk_vector_pairs.append([chunk, embedding])
    return all_chunk_vector_pairs, chunk, embedding, ollama


@app.cell
def __(all_chunk_vector_pairs):
    len(all_chunk_vector_pairs)
    return


@app.cell
def __(all_chunk_vector_pairs):
    import numpy as np

    from sklearn.manifold import TSNE
    from sklearn.decomposition import PCA

    # vectors_embedded = TSNE(n_components=2, learning_rate='auto',init='random', perplexity=3).fit_transform(np.array([x[1] for x in all_chunk_vector_pairs]))
    vectors_embedded = PCA(n_components=2).fit_transform(np.array([x[1] for x in all_chunk_vector_pairs]))
    import pandas as pd
    return PCA, TSNE, np, pd, vectors_embedded


@app.cell
def __():
    return


@app.cell
def __():
    return


@app.cell
def __():
    return


@app.cell
def __():
    return


@app.cell
def __(vectors_embedded_clustered):
    vectors_embedded_clustered
    return


@app.cell
def __(all_chunk_vector_pairs, np, pd, vectors_embedded):
    from sklearn.cluster import HDBSCAN, AffinityPropagation, k_means


    vectors_embedded_clustered = HDBSCAN( min_cluster_size=3).fit_predict(np.array([x[1] for x in all_chunk_vector_pairs]))
    # vectors_embedded_clustered = AffinityPropagation().fit_predict(np.array([x[1] for x in all_chunk_vector_pairs]))
    # vectors_embedded_clustered = k_means(np.array([x[1] for x in all_chunk_vector_pairs]), num_files)[1]

    df = pd.DataFrame({"v1":vectors_embedded[:, 0], "v2":vectors_embedded[:, 1], 'text': [x[0] for x in all_chunk_vector_pairs], "cluster":vectors_embedded_clustered})
    import plotly.express as px
    fig = px.scatter(df, x='v1', y='v2', color='cluster')
    fig.show()
    print(f"{len(set(vectors_embedded_clustered))} Clusters")
    return (
        AffinityPropagation,
        HDBSCAN,
        df,
        fig,
        k_means,
        px,
        vectors_embedded_clustered,
    )


@app.cell
def __():
    return


@app.cell
def __(
    all_chunk_vector_pairs,
    claim,
    np,
    ollama,
    vectors_embedded_clustered,
):
    from sklearn.metrics.pairwise import cosine_similarity

    clustered_chunks = {}

    for ch, clust in zip(all_chunk_vector_pairs, vectors_embedded_clustered):
        if clust not in clustered_chunks:
            clustered_chunks[clust] = []
        clustered_chunks[clust].append(ch)



    claim_embedding = ollama.embeddings(model="nomic-embed-text", prompt=claim)["embedding"]
    claim_embedding = np.array(claim_embedding)
    # print(claim_embedding)
    clustered_sims =  {}
    for chunk_group in clustered_chunks:
        vec_sim = 0
        for chv in clustered_chunks[chunk_group]:
            vec_sim +=cosine_similarity(np.array(chv[1]).reshape(1,-1), claim_embedding.reshape(1,-1))
        vec_sim /= len(clustered_chunks[chunk_group])
        clustered_sims[chunk_group] = vec_sim
        clustered_chunks[chunk_group] = [x[0] for x in clustered_chunks[chunk_group]]
        #calculate cosine similarity to original claim
    return (
        ch,
        chunk_group,
        chv,
        claim_embedding,
        clust,
        clustered_chunks,
        clustered_sims,
        cosine_similarity,
        vec_sim,
    )


@app.cell
def __(clustered_chunks, clustered_sims):
    sims_sorted = [x[0] for x in sorted(list(clustered_sims.items()), key = lambda x : x[1], reverse=True)]

    for clusterid in sims_sorted:
        #this order may help with generating the strongest reasons
        chungs = clustered_chunks[clusterid]
        print(len(chungs))
    return chungs, clusterid, sims_sorted


@app.cell
def __():
    # How to filter for useful chunks?
    # , average of vector similarity to ai generated premises?
    return


if __name__ == "__main__":
    app.run()
