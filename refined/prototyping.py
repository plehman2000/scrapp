import marimo

__generated_with = "0.9.9"
app = marimo.App(width="medium")


@app.cell
def __():
    from premiser import get_conclusion_premise, get_inversion
    from llm_funcs import reword_query
    from text_utils import chunk_text, is_non_informative
    from web_funcs import download_webpage_html
    return (
        chunk_text,
        download_webpage_html,
        get_conclusion_premise,
        get_inversion,
        is_non_informative,
        reword_query,
    )


@app.cell
def __():
    claim = "Donald Trump a bad candidate for president"
    return (claim,)


@app.cell
def __(claim, reword_query):
    from pymojeek import Search

    query = reword_query(claim)
    client = Search(api_key="HNJaxYzYNVImfHCaLJzohRSJnoKofi")
    results = client.search(query)

    print(f"Found {len(results)} for query '{results.query}'")
    return Search, client, query, results


@app.cell
def __():
    from tqdm import tqdm
    # for x in tqdm(results):
        # print(download_webpage_html(x.url, title=x.title.replace(" ", "").replace("\\", "").replace("/", "")))
    return (tqdm,)


@app.cell
def __():
    return


@app.cell
def __(chunk_text, is_non_informative, tqdm):
    import os
    from web_funcs import extract_text_from_html_file
    filedir = "./documents/"
    all_chunks = []

    num_files = 0
    for file in tqdm(os.listdir(filedir)):
        text = extract_text_from_html_file(filedir + file)
        num_files = num_files +1
        chunks = chunk_text(text)
        for c in chunks:
            if not is_non_informative(c):
                all_chunks.append(c)
    return (
        all_chunks,
        c,
        chunks,
        extract_text_from_html_file,
        file,
        filedir,
        num_files,
        os,
        text,
    )


@app.cell(hide_code=True)
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
    import numpy as np
    import pandas as pd
    from sklearn.manifold import TSNE
    from sklearn.decomposition import PCA

    vectors_embedded = PCA(n_components=2).fit_transform(np.array([x[1] for x in all_chunk_vector_pairs]))

    return PCA, TSNE, np, pd, vectors_embedded


@app.cell(hide_code=True)
def __(all_chunk_vector_pairs, np):
    from sklearn.cluster import HDBSCAN, AffinityPropagation, k_means, dbscan

    N = 5

    a_clustered = k_means(np.array([x[1] for x in all_chunk_vector_pairs]), N)
    vectors_embedded_clustered = a_clustered[1]

    #VISUALIZATION CODE
    ####################################################
    # df = pd.DataFrame({"v1":vectors_embedded[:, 0], "v2":vectors_embedded[:, 1], 'text': [x[0] for x in all_chunk_vector_pairs], "cluster":vectors_embedded_clustered})
    # import plotly.express as px
    # fig = px.scatter(df, x='v1', y='v2', color='cluster')
    # fig.show()
    # print(f"{len(set(vectors_embedded_clustered))} Clusters")
    ####################################################

    return (
        AffinityPropagation,
        HDBSCAN,
        N,
        a_clustered,
        dbscan,
        k_means,
        vectors_embedded_clustered,
    )


@app.cell
def __(N, a_clustered):
    from collections import Counter
    # print(Counter(a_clustered[1]))
    # Take N biggest clusters
    sampled_clusters = [x[0] for x in sorted(Counter(a_clustered[1]).items(), key = lambda x : x[1], reverse=True)][:N]

    return Counter, sampled_clusters


@app.cell
def __(
    all_chunk_vector_pairs,
    sampled_clusters,
    vectors_embedded_clustered,
):
    cluster_to_chunk = {}
    i = 0
    for clu in sampled_clusters:
        chunks_of_cluster_n = []
        for z,a in zip(all_chunk_vector_pairs, vectors_embedded_clustered):
            if a == clu:
                chunks_of_cluster_n.append(z[0])
        cluster_to_chunk[i] = chunks_of_cluster_n
        i = i +1
    return a, chunks_of_cluster_n, clu, cluster_to_chunk, i, z


@app.cell
def __(N, claim, cluster_to_chunk, tqdm):
    # for each set of chunks, random sample
    from random import sample
    from llm_funcs import determine_informative, combine_claims, restate_claim
    max_sample_count_per_cluster = 100
    n_chunks_needed_per_cluster = 6

    informative_chunks = {}
    for clust_i in tqdm(range(N)):
        sampled_chunks = sample(cluster_to_chunk[clust_i], max_sample_count_per_cluster)
        # print(sampled_chunks)
        n_informatives_found = 0
        informative_chunks[clust_i] = []
        
        for chu in sampled_chunks:
            informative = determine_informative(chu, claim)
            if 'response' in informative:
                if informative['response'].lower() == 'true':
                    n_informatives_found +=1
                    # print(f"{n_informatives_found} Info Chunk(s) Found!")
                    informative_chunks[clust_i].append(chu)
            if n_informatives_found >=n_chunks_needed_per_cluster:
                print(f"Enough Info Chunk(s) Found!")
                
                break

    return (
        chu,
        clust_i,
        combine_claims,
        determine_informative,
        informative,
        informative_chunks,
        max_sample_count_per_cluster,
        n_chunks_needed_per_cluster,
        n_informatives_found,
        restate_claim,
        sample,
        sampled_chunks,
    )


@app.cell
def __(claim, combine_claims, restate_claim):

    def reduce_chunks(chunks):
        print(f"Reducing {len(chunks)} chunks...")
        intermediate_summaries = chunks
        while len(intermediate_summaries) != 1:
            temp = []
            for zx in range(0,len(intermediate_summaries), 2):
                if zx+1 < len(intermediate_summaries):
                    combined_claim = combine_claims(claim, intermediate_summaries[zx], intermediate_summaries[zx+1])
                    temp.append(combined_claim)
                else:
                    temp.append(restate_claim(claim,intermediate_summaries[zx]))
            intermediate_summaries = temp
            # print(intermediate_summaries)
            # print(len(intermediate_summaries))
        
        final_argument = intermediate_summaries[0]
        return final_argument

    # final_arg = reduce_chunks(informative_chunks[0])
    return (reduce_chunks,)


@app.cell
def __(informative_chunks, reduce_chunks):
    final_args = []
    for cl in informative_chunks:
        final_arg = reduce_chunks(informative_chunks[cl])
        final_args.append(final_arg)
        print(final_arg)
    return cl, final_arg, final_args


@app.cell
def __(final_args):
    final_args
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
