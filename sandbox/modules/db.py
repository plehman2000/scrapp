import chromadb
import ollama
import os


client = chromadb.PersistentClient(path=os.getcwd() + "\\databases\\scrapp_chroma")
import uuid


# Define the EmbeddingFunction class
class OllamaEmbeddingFunction:
    def __call__(self, input):
        if isinstance(input, list):
            return [
                ollama.embeddings(model="nomic-embed-text", prompt=text)["embedding"]
                for text in input
            ]
        else:
            return ollama.embeddings(model="nomic-embed-text", prompt=input)[
                "embedding"
            ]


# Create an instance of the embedding function
embedding_function = OllamaEmbeddingFunction()

# Create or get an existing collection
global scrapp_db
scrapp_db = client.get_or_create_collection(
    name="my_collection", embedding_function=embedding_function
)

# def add_docs(subject, chunks, metadata):
#     documents = []
#     ids = []
#     metadatas = []

#     for i, chunk in enumerate(chunks):
#         documents.append(f"{subject}: {chunk[0]}")
#         ids.append(f"{subject}-{metadata['lookup_id']}-{i}")
#         chunk_metadata = metadata.copy()
#         chunk_metadata['subject'] = subject
#         metadatas.append(chunk_metadata)

#     scrapp_db.add(
#         documents=documents,
#         metadatas=metadatas,
#         ids=ids
#     )

# update entitys TODO


def add_docs(
    subject, chunks, metadata
):  # Add some documents to the collection (if not already added)
    # list of [x["predicate"], doc_id]

    scrapp_db.add(
        documents=[x[0] for x in chunks],
        metadatas=metadata,
        ids=[str(uuid.uuid4() for _ in range(len(chunks)))],  # doc_ids
    )
    # update entitys TODO


import json


def rewrite_json(input_json):
    if input_json == "":
        return ""
    # Parse the input JSON if it's a string
    if isinstance(input_json, str):
        data = json.loads(input_json)
    else:
        data = input_json

    results = []

    # Assuming all lists have the same length and structure
    num_results = len(data["ids"][0])
    # print(f"NUM REUSLTS: {data}")
    if num_results == 0:
        return None
    for i in range(num_results):
        result = {
            "id": data["ids"][0][i],
            "distance": data["distances"][0][i],
            "metadata": data["metadatas"][0][i],
            "subject": data["metadatas"][0][i],
            "fact": data["documents"][0][i],
        }
        results.append(result)
    return {"results": results}


def search_db(query, n_results=10):
    res = scrapp_db.query(query_texts=[query], n_results=n_results)
    return rewrite_json(res)["results"]
    # return rewrite_json(res)['results']


def search_db_id(query, n_results=10):
    query = {"metadata": {"subject": query}}
    res = scrapp_db.query(query, n_results=n_results)
    return rewrite_json(res)["results"]
    # return rewrite_json(res)['results']
