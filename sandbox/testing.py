import marimo

__generated_with = "0.6.25"
app = marimo.App(width="medium")


@app.cell
def __():
    import modules.scrapper as scrapper
    return scrapper,


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
def __(read_file_with_metadata, scrapper):
    file_info = read_file_with_metadata("./test_inputs/info.txt")# Enter File name here
    relations = scrapper.text_to_relations(file_info['content'])
    return file_info, relations


@app.cell
def __():
    # relations
    # some of these facts are completely irrelevant... to me i guess. 
    #But also we shouldn't give a fuck if shes the first black VP
    return


@app.cell
def __(relations):
    relations
    return


@app.cell
def __():
    #:now to combine the relations based on the same subjects, thwen storee the docs and scrapps
    return


@app.cell
def __():
    # class ScrappSource():
    #     def __init__(filepath)


    # class Scrapp():
    #     def __init__()
    return


if __name__ == "__main__":
    app.run()
