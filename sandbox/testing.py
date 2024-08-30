import marimo

__generated_with = "0.6.25"
app = marimo.App(width="medium")


@app.cell
def __():
    from modules.ingest_docs import search_db, ingest_document_prototype
    return ingest_document_prototype, search_db


@app.cell
def __(search_db):
    search_db("Kamala D. Harris")
    return


@app.cell
def __(ingest_document_prototype):
    # file_path = "./test_inputs/info3.txt"
    file_path = "./test_inputs/info2.txt"
    ingest_document_prototype(file_path)
    ingest_document_prototype("./test_inputs/info3.txt")
    ingest_document_prototype("./test_inputs/info1.txt")

    return file_path,


@app.cell
def __(ingest_document_prototype):

    ingest_document_prototype("./test_inputs/info3.txt")
    ingest_document_prototype("./test_inputs/info1.txt")
    return


if __name__ == "__main__":
    app.run()
