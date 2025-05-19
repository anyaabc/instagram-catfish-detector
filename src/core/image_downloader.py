import requests
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
import json

def fetch_and_display_images_from_json(json_file):
    # Load JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Initialize a list to store images
    images = []

    # Iterate through each entry
    for entry in data:
        photo_urls = entry.get('photos', [])
        
        for url in photo_urls:
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                    "Referer": "https://www.instagram.com/"
                }
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                image_bytes = BytesIO(response.content)
                images.append(Image.open(image_bytes))
            except requests.exceptions.RequestException as e:
                print(f"Error fetching {url}: {e}")

    # Display images
    if images:
        fig, axes = plt.subplots(1, len(images), figsize=(5 * len(images), 5))
        if len(images) == 1:
            axes = [axes]  # Make it iterable
        for ax, img in zip(axes, images):
            ax.imshow(img)
            ax.axis("off")
        plt.show()
    else:
        print("No images to display.")

# Example usage
if __name__ == "__main__":
    json_file_path = r"C:\Users\karin\OneDrive - Bina Nusantara\Documents\skripsi\instagram-catfish-detector\data\cleaned_dataset.json"
    fetch_and_display_images_from_json(json_file_path)
