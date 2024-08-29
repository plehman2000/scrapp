import marimo

__generated_with = "0.7.1"
app = marimo.App(width="medium")


@app.cell
def __():
    import dbm
    import uuid
    from tqdm import tqdm
    from wonderwords import RandomWord



    db = dbm.open('scrapps', 'c')
    r = RandomWord()




    # Add scrapps to databases
    for i in tqdm(range(100000)):
        db[r.word()] = {"scrapps": [{"subject": "this"}]}

    return RandomWord, db, dbm, i, r, tqdm, uuid


@app.cell
def __(db):
    from rapidfuzz import fuzz


    query = "apple"

    keys = db.keys()
    keys = sorted(keys, key=lambda x: fuzz.partial_ratio(query,x), reverse=True)
    print(keys[:5])
    return fuzz, keys, query


if __name__ == "__main__":
    app.run()
