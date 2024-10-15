import requests
from urllib.parse import urlparse
import uuid
import os
def download_webpage_html(url,title, save_folder="./documents/"):
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Raise an exception for bad status codes
        response.raise_for_status()

        # Get the HTML content
        html_content = response.text

        # If save_path is not provided, create a filename based on the URL
        filename = title+ "__" + str(uuid.uuid4())[:8] + ".html"
        save_path = os.path.join(save_folder, filename)

        # Save the HTML content to a file
        with open(save_path, "w", encoding="utf-8") as file:
            file.write(html_content)

        print(f"HTML content saved successfully to: {save_path}")
        return save_path

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading the webpage: {e}")
        return None
    except IOError as e:
        print(f"An error occurred while saving the file: {e}")
        return None



import html_text


def extract_text_from_html_file(file_path, guess_layout=True):
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        # Open and read the HTML file
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        # Extract text from the HTML content
        extracted_text = html_text.extract_text(html_content, guess_layout=guess_layout)

        return extracted_text

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")
        return None
