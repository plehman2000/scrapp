import marimo

__generated_with = "0.6.25"
app = marimo.App(width="medium")


@app.cell
def __():
    from ingestion_utils import find_paper_by_name, extract_title, ingest_text, create_folder_if_not_exists,extract_images_with_captions,extract_caption, get_paper_info,wrap_text
    import spacy
    import marimo as mo
    import matplotlib.pyplot as plt
    import json
    return (
        create_folder_if_not_exists,
        extract_caption,
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
