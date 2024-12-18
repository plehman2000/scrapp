import marimo

__generated_with = "0.9.9"
app = marimo.App(width="medium")


@app.cell
def __():
    from marker.converters.pdf import PdfConverter
    from marker.models import create_model_dict
    from marker.output import text_from_rendered

    converter = PdfConverter(
        artifact_dict=create_model_dict(device='cuda'),
    )
    return PdfConverter, converter, create_model_dict, text_from_rendered


@app.cell
def __(converter, text_from_rendered):
    rendered = converter(r"C:\GH\scrapp\src\docs\long.pdf")
    ocr_text, _, images = text_from_rendered(rendered)
    return images, ocr_text, rendered


@app.cell
def __(ocr_text):
    ocr_text
    return


@app.cell
def __(images):
    images #TODO gonna need to add code to translate images into useful text and reinsert them where the text goes
    # e.g. in text:![](_page_27_Figure_7.jpeg)


    return


@app.cell
def __(ocr_text):
    from textsplitter import TextSplitter

    text_splitter = TextSplitter(
            max_token_size=300,
            end_sentence=True,
            preserve_formatting=False, #opposite is true?
            remove_urls=False,
            replace_entities=True,
            remove_stopwords=False,
            language="english",
        )

    text_chunks = text_splitter.split_text(ocr_text)
    print(text_chunks)

    for zx in text_chunks:
        print(zx)
        print("=" * 300)
        print("=" * 300)
    return TextSplitter, text_chunks, text_splitter, zx


@app.cell
def __():
    # IDEA
     # always running twitter bot that constantly pulls new research, process it and determiones promising research and promising directions of research
    return


if __name__ == "__main__":
    app.run()
