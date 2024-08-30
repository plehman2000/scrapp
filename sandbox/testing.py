import marimo

__generated_with = "0.6.25"
app = marimo.App(width="medium")


@app.cell
def __():
    import modules.scrapper as scrapper
    import uuid
    return scrapper, uuid


@app.cell
def __():
    import os
    import datetime

    def read_file_with_metadata(file_path):
        result = {}

        # Get file metadata
        file_stats = os.stat(file_path)
        result['metadata'] = {
            'file_name': os.path.basename(file_path),
            'file_size': file_stats.st_size,
            'creation_time': datetime.datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
            'modification_time': datetime.datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
            # 'access_time': datetime.datetime.fromtimestamp(file_stats.st_atime).isoformat(),
        }

        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                result['content'] = file.read()
        except UnicodeDecodeError:
            # If UTF-8 decoding fails, try reading as binary
                result['content'] = file.read().decode('utf-8', errors='replace')

        return result
    return datetime, os, read_file_with_metadata


@app.cell
def __():
    #:now to combine the relations based on the same subjects, thwen storee the docs and scrapps
    def db_ready_facts(relations, doc_id):
        temp_facts = relations['facts']
        filtered_facts = {}
        for x in temp_facts:
            if x['subject'] not in filtered_facts:
                filtered_facts[x['subject']] = [] 
            filtered_facts[x['subject']].append([ x['predicate'], doc_id]) 
        return filtered_facts
    return db_ready_facts,


@app.cell
def __():
    # def ingest_doc(file_path, scrapp_db, file_name_db):
    #     file_info = read_file_with_metadata(file_path)# Enter File name here
    #     doc_id = uuid.uuid4()
    #     relations = scrapper.text_to_relations(file_info['content'])
    #     filtered_facts = db_ready_facts(relations, doc_id)
    #     file_name_db[doc_id] = file_info
    #     return filtered_facts
    return


@app.cell
def __():
    # import dbm
    # import shelve
    # from modules.loader_anim import Loader

    # from tqdm import tqdm
    # from wonderwords import RandomWord
    # scrapp_db = shelve.open('.\\databases\\scrapps_db', 'c')
    # file_name_db = dbm.open('.\\databases\\files_db', 'c')
    # file_path = "./test_inputs/info.txt"
    # # filtered_facts = ingest_doc(file_path, scrapp_db, file_name_db)


    # file_info = read_file_with_metadata(file_path)# Enter File name here
    # doc_id = str(uuid.uuid4())
    # relations = scrapper.text_to_relations(file_info['content'])
    # filtered_facts = db_ready_facts(relations, doc_id)
    # loader = Loader("Adding to db...", "Done!").start()
    # file_name_db[doc_id] = file_info['metadata']['file_name']
    # for subject in filtered_facts:
    #     temp = []
    #     if subject  in scrapp_db.keys():
    #         temp = scrapp_db[subject]
    #     for entry in filtered_facts[subject]:
    #         temp.append(entry)
    #     scrapp_db[subject] = temp
    # loader.stop()
    return


@app.cell
def __():
    return


@app.cell
def __(db_ready_facts, read_file_with_metadata, scrapper, uuid):
    from tinydb import TinyDB, Query
    from modules.loader_anim import Loader
    from tqdm import tqdm

    # Initialize TinyDB databases
    scrapp_db = TinyDB('./databases/scrapps_db.json')
    file_name_db = TinyDB('./databases/files_db.json')



    def ingest_document_prototype(file_path):
        # Read file and process content
        file_info = read_file_with_metadata(file_path)
        doc_id = str(uuid.uuid4())
        relations = scrapper.text_to_relations(file_info['content'])
        filtered_facts = db_ready_facts(relations, doc_id)
        
        # Add file name to file_name_db
        file_name_db.insert({'doc_id': doc_id, 'file_name': file_info['metadata']['file_name']})
        
        # Add filtered facts to scrapp_db
        loader = Loader("Adding to DB...", "Done!").start()
        
        for subject in filtered_facts:
            existing_entry = scrapp_db.get(Query().subject == subject)
            if existing_entry:
                updated_facts = existing_entry['facts'] + filtered_facts[subject]
                scrapp_db.update({'facts': updated_facts}, Query().subject == subject)
            else:
                scrapp_db.insert({'subject': subject, 'facts': filtered_facts[subject]})
        
        loader.stop()


    file_path = "./test_inputs/info3.txt"
    # file_path = "./test_inputs/info2.txt"
        

    ingest_document_prototype(file_path)


    return (
        Loader,
        Query,
        TinyDB,
        file_name_db,
        file_path,
        ingest_document_prototype,
        scrapp_db,
        tqdm,
    )


@app.cell
def __():
    from rapidfuzz import fuzz

    return fuzz,


@app.cell
def __(Query, fuzz, scrapp_db):
    import json
    query = "Kamala"
    # Get all documents
    def search_db(query, n=1):
        all_docs = scrapp_db.all()
        all_subjects = [doc['subject'] for doc in all_docs]
        for s in all_subjects:
            print(s)
        all_subjects = sorted(all_subjects, key=lambda x: fuzz.partial_ratio(query,x), reverse=True)
        top_n = all_subjects[:n]
        return top_n


    results = search_db(query, n=1)
    q = Query()
    output = scrapp_db.search(q.subject == results[0])
    print(json.dumps(output[0], indent=4))
    # print(results)
    return json, output, q, query, results, search_db


app._unparsable_cell(
    r"""
    # Need to figure out how to fix the subjects not grouping together
    def condense_db(scrapp_db):
        
    """,
    name="__"
)


@app.cell
def __():
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
