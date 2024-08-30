import marimo

__generated_with = "0.6.25"
app = marimo.App(width="medium")


@app.cell
def __():
    return


@app.cell
def __():
    import dbm
    import shelve
    import uuid
    from tqdm import tqdm
    from wonderwords import RandomWord



    db = shelve.open('scrapps', 'c')
    r = RandomWord()



    # Add scrapps to databases
    for i in tqdm(range(100)):
        db[r.word()] = {"scrapps": [{"subject": "this"}]}



    from rapidfuzz import fuzz


    query = "apple"

    keys = db.keys()
    keys = sorted(keys, key=lambda x: fuzz.partial_ratio(query,x), reverse=True)
    print(keys[:5])
    print(db[keys[0]])
    return RandomWord, db, dbm, fuzz, i, keys, query, r, shelve, tqdm, uuid


if __name__ == "__main__":
    app.run()
