import json
import os
import requests
import logging
import hashlib
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_images_and_save_metadata(dataset_path, image_dir):
    # Ensure the image directory exists
    os.makedirs(image_dir, exist_ok=True)

    # Load cleaned dataset
    with open(dataset_path, 'r', encoding='utf-8') as f:
        cleaned_data = json.load(f)

    # Container for metadata
    metadata = []

    for entry in cleaned_data:
        for photo_url in entry['photos']:
            try:
                # Set headers to mimic a browser
                headers = {
                    'User -Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Referer': 'https://www.instagram.com/'
                }

                # Download the image
                response = requests.get(photo_url, headers=headers, timeout=10)
                
                # Check for 429 Too Many Requests
                if response.status_code == 429:
                    logging.warning("Received 429 Too Many Requests. Retrying after a delay...")
                    time.sleep(60)  # Wait for 60 seconds before retrying
                    response = requests.get(photo_url, headers=headers, timeout=10)

                response.raise_for_status()  # Raise an error for bad responses
                logging.info(f"Downloading image from {photo_url}")

                # Create a unique file name using a hash of the URL
                file_name = hashlib.md5(photo_url.encode()).hexdigest() + '.jpg'
                file_path = os.path.join(image_dir, file_name)

                # Save the image
                with open(file_path, 'wb') as img_file:
                    img_file.write(response.content)

                # Append metadata
                metadata.append({
                    'file_name': file_name,
                    'url': entry['url'],
                    'user_posted': entry['user_posted'],
                    'description': entry['description'],
                    'hashtags': entry['hashtags'],
                    'num_comments': entry['num_comments'],
                    'date_posted': entry['date_posted'],
                    'likes': entry.get('likes', 0),  # Default to 0 if likes is None
                    'is_verified': entry['is_verified'],
                    'followers': entry['followers']
                })

                logging.info(f"Successfully saved image: {file_name}")

                # Sleep to avoid rate limiting
                time.sleep(1)

            except requests.exceptions.RequestException as e:
                logging.error(f"Failed to download image from {photo_url}: {e}")

    # Save metadata to a JSON file
    metadata_file_path = os.path.join(image_dir, 'metadata.json')
    with open(metadata_file_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    logging.info(f"Metadata saved to {metadata_file_path}")

# Define paths
dataset_path = 'data/cleaned_dataset.json'  # Path to your cleaned dataset
image_dir = 'data/images/'                   # Directory to save images

# Run the function
download_images_and_save_metadata(dataset_path, image_dir)
