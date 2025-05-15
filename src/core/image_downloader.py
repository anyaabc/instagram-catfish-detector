import requests
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import ast  # To safely evaluate the string representation of lists

def fetch_and_display_images_from_csv(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Initialize a list to store images
    images = []
    
    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        # Extract the 'photos' column and convert it from string representation of list to actual list
        photo_urls = ast.literal_eval(row['photos'])  # Convert string representation of list to list
        
        for url in photo_urls:
            try:
                response = requests.get(url)
                response.raise_for_status()  # Ensure we got a valid response
                image_bytes = BytesIO(response.content)
                images.append(Image.open(image_bytes))
            except requests.exceptions.RequestException as e:
                print(f"Error fetching {url}: {e}")

    # Display images
    if images:
        fig, axes = plt.subplots(1, len(images), figsize=(5 * len(images), 5))
        if len(images) == 1:
            axes = [axes]  # Ensure iterable for single image
        for ax, img in zip(axes, images):
            ax.imshow(img)
            ax.axis("off")
        plt.show()
    else:
        print("No images to display.")

# Example usage
if __name__ == "__main__":
    # Define the path to the CSV file
    csv_file_path = r"C:\Users\karin\OneDrive - Bina Nusantara\Documents\skripsi\instagram-catfish-detector\cleaned_instagram_data.csv"  # Use raw string to avoid escape issues
    fetch_and_display_images_from_csv(csv_file_path)  # Pass the path to the function
