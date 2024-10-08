import marimo

__generated_with = "0.6.25"
app = marimo.App(width="medium")


@app.cell
def __():
    from ingestion_utils import find_paper_by_name, extract_title, ingest_text, create_folder_if_not_exists,extract_images_with_captions,extract_caption, get_paper_info,wrap_text, extract_details
    import spacy
    import marimo as mo
    import matplotlib.pyplot as plt
    import json
    return (
        create_folder_if_not_exists,
        extract_caption,
        extract_details,
        extract_images_with_captions,
        extract_title,
        find_paper_by_name,
        get_paper_info,
        ingest_text,
        json,
        mo,
        plt,
        spacy,
        wrap_text,
    )


@app.cell
def __():
    file_name = "./papers/paper1.pdf"
    return file_name,


@app.cell
def __(extract_images_with_captions, file_name):
    images_with_captions = extract_images_with_captions(file_name)
    return images_with_captions,


@app.cell
def __(images_with_captions):
    images_with_captions
    return


@app.cell
def __():
    # imgshow = plt.imshow(images_with_captions[0]['image'])
    # plt.show()
    return


@app.cell
def __(file_name, get_paper_info):
    paper = get_paper_info(file_name)
    return paper,


@app.cell
def __(file_name):
    import fitz  # PyMuPDF

    def extract_text(pdf_path):
        doc = fitz.open(pdf_path)
        full_text = ""
        for page in doc:
            # Extract text from the page
            text = page.get_text()
            full_text += text
            
        doc.close()
        
        return full_text

    # Usage
    full_text = extract_text(file_name)
    return extract_text, fitz, full_text


@app.cell
def __(file_name):
    import pdfplumber
    import re

    def split_pdf_by_section(text):
        sections = {}
        current_section = "Default"
        lines = text.split('\n')
        
        for line in lines:
            if line.startswith("Section: "):
                current_section = line.replace("Section: ", "").strip()
                sections[current_section] = []
            else:
                if current_section not in sections:
                    sections[current_section] = []
                sections[current_section].append(line)
        
        return sections
    sections = split_pdf_by_section(file_name)

    for section, content in sections.items():
        print(f"Section: {section}")
        print("-" * 50)
        print("\n".join(content[:5]))  # Print first 5 lines of each section
        print("...\n")


    return content, pdfplumber, re, section, sections, split_pdf_by_section


@app.cell
def __(extract_info, full_text):
    info = extract_info(full_text)
    print(info)
    return info,


@app.cell
def __(info):
    type(info)
    return


@app.cell
def __(paper):
    chunks = paper['chunks']
    return chunks,


@app.cell
def __(chunks, extract_details, json):
    from tqdm import tqdm
    details = []
    for chunk in tqdm(chunks):
        temp_str = extract_details(chunk, model='llama3.1')
        interm = temp_str[temp_str.find("{"):][:temp_str.find("}") + 1]
        print(interm)
        if interm:  # Check if interm is not empty
            print("|" + interm + "|")
            detail = json.loads(interm)
            details.extend(detail['details'])
        else:
            print("No details found in this chunk.")
    return chunk, detail, details, interm, temp_str, tqdm


@app.cell
def __():
    import pickle
    # pickle.dump(details, open("paper_deets.pkl", 'wb'))
    return pickle,


@app.cell
def __(pickle):
    deets = pickle.load(open("paper_deets.pkl", 'rb'))
    return deets,


@app.cell
def __(deets):
    deets
    return


@app.cell
def __(paper):
    title = paper['title']
    return title,


@app.cell
def __():
    # Visualizing
    return


@app.cell
def __(wrap_text):
    import os
    from PIL import Image
    from pyvis.network import Network

    def create_network(title, image_caption_pairs):
        # Create the directory to save images if it doesn't exist
        os.makedirs("./temp", exist_ok=True)

        # Create a Pyvis network
        net = Network(notebook=True, width="100%", height="1000px", bgcolor="#222222", font_color="white", select_menu=True)

        # Add central node with title
        net.add_node(wrap_text(title), title=wrap_text(title), color='#4287f5', size=30, shape='dot')

        # Add nodes and edges for each image-caption pair
        for i, pair in enumerate(image_caption_pairs):
            image = pair['image']
            caption = pair['caption']
            image_path = f"./temp/{i}.png"
            image.save(image_path)
            print(wrap_text(pair['minicaption']))
            node_name = f"Node {i+1}"
            net.add_node(wrap_text(pair['minicaption']), title=wrap_text(pair['minicaption']), shape='image', image=image_path, color='#FFA500', size=50, mass=1.5  * len(image_caption_pairs))

            # Add an edge between the central node and the image node
            net.add_edge(wrap_text(title), wrap_text(pair['minicaption']), font={'color': 'black', 'size': 9})
        net.toggle_physics(False)

        # Generate and save the interactive HTML file
        html_filename = f"{title.lower().replace(' ', '_')}_network.html"
        net.save_graph(html_filename)

        return net, html_filename

    # Example usage
    # images_with_captions = [
    #     {"image": Image.open("path/to/image1.jpg"), "caption": "Caption 1"},
    #     {"image": Image.open("path/to/image2.jpg"), "caption": "Caption 2"}
    # ]
    # create_network("My Network", images_with_captions)
    return Image, Network, create_network, os


@app.cell
def __(images_with_captions):
    images_with_captions
    return


@app.cell
def __(create_network, images_with_captions, title):
    net, name = create_network(title.title(), images_with_captions)
    return name, net


if __name__ == "__main__":
    app.run()
