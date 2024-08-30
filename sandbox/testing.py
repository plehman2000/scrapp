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
    return


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

        response = ollama.chat(model='dolphin-llama3',
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


if __name__ == "__main__":
    app.run()
